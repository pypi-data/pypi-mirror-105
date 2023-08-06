"""
    Buffer class
"""

import numpy as np


class Buffer:
    def __init__(self, n_s_vars, n_a_vars, n_agents=1, capacity=1e6, batch_size=100):
        """
        Build a buffer instance
        Args:
            n_s_vars (int):         Numbers of state variables
            n_a_vars (int):         Numbers of action variables
            n_agents (int):         Number of agents
            capacity (int):         Capacity of Buffer
            batch_size (int):
        """

        self.n_s_vars = n_s_vars
        self.n_a_vars = n_a_vars
        self.n_agents = n_agents
        self.capacity = capacity
        self.batch_size = batch_size

        self.pointer = 0
        self._prev_states = np.zeros((self.capacity, self.n_s_vars), dtype='float32')
        self._actions = np.zeros((self.capacity, self.n_a_vars*self.n_agents), dtype='float32')
        self._rewards = np.zeros((self.capacity, 1), dtype='float32')
        self._next_states = np.zeros((self.capacity, self.n_s_vars), dtype='float32')
        self._done = np.zeros((self.capacity, 1))
        self._is_cons = np.zeros((self.capacity, 1))

    def add(self, prev_state, action, reward, next_state, done=False, is_cons=False):
        """
        Experience replay
        Args:
            prev_state (numpy array):   Previous state, shape=(1, n_states)
            action (numpy array):       Action corresponding to previous state, shape=(1, n_action)
            reward (float):             Reward corresponding to previous state
            next_state (numpy array):   Next state, shape=(1, n_states)
            done (bool):                Flag
            is_cons (bool):
        """

        # Set index to zero if buffer_capacity is exceeded, replacing old records
        index = self.pointer % self.capacity
        self._prev_states[index] = prev_state
        self._actions[index] = action
        self._rewards[index] = reward
        self._next_states[index] = next_state
        self._done[index] = done
        self._is_cons[index] = is_cons
        # Buffer pointer increase 1
        self.pointer += 1

    def random_sample(self):
        record_range = min(self.pointer, self.capacity)
        batch_indices = np.random.choice(record_range, self.batch_size)

        prev_states = self._prev_states[batch_indices]
        actions = self._actions[batch_indices]
        rewards = self._rewards[batch_indices]
        next_states = self._next_states[batch_indices]
        done_batch = self._done[batch_indices]

        return prev_states, actions, rewards, next_states, done_batch
