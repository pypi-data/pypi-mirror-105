"""
    Agent class containing Q network
"""

import keras
import numpy as np
import tensorflow as tf


class Agent:
    def __init__(self, n_s_vars, n_a_vars,
                 gamma, epsilon, batch_size=32, lr=0.001,
                 is_build_in=True, build_net=None):
        """
        Args:
            n_s_vars (int):         Number of state variables
            n_a_vars (int):         Number of action variables
            gamma (float):          Discount rate for a reward
            epsilon (float):        Exploration rate for epsilon-greedy search strategy
            batch_size (int):       Number of samples obtained from replay memory,
                                    and is regarded as a parameter of fit function
            lr (float):             Learning rate for optimizer
            is_build_in (bool):     Whether to use build-in model, default=True
            build_net (func):     Function, return a keras model object
        """

        self.n_s_vars = n_s_vars
        self.n_a_vars = n_a_vars
        self.gamma = gamma
        self.epsilon = epsilon
        self.batch_size = batch_size
        self.lr = lr
        self.is_build_in = is_build_in
        self.build_net = build_net
        if self.is_build_in:
            # Current Q network
            self.cur_net = Agent.build_in_net(input_shape=(self.n_s_vars,),
                                              n_outputs=self.n_a_vars)
            # Target Q network
            self.tar_net = Agent.build_in_net(input_shape=(self.n_s_vars,),
                                              n_outputs=self.n_a_vars)
        else:
            self.cur_net = self.build_net(input_shape=(self.n_s_vars,),
                                          n_outputs=self.n_a_vars)
            self.tar_net = self.build_net(input_shape=(self.n_s_vars,),
                                          n_outputs=self.n_a_vars)
        self.cur_weights = self.cur_net.get_weights()
        self.tar_net.set_weights(self.cur_weights)
        # Optimizer
        self.optimizer = keras.optimizers.Adam(lr=self.lr)
        self.ep_loss = list()

    @staticmethod
    def build_in_net(input_shape, n_outputs):
        _in = keras.Input(shape=input_shape, name='input_states')
        _out = keras.layers.Dense(units=32, activation=keras.activations.relu, )(_in)
        _out = keras.layers.Dense(units=32, activation=keras.activations.relu, )(_out)
        _out = keras.layers.Dense(units=n_outputs, activation=keras.activations.linear, )(_out)
        model = keras.Model(inputs=_in, outputs=_out)
        return model

    def update_for_dqn(self, prev_states, actions, rewards, next_states, done_batch):
        """
        Update current Q network for DQN
        Args:
            prev_states (numpy array):   Previous states, shape=(batch_size, n_s_vars)
            actions (numpy array):       Actions corresponding to previous states, shape=(batch_size, n_a_vars)
            rewards (numpy array):       Rewards corresponding to previous states, shape=(batch_size, )
            next_states (numpy array):   Next states, shape=(batch_size, n_s_vars)
            done_batch (numpy array):    Flag, shape=(batch_size, )
        """

        with tf.GradientTape() as tape:
            # Current network
            cur_pred = self.cur_net(prev_states, training=True)
            y_true = cur_pred.numpy()
            # Target network
            tar_pred = self.tar_net(next_states, training=True)
            tar_pred_array = tar_pred.numpy()
            # Loss
            for k in range(self.batch_size):
                done = done_batch[k]
                if done:
                    target = rewards[k]
                else:
                    target = rewards[k] + self.gamma * np.max(tar_pred_array[k, :])
                # y_true[k, actions[k]] = target
                y_true[k, np.argmax(actions[k])] = target
            y_true = tf.convert_to_tensor(y_true)
            loss = tf.keras.losses.mean_squared_error(y_true=y_true, y_pred=cur_pred)
            self.ep_loss.append(tf.reduce_mean(loss).numpy())
        cur_net_grad = tape.gradient(loss, self.cur_net.trainable_variables)
        self.optimizer.apply_gradients(zip(cur_net_grad, self.cur_net.trainable_variables))

    def update_for_ddqn(self, prev_states, actions, rewards, next_states, done_batch):
        """
        Update current Q network for Double DQN (DDQN)
        """
        pass

    def update_tar_net(self):
        """
        Update target network of Q network
        """

        self.cur_weights = self.cur_net.get_weights()
        self.tar_net.set_weights(self.cur_weights)

    def select_action(self, state):
        """
        Select action
        Args:
            state (numpy array):    State, shape=(n_s_vars, )
        Returns:
            action (numpy array):   Output action based on state, shape=(1, n_action)
        """

        if np.random.uniform(0, 1) <= self.epsilon:
            # Random selection
            action = np.random.uniform(0, 1, (1, self.n_a_vars))
            return action
        else:
            # Select according to Q network, shape=(1, n_actions)
            action = self.act(state)
            return action

    def act(self, state):
        """
        Act
        Args:
            state (numpy array):    State, shape=(n_s_vars, )
        Returns:
            action (numpy array):   Output action based on state, shape=(1, n_action)
        """

        state = np.reshape(state, (1, len(state)))
        action = self.cur_net(state)
        action = action.numpy()
        return action
