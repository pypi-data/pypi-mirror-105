"""
    Multi Agents Deep Deterministic Policy Gradient, MADDPG
"""

import numpy as np
import tensorflow as tf


class MADDPG:
    def __init__(self, n_episodes, n_steps, n_states=1, state_bound=None,
                 n_actions=1, action_bound=None,
                 buffer_capacity=1E6, batch_size=128,
                 gamma=0.99, tau=0.01, ):
        self.n_episodes = n_episodes
        self.n_steps = n_steps
        self.n_states = n_states
        self.state_bound = state_bound
        self.n_actions = n_actions
        self.action_bound = action_bound
        self.buffer_capacity = int(buffer_capacity)
        self.buffer_pointer = 0
        self.batch_size = batch_size
        self.gamma = gamma
        self.tau = tau
        # Replay buffer
        self.replay_buffer = ReplayBuffer(capacity=self.buffer_capacity, batch_size=self.batch_size)
        # Agents
        self.agent_counter = 0
        self.agents = dict()
        # Parameters for Agent
        self.params = {'n_states': self.n_states, 'n_actions': self.n_actions,
                       'action_bound': self.action_bound,
                       'gamma': self.gamma, 'tau': self.tau}

    def add_agent(self, agent):
        self.agents[agent.name] = agent
        self.agent_counter += 1

    def learn(self):
        for key in self.agents.keys():
            # Random sample
            prev_states, actions, rewards, next_states = self.replay_buffer.sample()
            # Numpy array converts to tensors
            prev_state_batch = tf.convert_to_tensor(prev_states)
            action_batch = tf.convert_to_tensor(actions)
            reward_batch = tf.convert_to_tensor(rewards)
            reward_batch = tf.cast(reward_batch, dtype=tf.float32)
            next_state_batch = tf.convert_to_tensor(next_states)
            # Training and updating Actor & Critic networks
            self.agents[key].update(prev_state_batch, action_batch, reward_batch, next_state_batch)

    def train(self, env, noise=None):
        for ep in range(self.n_episodes):
            prev_state = env.reset()
            episode_reward = 0
            step_counter = 0
            while True:
                # Select action
                actions, norm_actions = list(), list()
                for key in self.agents.keys():
                    tf_prev_state = tf.expand_dims(tf.convert_to_tensor(prev_state), 0)
                    action = self.agents[key].actor.select_action(tf_prev_state, noise_obj=noise, step=step_counter)
                    norm_action = self.agents[key].actor.normalize(action, step_counter)
                    actions.append(action)
                    norm_actions.append(norm_action)
                # Receive state and reward from environment.
                next_state, reward, done, info = env.step(actions)
                step_counter += 1
                # Experience replay
                self.replay_buffer.add(prev_state, norm_actions, reward, next_state)
                episode_reward += reward
                # Update state
                prev_state = next_state
                # Learn
                self.learn()
                # Update the target networks
                for key in self.agents.keys():
                    self.agents[key].update_target_net()
                # End this episode when `done` is True
                if done:
                    # -------------- Debug --------------
                    # print('[Debug]  original reward: {}'.format(env.rewards.sum()))
                    break
