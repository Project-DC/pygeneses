import torch
import torch.nn as nn
from torch.distributions import Categorical
import torch.nn.functional as F


class Agent(nn.Module):
    def __init__(self, s_size, a_size, device, h_size=30):
        super(Agent, self).__init__()
        self.device = device

        self.fc1 = nn.Linear(s_size, h_size)
        self.fc2 = nn.Linear(h_size, a_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.softmax(x, dim=1)

    def act(self, state):
        state = torch.from_numpy(state).float().unsqueeze(0).to(self.device)
        probs = self.forward(state).cpu()
        m = Categorical(probs)
        action = m.sample()
        return action.item(), m.log_prob(action)
