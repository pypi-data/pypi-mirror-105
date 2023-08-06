"""
    Agent: actor-critic framework
"""

from DRLZ.DDPG.actor import Actor
from DRLZ.DDPG.critic import Critic


class Agent:
    def __init__(self, params, name='default', n_agents=1,
                 lr_actor=0.001, lr_critic=0.001,
                 is_build_in=True, build_actor=None, build_critic=None,
                 reward_func=None):
        """
        Build a agent instance
        Args:
            params (dict):          Other parameters from DDPG or MADDPG, e.g. gamma, tau etc.
            name (str):             Name of agent, default='default'
            n_agents (int):         Number of agents, default=1
            lr_actor (float):       Learning rate of optimizer for actor, default=0.001
            lr_critic (float):      Learning rate of optimizer for critic, default=0.001
            is_build_in (bool):     Whether to use build-in model based on keras framework, default=True
            build_actor:            Function handle, default=None
            build_critic:           Function handle, default=None
            reward_func:            Function handle, default=None
        """

        self.n_s_vars = params['n_states']
        self.n_a_vars = params['n_actions']
        self.action_space = params['action_bound']
        self.gamma = params['gamma']
        self.tau = params['tau']

        self.name = name
        self.n_agents = n_agents
        self.lr_actor = lr_actor
        self.lr_critic = lr_critic
        self.is_build_in = is_build_in
        self.build_actor = build_actor
        self.build_critic = build_critic
        self.reward_func = reward_func

        self.other_agents = None

        # Actor
        self.actor = Actor(n_s_vars=self.n_s_vars,
                           n_a_vars=self.n_a_vars,
                           tau=self.tau,
                           lr=self.lr_actor,
                           is_build_in=self.is_build_in,
                           build_model=self.build_actor)
        # Critic
        self.critic = Critic(n_s_vars=self.n_s_vars, n_a_vars=self.n_a_vars,
                             n_outputs=1,
                             n_agents=self.n_agents,
                             lr=self.lr_critic,
                             gamma=self.gamma,
                             tau=self.tau,
                             is_build_in=self.is_build_in,
                             build_model=self.build_critic)

    def update_cur_net(self, prev_states, actions, rewards, next_states):
        """
        Update current network of actor & critic
        Args:
            prev_states (numpy array):   Previous states, shape=(batch_size, n_s_vars)
            actions (numpy array):       Actions corresponding to previous states, shape=(batch_size, n_a_vars)
            rewards (numpy array):       Rewards corresponding to previous states, shape=(batch_size, )
            next_states (numpy array):   Next states, shape=(batch_size, n_s_vars)
        """

        # Critic
        self.critic.update(self.actor, prev_states, actions, rewards, next_states,
                           other_agents=self.other_agents)
        # Actor
        self.actor.update(self.critic, prev_states, other_agents=self.other_agents)

    def update_target_net(self):
        """
        Update target network of actor & critic
        """

        # Actor
        self.actor.update_target_net()
        # Critic
        self.critic.update_target_net()
