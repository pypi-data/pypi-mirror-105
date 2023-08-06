"""
    Critic
"""

import keras
import tensorflow as tf


class Critic:
    def __init__(self, n_s_vars, n_a_vars, n_outputs, n_agents=1,
                 gamma=0.9, tau=0.01, lr=0.001,
                 is_build_in=True, build_model=None):
        """
        Build a critic instance
        Args:
            n_s_vars (int):              Number of state variables
            n_a_vars (int):              Number of action variable
            n_outputs (int):
            n_agents (int):              Number of agents
            gamma (float):               Discount rate, default=0.9
            tau (float):                 Parameter of soft update used by updating target network, default=0.01
            lr (float):                  Learning rate of optimizer, default=0.001
            is_build_in (bool):          Whether to use build-in model based on keras framework, default=True
            build_model (function):      Function handle, default=None
        """

        self.n_s_vars = n_s_vars
        self.n_a_vars = n_a_vars
        self.n_outputs = n_outputs
        self.n_agents = n_agents
        self.lr = lr
        self.gamma = gamma
        self.tau = tau
        self.is_build_in = is_build_in
        self.build_model = build_model
        if self.is_build_in:
            self.cur_net = Critic.build_critic(in_s_shape=(self.n_s_vars,),
                                               in_a_shape=(self.n_a_vars * self.n_agents,),
                                               n_outputs=self.n_outputs)
            self.target_net = Critic.build_critic(in_s_shape=(self.n_s_vars,),
                                                  in_a_shape=(self.n_a_vars * self.n_agents,),
                                                  n_outputs=self.n_outputs)
        else:
            self.cur_net = self.build_model(in_s_shape=(self.n_s_vars,),
                                            in_a_shape=(self.n_a_vars * self.n_agents,),
                                            n_outputs=self.n_outputs)
            self.target_net = self.build_model(in_s_shape=(self.n_s_vars,),
                                               in_a_shape=(self.n_a_vars * self.n_agents,),
                                               n_outputs=self.n_outputs)
        self.target_net.set_weights(self.cur_net.get_weights())
        # Optimizer
        self.optimizer = keras.optimizers.Adam(lr=self.lr)

    @staticmethod
    def build_critic(in_s_shape, in_a_shape, n_outputs):
        """
        Build critic network
        Args:
            in_s_shape (tuple):     Shape of input of Input layers named 'state'
            in_a_shape (tuple):     Shape of input of Input layers named 'action'
            n_outputs (int):        Number of units of output layer
        Returns:
            model:                  Model based on keras
        """

        # Input: state
        _in_state = keras.layers.Input(shape=in_s_shape)
        _out_state = keras.layers.Dense(units=64, activation="relu")(_in_state)
        # AInput: action
        _in_action = keras.layers.Input(shape=in_a_shape)
        _out_action = keras.layers.Dense(units=64, activation="relu")(_in_action)

        # Both are passed through separate layer before concatenating
        _out = keras.layers.Concatenate(axis=1)([_out_state, _out_action])
        _out = keras.layers.Dense(units=64, activation="relu")(_out)

        # Output
        _out = keras.layers.Dense(units=n_outputs)(_out)
        model = keras.Model(inputs=[_in_state, _in_action], outputs=_out)
        return model

    @tf.function
    def update(self, _actor, prev_states, actions, rewards, next_states, other_agents=None):

        with tf.GradientTape() as tape:
            # ------ Target actor ------
            if other_agents is None:
                next_actions = _actor.target_net(next_states, training=True)
            else:
                next_actions = list()
                for key in other_agents.keys():
                    _a = other_agents[key].actor.target_net(next_states, training=True)
                    next_actions.append(_a)
                next_actions = tf.concat(next_actions, axis=1)

            # ------ Target critic ------
            _y = self.target_net([next_states, next_actions], training=True)
            y = rewards + self.gamma * _y
            # ------ Current critic ------
            critic_value = self.cur_net([prev_states, actions], training=True)
            critic_loss = tf.math.reduce_mean(tf.math.square(y - critic_value))

        critic_grad = tape.gradient(critic_loss, self.cur_net.trainable_variables)
        self.optimizer.apply_gradients(zip(critic_grad, self.cur_net.trainable_variables))

    def update_target_net(self):
        """
        Update target network of critic
        """

        target_weights = self.target_net.variables
        weights = self.cur_net.variables
        for (a, b) in zip(target_weights, weights):
            a.assign(b * self.tau + a * (1 - self.tau))

    def save_model(self, saved_path):
        """
        saved_path (list):       Filepath of saved models, [actor path, target actor path]
        """

        keras.models.save_model(self.cur_net, filepath=saved_path[0])
        keras.models.save_model(self.target_net, filepath=saved_path[1])

    def load_model(self, saved_path):
        """
        saved_path (list):       Filepath of saved models, [actor path, target actor path]
        """

        critic_net = keras.models.load_model(filepath=saved_path[0])
        critic_tar_net = keras.models.load_model(filepath=saved_path[1])
        self.cur_net = critic_net
        self.target_net = critic_tar_net
