import shutil
import torch

from particle_class import Particle
from reinforce import ReinforceModel

algorithm_to_class = {'REINFORCE': ReinforceModel}

class Chimichangas:

    def __init__(self, initial_population, algorithm='REINFORCE'):
        self.log_dir = 'Players_Data'
        self.reset_logs()
        self.players = []
        self.killed = []
        self.initial_population = 0
        self.my_particles = []
        self.agents = []
        self.optimizers = []
        self.scores = []
        self.rewards = {}
        self.algorithm = algorithm
        self.model = algorithm_to_class[algorithm](initial_population, state_size=21, action_size=13)

    def make(self):
        pygame.init()
        pygame.display.set_caption("Chimichangas")

        self.players = regenerate_species(TIME)

        for j in range(NUMBER_OF_PARTICLES):
            self.my_particles.append(Particle())

        self.my_particles = check_particles(my_particles)

        screen.fill((0, 178, 0))
        for event in pygame.event.get():
            pass
        pygame.display.update()

    def reset_logs(self):
        if os.path.exists(self.log_dir):
            shutil.rmtree(self.log_dir)
            os.mkdir(self.log_dir)
        else:
            os.mkdir(self.log_dir)

    def pad_state(state, maxlen):
        self.state_size = maxlen + 1
        if len(state) > maxlen:
            return state[:maxlen]
        elif len(state) < maxlen:
            new_state = np.zeros((maxlen,))
            new_state[:len(state)] = state
            return new_state
        elif len(state) == maxlen:
            return state

    def get_state(players, my_particles, killed):
        initial_state = []
        for i in range(len(players)):
            if type(players[i]) != int:
                env_particles,env_particle_distance = food_in_env(players[i], my_particles)
                env_food_vector = getFoodVector(players[i],env_particles, my_particles)
                env_food_vector = sum(env_food_vector, [])

                env_players, env_player_distance = players_in_env(players[i],players)
                env_player_vector = getPlayerVector(players[i],env_players, players)
                env_player_vector = sum(env_player_vector, [])

                temp_state = [env_food_vector, env_player_vector]
                temp_state = sum(temp_state, [])
                initial_state.append(np.array(temp_state))
            else:
                initial_state.append(np.array([0]))

        initial_state = [pad_state(state, STATE_SIZE-1) for state in initial_state]
        initial_state = [np.append(initial_state[i], players[i].energy) if type(players[i]) != int else np.append(initial_state[i], -100) for i in range(len(players))]

        return np.array(initial_state)
