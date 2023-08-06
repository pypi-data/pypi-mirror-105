"""
    Q Learning
"""

import numpy as np
from DRLZ.utils.tool import epsilon_greedy


class QL:
    def __init__(self, state_space=None, action_space=None,
                 n_episodes=100, tol=1e-3,
                 alpha=0.1, gamma=0.9, reward_func=None,
                 method='epsilon_greedy', epsilon=0.5, is_return_index=True):
        """
        Initialize a QL instance
        Args:
            state_space (list/numpy array):      State space including all possible states of environment
            action_space (list/numpy array):     Action space including all executable actions of agent
            n_episodes (int):
            tol (float):                         Gap between Q_(t+1) and Q_t
            alpha (float):                       Learning rate for Q-learning
            gamma (float):                       Discount rate for a reward
            reward_func (func):                  Reward function
            method (str):                        Name of strategies for selecting action
            epsilon (float):                     Exploration rate for epsilon-greedy search strategy
            is_return_index (bool):              Whether to return index of selected action
        """

        self.state_space = state_space
        self.action_space = action_space
        self.n_episodes = n_episodes
        self.tol = tol
        self.alpha = alpha
        self.gamma = gamma
        self.reward_func = reward_func
        self.method = method
        self.epsilon = epsilon
        self.is_return_index = is_return_index

        self.n_s_vars = len(self.state_space)
        self.n_a_vars = len(self.action_space)
        self.q_table = np.zeros((self.n_s_vars, self.n_a_vars), dtype='float32')
        self.q_table_pre = np.inf * np.ones((self.n_s_vars, self.n_a_vars))
        self.episodes_counter = 0
        self.opt_action = None

    @staticmethod
    def select_action(method, q_table, state, action_space, epsilon, is_return_index):
        if method == 'epsilon_greedy':
            action, a_index = epsilon_greedy(q_table=q_table,
                                             state=state,
                                             action_space=action_space,
                                             epsilon=epsilon,
                                             is_return_index=is_return_index)
            return action, a_index
        else:
            print('Error in function of select_action')

    def cal_reward(self, s, a):
        return self.reward_func(s, a)

    def run_episode(self):
        for s in range(self.n_s_vars):
            # Agent selects the action based on state of environment
            action, a_index = QL.select_action(method=self.method,
                                               q_table=self.q_table,
                                               state=s,
                                               action_space=self.action_space,
                                               epsilon=self.epsilon,
                                               is_return_index=self.is_return_index)
            # Q update
            if s != self.n_s_vars - 1:
                self.q_table[s, a_index] = (1 - self.alpha) * self.q_table[s, a_index] \
                                           + self.alpha * (self.cal_reward(s, action)
                                                           + self.gamma * np.max(self.q_table[s + 1, :]))
            else:
                self.q_table[s, a_index] = (1 - self.alpha) * self.q_table[s, a_index] \
                                           + self.alpha * (self.cal_reward(s, action)
                                                           + self.gamma * np.max(self.q_table[0, :]))

    def train(self):
        while np.max(np.abs(self.q_table - self.q_table_pre)) > self.tol:
            self.episodes_counter += 1
            self.q_table_pre = np.copy(self.q_table)
            self.run_episode()

        # Best policy
        self.opt_action = [self.action_space[k] for k in np.argmax(self.q_table, axis=1)]
