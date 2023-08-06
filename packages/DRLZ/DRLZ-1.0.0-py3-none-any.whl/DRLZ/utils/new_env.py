"""
    Environment base class
"""

import numpy as np
from DRLZ.utils.tool import re_normalize, normalize


class Env:
    def __init__(self, n_states=1, n_actions=1, action_bound=None,
                 max_steps=24, reward_func=None, scale_factor=0.001,
                 verbose=True):
        """
        Args:
            n_states (int):                 Number of states
            n_actions (int):                Number of actions
            action_bound ():
            max_steps (int):                Number of steps in a episode
            reward_func (func):             Reward function name instead of a string of function name
            scale_factor (float):           Scale factor for reward
        """

        self.n_states = n_states
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
            return state

    def cal_reward(self, state, action, step):
        """
        Args:
            state (numpy array):   State which was not normalized, shape=(n_states, )
            action (list):         Action which was not normalized
            step (int):
        """

        reward = self.reward_func(state, action, step) * self.scale_factor
        return reward

    def reset(self):
        # Initialize the counter of step equal to -1
        self.step_counter = -1
        # Randomly select actions, 1-D vector
        # self.action = np.random.uniform(self.action_bound[0], self.action_bound[1], self.n_actions)
        action = list()
        # State, be scaled to [-1, 1]
        self.state = self.get_state(action)
        # Counter increase 1
        self.step_counter += 1
        return self.state

    def step(self, norm_action):
        """
        Args:
            norm_action (list):         Action which was normalized
        Returns:
            state (numpy array):        States
            reward (float):             Reward
            done (bool):                Done
            info:                       Nothing
        """

        if isinstance(norm_action, list):
            action = re_normalize(norm_action, x_bound=self.action_bound)
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

    def display_info(self):
        print('-'*26, 'Environment', '-'*26)
        print('- Num of states:  {} \n'
              '- Num of Actions: {} \n'
              '- Num of steps:   {} \n'
              '- Scale factor:   {}'
              . format(self.n_states, self.n_actions, self.max_steps, self.scale_factor))
        print('-'*65)
