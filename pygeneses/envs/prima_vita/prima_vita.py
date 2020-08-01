# Primary class for the environment (prima vita - first life)

# Import required libraries
import os
import shutil
import pygame
import random
import numpy as np

# Import other classes
from .player_class import Player
from .particle_class import Particle
from .global_constants import *
from pygeneses.models.reinforce.reinforce import ReinforceModel

# Dictionary to map from string to name of model
model_to_class = {"reinforce": "ReinforceModel"}


class PrimaVita:
    """
    Environment class for the species - Prima vita (First life)

    Data members
    ============
    log_dir                     (str)
       : The path to log directory where agent's life history to be logged
    initial_population          (int)
       : Size of initial population when agent starts
    state_size                  (int)
       : Number of variables in state that the agent experiences during his/her/its lifetime
    action_size                 (int)
       : Total number of possible actions that agent can take
    time                        (int)
       : Time of the environment (not in seconds, but in ticks), this changes when entire population
         completes one action
    regenerate_times            (int)
       : The number of times population has been regenerated after perishing
    max_regenerations           (int)
       : The maximum number of times population can be regenerated after perishing
    allow_regenerate            (bool)
       : Population can be regenerated after perishing or not
    food_regen_condition_is_met (bool)
       : Should food be regenerated now or not based on certain minimum threshold
    players                     (numpy.ndarray)
       : NumPy array of Player objects (representing the agents in the world)
    killed                      (numpy.ndarray)
       : NumPy array containing ids of killed players
    food_particles              (numpy.ndarray)
       : NumPy array containing Particle objects (representing food particles in the world)
    number_of_particles         (int)
       : Total number of food particles in the environment at the beginning of time (TICK = 0)
    particles_to_regrow         (int)
       : Number of particles to be regrown
    model                       (pygeneses.models)
       : Instance of pygeneses.models (RL algorithms)
    model_updates               (int)
       : Number of ticks after which model for all the population will be updated
    speed                       (int)
       : Speed with which agent moves in the environment (in pixels)
    max_age                     (int)
       : Maximum age that an agent can live up to
    """

    def __init__(
        self,
        initial_population=10,
        state_size=21,
        action_size=13,
        max_regenerations=0,
        model_updates=10,
    ):
        """
        Initializer for PrimaVita class

        Params
        ======
        initial_population (int)
            : Size of initial population when agent starts
        state_size         (int)
            : Number of variables in state that the agent experiences during his/her/its lifetime
        action_size        (int)
            : Total number of possible actions that agent can takes
        max_regenerations  (int)
            : The maximum number of times population can be regenerated after perishing
        model_updates      (int)
            : Number of ticks after which model for all the population will be updated
        """

        self.log_dir = "Players_Data"
        self.initial_population = initial_population
        self.state_size = state_size
        self.action_size = action_size
        self.time = -1
        self.regenerate_times = 0
        self.max_regenerations = max_regenerations
        self.allow_regenerate = True if max_regenerations > 0 else False
        self.food_regen_condition_is_met = False
        self.players = np.array([])
        self.killed = np.array([])
        self.food_particles = np.array([])
        self.number_of_particles = random.randint(70, 80)
        self.particles_to_regrow = (
            20,
            40,
        )  # Control this food to control max population
        self.model = 0
        self.model_updates = model_updates
        self.speed = 3
        self.max_age = 90

        self.reset_logs()

    def init(self, model_name="reinforce"):
        """
        Initialise the environment

        Params
        ======
        model_name (str):
            Name of the model to be used to train agents
        """

        # Initialise pygame
        pygame.init()

        # Title
        pygame.display.set_caption("Prima Vita")

        # Generate initial population
        self.time = 0
        self.regenerate_species()
        self.time -= 1

        # Put food particles in the environment
        for j in range(self.number_of_particles):
            self.food_particles = np.append(self.food_particles, Particle())

        # Remove food particles which either overlap or are very close to another food particle
        self.check_particles()

        # Initialize the model, convert string to name of model and evaluate that to convert to class name
        self.model = eval(model_to_class[model_name])(
            self.initial_population, self.state_size, self.action_size
        )

        # Fill the screen with green color
        screen.fill((0, 178, 0))

        # Event loop (# NOT REQUIRED here)
        for event in pygame.event.get():
            pass

        # Update pygame screen
        pygame.display.update()

    def reset_logs(self):
        """
        Delete directory containing logs if it already exists
        """

        # Check if log_dir already exists, if it does delete the directory and everything in it
        if os.path.exists(self.log_dir):
            shutil.rmtree(self.log_dir)

        # Create log directory and a directory inside this that holds embeddings for each agent
        os.mkdir(self.log_dir)
        os.mkdir(os.path.join(self.log_dir, "Embeddings"))

    def pad_state(self, state, maxlen):
        """
        Pad state array to a maximum length

        Params
        ======
        state  (numpy.ndarray)
            : NumPy array containing a state value for some agent
        maxlen (int)
            : Maximum length for the state to be padded to

        Returns
        =======
        state  (numpy.ndarray)
            : The padded state
        """

        # If the length of state is greater than maxlen then cut the remaining values
        if len(state) > maxlen:
            return state[:maxlen]
        # If the length of state is lesser than maxlen then pad it with zeros
        elif len(state) < maxlen:
            new_state = np.zeros((maxlen,))
            new_state[: len(state)] = state
            return new_state
        # If the length of state is equal to maxlen then return it as it is
        elif len(state) == maxlen:
            return state

    def get_current_state(self):
        """
        Return the current state of all the agents in the environment

        Returns
        =======
        initial_state (numpy.ndarray)
            : The state of all the agents in the environment, it contains vector (x, y) to
              all the food particles around a fixed radius of an agent, vector (x, y, sex) to
              all the agents in the same radius - these vectors are padded to match state_size - 1
              and the final entry in the state vector is the current energy of the agent
        """

        # If everyone is killed then return -1
        if len(self.killed) == len(self.players):
            return -1

        # List containing states of all the agents
        initial_state = []

        # Loop through all of the players
        for i in range(len(self.players)):
            # If a player is not dead then
            if type(self.players[i]) != int:
                # Get the food particles in environment
                env_particles, env_particle_distance = self.food_in_env(self.players[i])

                # Get all the food particle vectors close to current agent
                env_food_vector = self.getFoodVector(self.players[i], env_particles)

                # Convert all the vectors into a single vector
                env_food_vector = sum(env_food_vector, [])

                # Get the agents in environment
                env_players, env_player_distance = self.players_in_env(self.players[i])

                # Get the agents in radius of current agent
                env_player_vector = self.getPlayerVector(self.players[i], env_players)

                # Convert all the vectors into a single vector
                env_player_vector = sum(env_player_vector, [])

                # Stack together the food and player vectors
                temp_state = [env_food_vector, env_player_vector]

                # Save this as state in current agent's object
                self.players[i].states.append(
                    np.array([np.array(env_food_vector), np.array(env_player_vector)])
                )

                # Convert the food and player vectors stacked together into a single vector
                temp_state = sum(temp_state, [])

                # Convert this state to numpy.ndarray and append to initial_state
                initial_state.append(np.array(temp_state))
            else:
                # If agent is dead append an array with a single value - zero
                initial_state.append(np.array([0]))

        # Pad all the states
        initial_state = [
            self.pad_state(state, self.state_size - 1) for state in initial_state
        ]

        # Append energy if player isn't dead else append -100
        initial_state = [
            np.append(initial_state[i], self.players[i].energy)
            if type(self.players[i]) != int
            else np.append(initial_state[i], -100)
            for i in range(len(self.players))
        ]

        # Return the state as numpy array
        return np.array(initial_state)

    def take_action(self, idx, state):
        """
            Take an action, make changes to environment, return rewards

            Params
            ======
            idx   (int)
                : Index of the player to take action
            state (numpy.ndarray)
                : State that the agent currently experiences
        """

        # Predict action and return embedding using RL model used
        action, embed = self.model.predict_action(idx, state)

        # Convert embedding from tensor to numpy
        temp = embed.cpu().numpy()

        # Set embeddings to current player
        self.players[idx].embeddings = np.add(self.players[idx].embeddings, temp)

        reward = 0
        mate_idx = -1

        # Fill the screen with green
        screen.fill((0, 178, 0))

        # Event loop
        for event in pygame.event.get():
            pass

        # Action left
        if action == 0:
            self.players[idx].change_player_xposition(-self.speed)
            reward = -2
        # Action right
        elif action == 1:
            self.players[idx].change_player_xposition(self.speed)
            reward = -2
        # Action: up
        elif action == 2:
            self.players[idx].change_player_yposition(-self.speed)
            reward = -2
        # Action: down
        elif action == 3:
            self.players[idx].change_player_yposition(self.speed)
            reward = -2
        # Action: up left (move north-west)
        elif action == 4:
            self.players[idx].change_player_yposition(-self.speed)
            self.players[idx].change_player_xposition(-self.speed)
            reward = -2
        # Action: up right (move north-east)
        elif action == 5:
            self.players[idx].change_player_yposition(-self.speed)
            self.players[idx].change_player_xposition(self.speed)
            reward = -2
        # Action: down left (move south-west)
        elif action == 6:
            self.players[idx].change_player_yposition(self.speed)
            self.players[idx].change_player_xposition(-self.speed)
            reward = -2
        # Action: down right (move south-east)
        elif action == 7:
            self.players[idx].change_player_yposition(self.speed)
            self.players[idx].change_player_xposition(self.speed)
            reward = -2
        # Action: stay
        elif action == 8:
            self.players[idx].energy -= 2
            reward = -50
            self.players[idx].update_history(action, self.time, reward)
        # Action: food ingestion
        elif action == 9:
            # Find food particles nearby
            food_particle = self.food_nearby(self.players[idx])

            # If food is in radius of current agent then
            if food_particle != -1:
                # Begin food ingestion
                self.players[idx].ingesting_food(food_particle, self.time)
                self.food_particles[food_particle] = 0
                reward = 5

                # Log the ingestion action
                self.players[idx].update_history(action, self.time, reward)
            # Otherwise punish the agent
            else:
                reward = -10

                # Log the failed ingestion action
                self.players[idx].update_history(action, self.time, reward)
        # Action: asexual reproduction
        elif action == 10:
            # If agent is not dead and potent and is of age to reproduce [10, 60]
            if (
                type(self.players[idx]) != int
                and not self.players[idx].is_impotent
                and (self.time - self.players[idx].born_at) in range(10, 61)
            ):
                reward = 4

                # Perform asexual reproduction and get offsprings
                offspring_players, offspring_ids = self.players[
                    idx
                ].asexual_reproduction(len(self.players), self.time)

                # Put the offsprings to player array
                for offspring_player in offspring_players:
                    self.players = np.append(self.players, offspring_player)

                # Add the number of agents in initial_population
                self.initial_population += len(offspring_players)

                # Add to logs the action asexual reproduction
                self.players[idx].update_history(
                    action,
                    self.time,
                    reward,
                    num_offspring=len(offspring_ids),
                    offspring_ids=offspring_ids,
                )

                # Kill the agent after asexual reproduction :)
                self.players[idx].write_data(self.time)
                self.players[idx] = 0
                self.killed = np.append(self.killed, idx)

                # Add agents to RL model
                self.model.add_agents(idx, len(offspring_players))
                self.model.kill_agent(idx)
            # If the above conditions don't meet then asexul reproduction fails
            else:
                reward = -10

                # Add to logs the failed action asexual reproduction
                self.players[idx].update_history(action, self.time, reward)
        # Action: sexual reproduction
        elif action == 11:
            # If agent is not mating right now
            if self.players[idx].mating_begin_time == 0:

                # Find appropriate mate
                mate_idx = self.search_mate(self.players[idx])

                # If mate is found then perform sexual reproduction
                if mate_idx != -1:

                    # Time at which mating begins
                    mating_begin_time = self.time

                    reward = 4

                    # Get offsprings after sexual reproduction
                    offspring_players, offspring_ids = self.players[
                        idx
                    ].sexual_reproduction(mating_begin_time, len(self.players), True)

                    # Perform mating for other parent too but don't generate offsprings
                    self.players[mate_idx].sexual_reproduction(
                        mating_begin_time, len(self.players)
                    )

                    # Add the offsprings to player array
                    for offspring_player in offspring_players:
                        self.players.append(offspring_player)

                    # Increase the total population
                    self.initial_population += len(offspring_players)

                    # Update logs for sexual reproduction action
                    self.players[idx].update_history(
                        action,
                        mating_begin_time,
                        reward,
                        num_offspring=len(offspring_ids),
                        offspring_ids=offspring_ids,
                        mate_id=mate_idx,
                    )

                    # Update logs for sexual reproduction action
                    self.players[mate_idx].update_history(
                        action,
                        mating_begin_time,
                        reward,
                        num_offspring=len(offspring_ids),
                        offspring_ids=offspring_ids,
                        mate_id=idx,
                    )

                    # Find out percentage of offsprings that will inherit dominant and recessive genes
                    dominant_percent = random.randint(0, 10) * 10
                    recessive_percent = 100 - dominant_percent
                    offsprings = len(self.players) - len(self.model.agents)
                    num_dominant = round(offsprings * (dominant_percent / 100))
                    num_recessive = offsprings - num_dominant

                    # Find dominant and recessive parent
                    dominant_idx = (
                        idx
                        if self.players[idx].energy > self.players[mate_idx].energy
                        else mate_idx
                    )
                    recessive_idx = idx if dominant_idx == mate_idx else mate_idx

                    # Add offsprings to RL model
                    self.model.add_agents(dominant_idx, num_dominant)
                    self.model.add_agents(recessive_idx, num_recessive)
                # Otherwise punish the agent trying to perform sexual reproduction
                else:
                    reward = -10

                    # Update logs for failed sexual reproduction action
                    self.players[idx].update_history(action, self.time, reward)
            # If agent is already mating then also punish the agent (bad manners)
            else:
                reward = -10

                # Update logs for failed sexual reproduction action
                self.players[idx].update_history(action, self.time, reward)
        elif action == 12:  # Fight
            if self.players[idx].fighting_with == -1:
                enemy = self.search_enemy(self.players[idx])
                if enemy != -1:
                    reward = -1
                    self.players[idx].fighting_with = enemy
                    self.players[enemy].fighting_with = idx
                    self.players[idx].energy -= 10
                    self.players[enemy].energy -= 10
                    self.players[idx].fighting_with = -1
                    self.players[enemy].fighting_with = -1
                    self.players[idx].update_history(
                        action, self.time, reward, fight_with=enemy
                    )
                    self.players[enemy].update_history(
                        action, self.time, reward, fight_with=idx
                    )
                else:
                    reward = -10
                    self.players[idx].update_history(action, self.time, reward)
            else:
                reward = -10
                self.players[idx].update_history(action, self.time, reward)

        if action <= 7:
            if self.players[idx].cannot_move == False:
                self.players[idx].update_history(action, self.time, reward)
            else:
                self.players[idx].update_history(action, self.time, reward)

        if self.food_regen_condition_is_met:  # FOOD REGEN PART always false for now
            print("Food regenerated!")
            self.food_particles, _ = self.refreshParticles()
            self.food_regen_condition_is_met = False

        # Show particles
        for j in range(len(self.food_particles)):
            if type(self.food_particles[j]) != int:
                self.food_particles[j].show_particle()

        now_time = self.time

        for i in range(len(self.players)):
            if i not in self.killed:
                if i == idx:
                    self.model.rewards[idx].append(reward)
                    self.model.scores[idx] += reward

                env_particles, env_particle_distance = self.food_in_env(self.players[i])
                self.players[i].food_near = env_particle_distance
                env_food_vector = self.getFoodVector(
                    self.players[i], env_particles
                )  # VECTOR FOOD

                env_players, env_player_distance = self.players_in_env(self.players[i])
                self.players[i].players_near = env_player_distance
                env_player_vector = self.getPlayerVector(
                    self.players[i], env_players
                )  # VECTOR player

                for index in range(
                    0, len(env_particles)
                ):  # change color of food in env_particles
                    local = env_particles[index]
                    if type(self.food_particles[local]) != int:
                        self.food_particles[local].show_close()

                if not env_players:
                    self.players[i].show_player()
                else:
                    self.players[i].show_close()

                if (
                    type(self.players[i]) != int
                    and self.players[i].ingesting_begin_time != 0
                    and self.time - self.players[i].ingesting_begin_time >= 1
                ):
                    self.players[i].food_ate += 1
                    self.players[i].ingesting_begin_time = 0
                    self.players[i].cannot_move = False

                if (
                    type(self.players[i]) != int
                    and self.players[i].mating_begin_time != 0
                    and self.time - self.players[i].mating_begin_time >= 2
                ):
                    self.players[i].mating_begin_time = 0
                    self.players[i].cannot_move = False

                if type(self.players[i]) != int and self.players[i].energy <= 0:
                    self.players[i].write_data(self.time)
                    self.players[i] = 0
                    self.killed = np.append(self.killed, i)
                    self.model.kill_agent(i)

                if (
                    type(self.players[i]) != int
                    and now_time - self.players[i].born_at >= self.max_age
                ):
                    self.players[i].write_data(self.time)
                    self.players[i] = 0
                    self.killed = np.append(self.killed, i)
                    self.model.kill_agent(i)

        if now_time % self.model_updates == 0:
            self.model.update_all_agents()

        # Update the window
        pygame.display.update()

    def update_time(self):
        self.time += 1

    def food_nearby(self, player):
        if type(player) == int:
            return -1
        for i, food_particle in enumerate(self.food_particles):
            if type(food_particle) != int:
                ed = (
                    (food_particle.particleX - (player.playerX + 16)) ** 2
                    + (food_particle.particleY - (player.playerY + 16)) ** 2
                ) ** (1 / 2)
                if ed <= 20:
                    return i
        return -1

    def food_in_env(self, player):
        env = []
        distances = []
        if type(player) == int:
            return -1
        for i, food_particle in enumerate(self.food_particles):
            if type(food_particle) != int:
                ed = (
                    (food_particle.particleX - (player.playerX)) ** 2
                    + (food_particle.particleY - (player.playerY)) ** 2
                ) ** (1 / 2)
                if ed <= 100:
                    env.append(i)
                    distances.append(ed)

        return env, distances

    def players_in_env(self, host):
        env = []
        distances = []
        if type(host) == int:
            return [], []
        for i, player in enumerate(self.players):
            if (type(player) != int) and (player != host):
                ed = (
                    (host.playerX - (player.playerX)) ** 2
                    + (host.playerY - (player.playerY)) ** 2
                ) ** (1 / 2)
                if ed <= 100:
                    env.append(i)
                    distances.append(ed)

        return env, distances

    def getPlayerVector(self, host, env_players):
        X = []
        Y = []
        sex = []
        if type(host) == int:
            return [], []
        gender_to_number = {"Female": 1, "Male": 2}
        for idx in env_players:
            if (type(self.players[idx]) != int) and (self.players[idx] != host):
                X.append((host.playerX - self.players[idx].playerX))
                Y.append((host.playerY - self.players[idx].playerY))
                sex.append(gender_to_number[self.players[idx].gender])

        if len(X) == 0:
            X.append(0)
            Y.append(0)
            sex.append(0)

        return list([X, Y, sex])

    def getFoodVector(self, player, env_particles):
        X = []
        Y = []
        if type(player) == int:
            return [], []
        for idx in env_particles:
            if type(self.food_particles[idx]) != int:
                X.append((player.playerX - self.food_particles[idx].particleX))
                Y.append((player.playerY - self.food_particles[idx].particleY))

        if len(X) == 0:
            X.append(0)
            Y.append(0)

        return list([X, Y])

    def search_mate(self, host):
        env = []
        if type(host) == int:
            return -1
        for i, player in enumerate(self.players):
            if (
                (type(player) != int)
                and (player != host)
                and (not player.is_impotent)
                and ((self.time - player.born_at) in range(10, 61))
                and (player.gender != host.gender)
            ):
                ed = (
                    ((host.playerX + 16) - (player.playerX + 16)) ** 2
                    + ((host.playerY + 16) - (player.playerY + 16)) ** 2
                ) ** (1 / 2)
                if ed <= 30:
                    env.append(i)

        return env[np.array(env).argsort()[0]] if len(env) > 0 else -1

    def search_enemy(self, host):
        env = []
        if type(host) == int:
            return -1
        for i, player in enumerate(self.players):
            if (
                (type(player) != int)
                and (player != host)
                and (player.fighting_with == -1)
            ):
                ed = (
                    ((host.playerX + 16) - (player.playerX + 16)) ** 2
                    + ((host.playerY + 16) - (player.playerY + 16)) ** 2
                ) ** (1 / 2)
                if ed <= 30:
                    env.append(i)

        return env[np.array(env).argsort()[0]] if len(env) > 0 else -1

    def check_particles(self):
        for my_particle in self.food_particles:
            for j, my_particle_inner in enumerate(self.food_particles):
                if (
                    my_particle_inner != my_particle
                    and type(my_particle) != int
                    and type(my_particle_inner) != int
                ):
                    ed = (
                        (my_particle.particleX - my_particle_inner.particleX) ** 2
                        + (my_particle.particleY - my_particle_inner.particleY) ** 2
                    ) ** (1 / 2)
                    if ed < 20:
                        self.food_particles[j] = 0

    def regenerate_species(self):
        for i in range(self.initial_population):
            self.players = np.append(self.players, Player(i, self.time))

    def refreshParticles(self):
        NEW_PARTICLES = random.randint(
            self.particles_to_regrow[0], self.particles_to_regrow[1]
        )
        for j in range(NEW_PARTICLES):
            self.food_particles = np.append(self.food_particles, Particle())
        self.food_particles = self.check_particles()
        self.number_of_particles += NEW_PARTICLES
