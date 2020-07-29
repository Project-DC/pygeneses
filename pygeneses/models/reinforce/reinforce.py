import torch
import torch.optim as optim

from .reinforce_nn import Agent


class ReinforceModel:
    def __init__(self, initial_population, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.agents = []
        self.optimizers = []
        self.scores = []
        self.saved_log_probs = {}
        self.rewards = {}
        self.policy_loss = {}

        self.init(initial_population)

    def init(self, initial_population):
        for idx in range(initial_population):
            self.agents.append(
                Agent(self.state_size, self.action_size, self.device).to(self.device)
            )
            self.optimizers.append(optim.Adam(self.agents[-1].parameters(), lr=1e-2))
            self.scores.append(0)
            self.saved_log_probs[idx] = []
            self.policy_loss[idx] = []
            self.rewards[idx] = []

    def predict_action(self, idx, state):
        action, log_prob, embed = self.agents[idx].act(state)
        self.saved_log_probs[idx].append(log_prob)

        return action, embed

    def update_reward(self, idx, reward):
        self.rewards[i].append(reward)


    def add_agents(self, parent_idx, num_offsprings):
        for idx in range(len(self.agents), len(self.agents) + num_offsprings):
            self.agents.append(
                Agent(self.state_size, self.action_size, self.device).to(self.device)
            )
            self.agents[-1].load_state_dict(self.agents[parent_idx].state_dict())
            self.optimizers.append(optim.Adam(self.agents[-1].parameters(), lr=1e-2))
            self.scores.append(0)
            self.saved_log_probs[idx] = []
            self.rewards[idx] = []

    def kill_agent(self, idx):
        self.agents[idx] = 0
        self.optimizers[idx] = 0
        self.scores[idx] = 0
        self.saved_log_probs[idx] = 0
        self.rewards[idx] = 0

    def update_all_agents(self):
        for idx in range(len(self.agents)):
            if type(self.agents[idx]) != int and len(self.saved_log_probs[idx]) > 0:
                self.policy_loss[idx] = []
                for j in range(len(self.saved_log_probs[idx])):
                    self.policy_loss[idx].append(-(self.saved_log_probs[idx][j] * self.rewards[idx][j]))
                self.policy_loss[idx] = torch.cat(self.policy_loss[idx]).sum()

                self.optimizers[idx].zero_grad()
                self.policy_loss[idx].backward(retain_graph=True)
                self.optimizers[idx].step()
