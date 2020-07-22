from reinforce_nn import Agent

class ReinforceModel():

    def __init__(self, initial_population):
        self.initial_population = []
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.agents = [Agent().to(device) for _ in range(world.INITIAL_POPULATION)]
        self.optimizers = [optim.Adam(agent.parameters(), lr=1e-2) for agent in agents]
        
