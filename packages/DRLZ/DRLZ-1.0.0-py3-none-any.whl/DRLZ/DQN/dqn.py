"""
    Deep D-learning Network Algorithm
    ---------------------------------
    - Author: zhf026
    - Email:  zhf026@outlook.com
"""

import numpy as np
import matplotlib.pyplot as plt
from DRLZ.DQN.agent import Agent
from DRLZ.utils.buffer import Buffer


class DQN:
    """
    Deep Q-learning Network based on NIPS 2015 (Aka Nature DQN)
    -------------------------------------------------------------------
    References: Human-level control through deep reinforcement learning
                https://www.nature.com/articles/nature14236
    """

    def __init__(self, n_episodes, n_s_vars, n_a_vars,
                 gamma=0.9, epsilon=0.5, min_epsilon=0.01, decay_factor=0.9,
                 buffer_len=1E6, batch_size=64, tar_updated_freq=10,
                 lr=0.001, is_build_in=True, build_model=None, verbose=True):
        """
        Initialize a DQN instance
        Args:
            n_episodes (int):       NUmber of episodes for a game
            n_s_vars (int):         Number of state variables
            n_a_vars (int):         Number of action variables
            gamma (float):          Discount rate for a reward
            epsilon (float):        Exploration rate for epsilon-greedy search strategy
            min_epsilon (float):    Minimal epsilon value
            decay_factor (float):   Decay factor for epsilon
            buffer_len (int):       Length of replay memory
            batch_size (int):       Number of samples obtained from replay memory,
                                    and is regarded as a parameter of fit function
        """

        self.n_episodes = n_episodes
        self.n_s_vars = n_s_vars
        self.n_a_vars = n_a_vars
        self.gamma = gamma
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.decay_factor = decay_factor
        self.buffer_capacity = int(buffer_len)
        self.batch_size = batch_size
        self.tar_updated_freq = tar_updated_freq
        self.lr = lr
        self.verbose = verbose
        # Buffer
        self.buffer = Buffer(n_s_vars=self.n_s_vars, n_a_vars=self.n_a_vars,
                             capacity=self.buffer_capacity, batch_size=self.batch_size)
        # Agent
        self.agent = Agent(n_s_vars=self.n_s_vars, n_a_vars=self.n_a_vars,
                           gamma=self.gamma, epsilon=self.epsilon,
                           batch_size=self.batch_size, lr=self.lr,
                           is_build_in=is_build_in, build_net=build_model)
        self.ep_rewards = list()

    def learn(self):
        # Random sample
        prev_states, actions, rewards, next_states, done_batch = self.buffer.random_sample()
        # Update current Q network
        self.agent.update_for_dqn(prev_states, actions, rewards, next_states, done_batch)

    def train(self, env):
        for ep in range(self.n_episodes):
            ep_reward = 0
            prev_state = env.reset()
            while True:
                # ------- Select action -------
                action = self.agent.select_action(prev_state)
                # ------- Step -------
                next_state, reward, done, _ = env.step(np.argmax(action[0]))
                ep_reward += reward
                # ------- Experience replay -------
                self.buffer.add(prev_state.copy(), action, reward, next_state.copy(), done)
                # ------- Learn -------
                self.learn()
                # ------- Update state -------
                prev_state = next_state.copy()
                # ------- Reduce epsilon -------
                if self.epsilon > self.min_epsilon:
                    self.epsilon *= self.decay_factor
                if done:
                    break
            # ------- Update target network -------
            if (ep + 1) % self.tar_updated_freq == 0:
                self.agent.update_tar_net()

            # Store the reward of each episode
            self.ep_rewards.append(ep_reward)

            # Display info
            if self.verbose:
                print('[DQN-train]  Episode: {}/{}  Reward: {}'.
                      format((ep + 1), self.n_episodes, round(ep_reward, 6)))

    def evaluate(self, env, n_episodes):
        total_reward = 0
        for ep in range(n_episodes):
            ep_reward = self.play_episode(env)
            total_reward += ep_reward
            if self.verbose:
                print('[DQN-evaluate]  Episode: {}/{}  Reward: {}'.
                      format((ep + 1), n_episodes, round(ep_reward, 6)))
        ave_reward = round(total_reward / n_episodes)
        print('[DQN-evaluate]  Run {} episodes  Average reward: {}' . format(n_episodes, ave_reward))

    def play_episode(self, env):
        ep_reward = 0
        state = env.reset()
        state = np.reshape(state, [1, self.n_s_vars])
        while True:
            action = self.agent.act(state)
            next_state, reward, done, info = env.step(np.argmax(action[0]))
            next_state = np.reshape(next_state, [1, self.n_s_vars])
            ep_reward += reward
            state = next_state.copy()
            if done:
                break
        return ep_reward

    def plot_result(self):
        plt.figure('Train result')
        plt.plot(self.ep_rewards, 'r')
        plt.xlim(0, self.n_episodes)
        plt.xlabel('Episodes')
        plt.ylabel('Reward of episode')
        plt.rcParams['font.sans-serif'] = ['Times New Roman']
        plt.show()
