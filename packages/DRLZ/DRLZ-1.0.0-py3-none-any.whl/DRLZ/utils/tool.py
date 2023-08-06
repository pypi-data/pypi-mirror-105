"""
    tool
"""


import numpy as np


def mapping(x, self_bound=None, target_bound=None):
    """
    Mapping to target boundary from self boundary
    Args:
        x (float):                       Input value
        self_bound (tuple or list):      Self boundary, e.g. (min, max) or [min, max]
        target_bound (tuple or list):    Target boundary, e.g. (min, max) or [min, max]
    """

    self_min, self_max = self_bound
    target_min, target_max = target_bound
    target_x = target_min + (target_max - target_min) / (self_max - self_min) * (x - self_min)
    return target_x


def normalize(x, x_bound, target_bound=(-1, 1)):
    """
    Args:
        x (list):                        List
        x_bound (numpy array):           shape=(len(x), 2)
        target_bound (tuple or list)     Target boundary, e.g. (min, max) or [min, max]
    Returns:
        norm_x (list):
    """

    norm_x = list()
    for k in range(len(x)):
        norm_x.append(mapping(x[k], self_bound=x_bound[k], target_bound=target_bound))
    return norm_x


def re_normalize(norm_x, x_bound, target_bound=(-1, 1)):
    """
    Args:
        norm_x (list):
        x_bound (numpy array):
        target_bound (tuple or list)     Target boundary, e.g. (min, max) or [min, max]
    Returns:
        x (list):
    """

    x = list()
    for k in range(len(norm_x)):
        x.append(mapping(norm_x[k], self_bound=target_bound, target_bound=x_bound[k]))
    return x


def epsilon_greedy(q_table, state, action_space, epsilon, is_return_index=False):
    """
    Epsilon greedy strategy for exploration
    ---------------------------------------
    Args:
        q_table (2D np.array):            Q table, the row presents states and the column presents actions
        state (int):                      Index of state, which is equal to the row index of Q table
        action_space (list/1D np.array):  Action space, which includes some different actions
        epsilon (float):                  Epsilon value, range is (0, 1)
        is_return_index (bool):
    Returns:
        action (object):                  Selected action, which is derived from the action set
    """

    if np.random.uniform(0, 1) <= epsilon:
        # Random selection
        n_a_vars = len(action_space)
        selected_index = np.random.randint(0, n_a_vars)
        action = action_space[selected_index]
    else:
        # Select from Q table
        selected_index = np.argmax(q_table[state, :])
        action = action_space[selected_index]

    if is_return_index:
        return action, selected_index
    else:
        return action
