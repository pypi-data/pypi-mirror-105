"""
    Environment base class
"""

import numpy as np


class Env:
    def __init__(self, n_states=1, state_bound=None, n_actions=1, action_bound=None,
                 max_steps=24, reward_func=None, scale_factor=0.001,
                 verbose=True):
        """
        Args:
            n_states (int):                 Number of states
            state_bound (numpy array):      3-D numpy array, shape=(n_states, max_steps, 2)
            n_actions (int):                Number of actions
            action_bound ():
            max_steps (int):                Number of steps in a episode
            reward_func (func):             Reward function name instead of a string of function name
            scale_factor (float):           Scale factor for reward
        """

        self.n_states = n_states
        self.state_bound = state_bound
        self.n_actions = n_actions
        self.action_bound = action_bound
        self.max_steps = max_steps
        self.reward_func = reward_func
        self.scale_factor = scale_factor

        self.state_mapping_bound = [-1, 1]
        self.state = None
        self.action = None
        self.done = None
        self.reward = None
        self.rewards = np.zeros((self.max_steps, ), )

        self.step_counter = -1

        if verbose:
            self.display_info()

    def get_state(self, action):
        """
        Args:
            action (list):         actions
        Returns:
            state (numpy array):   State scaled to [-1, 1]
        """

        if isinstance(action, list):
            t = self.step_counter
            # TODO: your code
            s0 = None
            # State
            state = np.array([s0, ])
            # Scaled states
            scaled_state = self.normalize(state, t)
            return scaled_state

    def cal_reward(self, scaled_state, action, step):
        """
        Args:
            scaled_state (numpy array):
            action (list):
            step (int):
        """

        state = self.re_normalize(scaled_state, step)
        reward = self.reward_func(state, action, step) * self.scale_factor
        return reward

    def step(self, action):
        """
        Args:
            action (list):        Actions
        Returns:
            state (numpy array):  States
            reward (float):       Reward
            done (bool):          Done
            info:                 Nothing
        """

        if isinstance(action, list):
            # State, be scaled to [-1, 1]
            self.state = self.get_state(action)
            # Reward
            self.reward = self.cal_reward(self.state, action, self.step_counter)
            self.rewards[self.step_counter] = self.reward / self.scale_factor
        # Counter increase 1
        self.step_counter += 1
        # Done
        if self.step_counter < self.max_steps:
            self.done = False
        else:
            self.done = True
        # Info
        info = None  # Not working
        return self.state, self.reward, self.done, info

    def reset(self):
        # Initialize the counter of step equal to -1
        self.step_counter = -1
        # Randomly select actions, 1-D vector
        # self.action = np.random.uniform(self.action_bound[0], self.action_bound[1], self.n_actions)
        action = list()
        for k in range(self.n_actions):
            action.append(np.random.uniform(self.action_bound[k, 0, 0], self.action_bound[k, 0, 1]))
        # State, be scaled to [-1, 1]
        self.state = self.get_state(action)
        # Counter increase 1
        self.step_counter += 1
        return self.state

    @staticmethod
    def mapping(x, self_bound=None, target_bound=None):
        """
        Args:
            x (float, Numpy array) :    Input
            self_bound (list):          Range of x, e.g. [min_x, max_x]
            target_bound (list):        Range of target, e.g. [min, max]
        Returns:
            _x (float):                 Output
        """

        self_min, self_max = self_bound
        target_min, target_max = target_bound
        _x = target_min + (target_max - target_min) / (self_max - self_min) * (x - self_min)
        return _x

    def normalize(self, state, step):
        """
        Args:
            state (numpy array):
            step (int):
        Returns:
            scaled_state (numpy array):
        """

        scaled_state = np.zeros((len(state),))
        for k in range(len(state)):
            # Range
            state[k] = np.clip(state[k], self.state_bound[k, step, 0], self.state_bound[k, step, 1])
            # Scale
            scaled_state[k] = Env.mapping(state[k], self_bound=self.state_bound[k, step, :],
                                          target_bound=self.state_mapping_bound)
        return scaled_state

    def re_normalize(self, scaled_state, step):
        """
        Args:
            scaled_state (numpy array):
            step (int):
        Returns:
            state (numpy array):
        """

        state = np.zeros((len(scaled_state), ))
        for k in range(len(scaled_state)):
            state[k] = Env.mapping(scaled_state[k], self_bound=self.state_mapping_bound,
                                   target_bound=self.state_bound[k, step, :])
        return state

    def display_info(self):
        print('-'*26, 'Environment', '-'*26)
        print('- Num of states:  {} \n'
              '- Num of Actions: {} \n'
              '- Num of steps:   {} \n'
              '- Scale factor:   {}'
              . format(self.n_states, self.n_actions, self.max_steps, self.scale_factor))
        print('-'*65)
