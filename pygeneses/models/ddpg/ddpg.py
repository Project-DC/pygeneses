import torch

from .ddpg_agent import Agent

class DDPGModel:

    def __init__(self, initial_population, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.agents = []
        self.current_state = {}
        self.current_action = {}
        self.current_reward = {}

        self.init(initial_population)

    def init(self, initial_population):
        for idx in range(initial_population):
            self.agents.append(
                Agent(self.state_size, self.action_size, self.device)
            )

            self.current_reward[idx] = 0

    def predict_action(self, idx, state):
        action, action_probs = self.agents[idx].act(state)

        self.current_state[idx] = state
        self.current_action[idx] = action_probs

        return action, []

    def update_reward(self, idx, reward):
        self.current_reward[idx] = reward

    def update_next_state(self, idx, next_state):
        self.agents[idx].step(self.current_state[idx], self.current_action[idx], self.current_reward[idx], next_state)

        self.current_state[idx] = 0
        self.current_action[idx] = 0
        self.current_reward[idx] = 0

    def add_agents(self, parent_idx, num_offsprings):
        for idx in range(len(self.agents), len(self.agents) + num_offsprings):
            self.agents.append(
                Agent(self.state_size, self.action_size, self.device, actor_local=self.agents[parent_idx].actor_local,
                      actor_target=self.agents[parent_idx].actor_target, critic_local=self.agents[parent_idx].critic_local,
                      critic_target=self.agents[parent_idx].critic_target)
            )

            self.current_state[idx] = 0
            self.current_action[idx] = 0
            self.current_reward[idx] = 0

    def kill_agent(self, idx):
        self.agents[idx] = 0
        self.current_state[idx] = 0
        self.current_action[idx] = 0
        self.current_reward[idx] = 0