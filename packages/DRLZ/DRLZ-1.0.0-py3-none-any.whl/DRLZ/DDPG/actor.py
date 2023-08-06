"""
    Actor
"""

import keras
import numpy as np
import tensorflow as tf


class Actor:
    def __init__(self, n_s_vars, n_a_vars,
                 lr=0.001, tau=0.01,
                 is_build_in=True, build_model=None):
        """
        Build a actor instance
        Args:
            n_s_vars (int):          Number of state variables
            n_a_vars (int):          Number of action variable
            tau (float):             Parameter of soft update used by updating target network, default=0.01
            lr (float):              Learning rate of optimizer, default=0.001
            is_build_in (bool):      Whether to use build-in model based on keras framework, default=True
            build_model:             Function handle, default=None
        """

        self.n_s_vars = n_s_vars
        self.n_a_vars = n_a_vars
        self.tau = tau
        self.lr = lr
        self.is_build_in = is_build_in
        self.build_model = build_model
        if self.is_build_in:
            self.cur_net = Actor.build_actor(input_shape=(self.n_s_vars,),
                                             n_outputs=self.n_a_vars)
            self.target_net = Actor.build_actor(input_shape=(self.n_s_vars,),
                                                n_outputs=self.n_a_vars)
        else:
            self.cur_net = self.build_model(input_shape=(self.n_s_vars,),
                                            n_outputs=self.n_a_vars)
            self.target_net = self.build_model(input_shape=(self.n_s_vars,),
                                               n_outputs=self.n_a_vars)
        self.target_net.set_weights(self.cur_net.get_weights())
        # Optimizer
        self.optimizer = keras.optimizers.Adam(lr=self.lr)

    @staticmethod
    def build_actor(input_shape, n_outputs):
        """
        Build actor network
        Args:
            input_shape (tuple):    Shape of input for Input layers of keras
            n_outputs (int):        Number of units of output layer
        Returns:
            model:                  Model based on keras
        """

        _in_state = keras.layers.Input(shape=input_shape)
        _out_action = keras.layers.Dense(units=64,
                                         activation="relu",
                                         kernel_initializer=keras.initializers.random_normal(0, 0.1))(_in_state)
        _out_action = keras.layers.Dense(units=n_outputs,
                                         activation=keras.activations.tanh,
                                         )(_out_action)
        model = keras.Model(inputs=_in_state, outputs=_out_action)
        return model

    @tf.function
    def update(self, _critic, prev_states, other_agents=None):

        with tf.GradientTape() as tape:
            # ------ Current actor ------
            if other_agents is None:
                actions = self.cur_net(prev_states, training=True)
            else:
                actions = list()
                for key in other_agents.keys():
                    _a = other_agents[key].actor.cur_net(prev_states, training=True)
                    actions.append(_a)
                actions = tf.concat(actions, axis=1)

            # ------ Current critic ------
            critic_value = _critic.cur_net([prev_states, actions], training=True)
            # Used `-value` as we want to maximize the value given by the critic for our actions
            actor_loss = -tf.math.reduce_mean(critic_value)

        actor_grad = tape.gradient(actor_loss, self.cur_net.trainable_variables)
        self.optimizer.apply_gradients(zip(actor_grad, self.cur_net.trainable_variables))

    def update_target_net(self):
        """
        Update target network of actor
        """

        target_weights = self.target_net.variables
        weights = self.cur_net.variables
        for (a, b) in zip(target_weights, weights):
            a.assign(b * self.tau + a * (1 - self.tau))

    def select_action(self, state, noise_obj=None, step=None):
        """
        Select a action based on current network of actor and current state
        Args:
            state (numpy array):      State which was normalized, shape=(n_s_vars, )
            noise_obj (noise obj):
            step:                     No used
        Returns:
            action (list):            Action which was normalized
        """

        if noise_obj is not None:
            action = self.act(state=state, step=step)
            # Add noise, numpy array, shape=(n_actions, )
            noise = noise_obj()
            for k in range(len(action)):
                action[k] = action[k] + noise[k]
            return action
        else:
            action = self.act(state=state, step=step)
            return action

    def act(self, state, step=None):
        """
        Select a action based on trained network and current state
        Args:
            state (numpy array):      State which was normalized, shape=(n_s_vars, )
            step:
        Returns:
            action (list):            Action which was normalized
        """

        # Current state
        state = np.reshape(state, (1, len(state)))
        # Select action
        action = self.cur_net(state).numpy()
        action = np.reshape(action, (action.shape[1], ))
        action = action.tolist()
        if not isinstance(action, list):
            action = [action]
        return action

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

        actor_net = keras.models.load_model(filepath=saved_path[0])
        actor_tar_net = keras.models.load_model(filepath=saved_path[1])
        self.cur_net = actor_net
        self.target_net = actor_tar_net
