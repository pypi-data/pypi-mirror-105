"""
    Deep Deterministic Policy Gradient, DDPG
"""

import numpy as np
import matplotlib.pyplot as plt
from DRLZ.DDPG.agent import Agent
from DRLZ.utils.buffer import Buffer


class DDPG:
    def __init__(self, n_episodes=100, n_steps=24,
                 n_s_vars=1, state_space=None,
                 n_a_vars=1, action_space=None,
                 buffer_capacity=1e6, batch_size=128,
                 gamma=0.9, tau=0.01,
                 lr_actor=0.001, lr_critic=0.001,
                 is_build_in=True, build_actor=None, build_critic=None,
                 verbose=True, is_saved=False):
        """
        Args:
            n_episodes (int):               Numbers of episodes
            n_steps (int):                  Numbers of steps for each episodes, i.e. the number of states located
            n_s_vars (int):                 Numbers of state variables
            n_a_vars (int):                 Numbers of action variables
            action_space (numpy array):     Boundary of continuous action
            buffer_capacity (int):          Capacity of buffer
            batch_size (int):               Number of random sample from buffer
            gamma (float):                  Discount rate, default=0.9
            tau (float):                    Parameter of soft update used by updating target network, default=0.01
            lr_actor (float):               Learning rate of optimizer for actor, default=0.001
            lr_critic (float):              Learning rate of optimizer for critic, default=0.001
            is_build_in (bool):             Whether to use build-in model based on keras framework, default=True
            build_actor:                    Function handle, default=None
            build_critic:                   Function handle, default=None
            verbose (bool):                 Whether to display information
            is_saved (bool):                Whether to save the weights of models
        """

        self.n_episodes = n_episodes
        self.n_steps = n_steps
        self.n_s_vars = n_s_vars
        self.state_space = state_space
        self.n_a_vars = n_a_vars
        self.action_space = action_space
        self.buffer_capacity = int(buffer_capacity)
        self.buffer_pointer = 0
        self.batch_size = batch_size
        self.gamma = gamma
        self.tau = tau
        self.lr_actor = lr_actor
        self.lr_critic = lr_critic
        self.is_build_in = is_build_in
        self.build_actor = build_actor
        self.build_critic = build_critic
        self.verbose = verbose
        self.is_saved = is_saved

        self.ep_rewards = list()
        self.avg_rewards = list()
        self.opt_reward = -np.inf

        # Buffer
        self.replay_buffer = Buffer(n_s_vars=self.n_s_vars,
                                    n_a_vars=self.n_a_vars,
                                    capacity=self.buffer_capacity,
                                    batch_size=self.batch_size)
        # Agent
        params = {'n_states': self.n_s_vars, 'n_actions': self.n_a_vars,
                  'action_bound': self.action_space,
                  'gamma': self.gamma, 'tau': self.tau}
        self.agent = Agent(params=params,
                           name='ddpg-agent',
                           lr_actor=self.lr_actor,
                           lr_critic=self.lr_critic,
                           is_build_in=self.is_build_in,
                           build_actor=self.build_actor,
                           build_critic=self.build_critic,)

    def learn(self):
        # Random sample
        prev_states, actions, rewards, next_states, done_batch = self.replay_buffer.random_sample()
        # Training and updating Actor & Critic networks
        self.agent.update_cur_net(prev_states, actions, rewards, next_states)

    def train(self, env, noise=None):
        """
        Args:
            env (instance class):    Environment
            noise (instance class):  Noise
        """

        print('[DDPG] Training ...')
        for ep in range(self.n_episodes):
            ep_reward = 0
            prev_state = env.reset()
            while True:
                # ------- Select action -------
                action = self.agent.actor.select_action(prev_state, noise_obj=noise, step=step_counter)
                # ------- Step -------
                next_state, reward, done, _ = env.step(action)
                ep_reward += reward
                # ------- Experience replay -------
                self.replay_buffer.add(prev_state.copy(), action, reward, next_state.copy(), done)
                # ------- Learn -------
                self.learn()
                # ------- Update state -------
                prev_state = np.copy(next_state)
                # ------- Update target networks -------
                self.agent.update_target_net()
                if done:
                    break

            # Store the reward of each episode
            self.ep_rewards.append(ep_reward)

            # Display info
            if self.verbose:
                print('[DDPG-train]  Episode: {}/{}  Reward: {}'.
                      format((ep + 1), self.n_episodes, round(ep_reward, 6)))

    def evaluate(self, env, n_episodes=1, is_render=False):
        """
        Args:
            env (instance class):  Environment
            n_episodes (int):      Numbers of episodes
            is_render (bool):      Be used when the env is gym environment
        """

        print('[DDPG] Evaluate ...')
        total_reward = 0
        for ep in range(n_episodes):
            ep_reward = self.play_episode(env, is_render=is_render)
            total_reward += ep_reward
            if self.verbose:
                print('[DDPG-Evaluate]  Episode: {}/{}  |  Reward: {}'
                      .format(ep + 1, n_episodes, round(ep_reward, 3)))
        ave_reward = round(total_reward / n_episodes)
        print('[DDPG-evaluate]  Run {} episodes  Average reward: {}'.format(n_episodes, ave_reward))

    def play_episode(self, env, is_render=False):
        ep_reward = 0
        step_counter = 0

        prev_state = env.reset()
        while True:
            if is_render:
                env.render()
            action = self.agent.actor.act(prev_state, step=step_counter)
            next_state, reward, done, info = env.step(action)
            step_counter += 1
            ep_reward += reward
            prev_state = np.copy(next_state)
            if done:
                if is_render:
                    env.close()
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
