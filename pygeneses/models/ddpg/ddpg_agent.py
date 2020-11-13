import numpy as np
import random
import copy
from collections import namedtuple, deque

from .ddpg_nn import Actor, Critic
from .buffer import ReplayBuffer
from .constants import *

import torch
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical

class Agent():
    """Interacts with and learns from the environment."""

    def __init__(self, state_size, action_size, device, actor_local=None, actor_target=None, critic_local=None,
                 critic_target=None, memory=None, random_seed=0):
        """Initialize an Agent object.
        Params
        ======
            state_size (int): dimension of each state
            action_size (int): dimension of each action
            random_seed (int): random seed
        """
        self.state_size = state_size
        self.action_size = action_size
        self.seed = random.seed(random_seed)
        self.device = device

        # Actor Network (w/ Target Network)
        self.actor_local = Actor(self.state_size, self.action_size, random_seed).to(self.device) if actor_local == None else actor_local
        self.actor_target = Actor(self.state_size, self.action_size, random_seed).to(self.device) if actor_target == None else actor_target
        self.actor_optimizer = optim.Adam(self.actor_local.parameters(), lr=LR_ACTOR)

        # Critic Network (w/ Target Network)
        self.critic_local = Critic(self.state_size, self.action_size, random_seed).to(self.device) if critic_local == None else critic_local
        self.critic_target = Critic(self.state_size, self.action_size, random_seed).to(self.device) if critic_target == None else critic_target
        self.critic_optimizer = optim.Adam(self.critic_local.parameters(), lr=LR_CRITIC)

        # Replay memory
        self.memory = ReplayBuffer(self.action_size, BUFFER_SIZE, BATCH_SIZE, random_seed, self.device)

    def step(self, state, action, reward, next_state):
        """Save experience in replay memory, and use random sample from buffer to learn."""
        # Save experience / reward
        self.memory.add(state, action, reward, next_state)

        # Learn, if enough samples are available in memory
        if len(self.memory) >= BATCH_SIZE:
            experiences = self.memory.sample()
            self.learn(experiences, GAMMA)

    def act(self, state):
        """Returns actions for given state as per current policy."""
        state = torch.from_numpy(state).float().to(self.device)
        self.actor_local.eval()
        with torch.no_grad():
            state = state.unsqueeze(0)
            probs = self.actor_local(state)
            m = Categorical(probs)
            action = m.sample()
        self.actor_local.train()

        return action.item(), probs

    def learn(self, experiences, gamma):
        """Update policy and value parameters using given batch of experience tuples.
        Q_targets = r + γ * critic_target(next_state, actor_target(next_state))
        where:
            actor_target(state) -> action
            critic_target(state, action) -> Q-value
        Params
        ======
            experiences (Tuple[torch.Tensor]): tuple of (s, a, r, s', done) tuples
            gamma (float): discount factor
        """
        states, actions, rewards, next_states = experiences

        # ---------------------------- update critic ---------------------------- #
        # Get predicted next-state actions and Q values from target models
        action_probs_next = self.actor_target(next_states)
        Q_targets_next = self.critic_target(next_states, action_probs_next)
        # Compute Q targets for current states (y_i)
        Q_targets = rewards + (gamma * Q_targets_next)
        # Compute critic loss
        Q_expected = self.critic_local(states, actions)
        critic_loss = F.mse_loss(Q_expected, Q_targets)
        # Minimize the loss
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

        # ---------------------------- update actor ---------------------------- #
        # Compute actor loss
        actions_probs_pred = self.actor_local(states)
        actor_loss = -self.critic_local(states, actions_probs_pred).mean()
        # Minimize the loss
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()

        # ----------------------- update target networks ----------------------- #
        self.soft_update(self.critic_local, self.critic_target, TAU)
        self.soft_update(self.actor_local, self.actor_target, TAU)

    def soft_update(self, local_model, target_model, tau):
        """Soft update model parameters.
        θ_target = τ*θ_local + (1 - τ)*θ_target
        Params
        ======
            local_model: PyTorch model (weights will be copied from)
            target_model: PyTorch model (weights will be copied to)
            tau (float): interpolation parameter
        """
        for target_param, local_param in zip(target_model.parameters(), local_model.parameters()):
            target_param.data.copy_(tau*local_param.data + (1.0-tau)*target_param.data)
