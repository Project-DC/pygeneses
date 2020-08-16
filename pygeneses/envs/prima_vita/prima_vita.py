# Primary class for the environment (prima vita - first life)

# Import required libraries
import os
import glob
import shutil
import pygame
import random
import numpy as np
import time
import importlib

# Import other classes
from .player_class import Player
from .particle_class import Particle
from .global_constants import *

# Dictionary to map from string to name of model
model_to_class = {"reinforce": importlib.import_module('pygeneses.models.reinforce.reinforce').ReinforceModel}


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
    initial_energy              (int)
       : Initial energy of agents
    state_size                  (int)
       : Size to which state is to be padded
    model                       (pygeneses.models)
       : Instance of pygeneses.models (RL algorithms)
    model_updates               (int)
       : Number of ticks after which model for all the population will be updated
    speed                       (int)
       : Speed with which agent moves in the environment (in pixels)
    max_age                     (int)
       : Maximum age that an agent can live up to
    current_population          (int)
       : Current population of alive people
    max_allowed_population      (int)
       : Maximum allowed population of alive people
    kill_type                   (str)
       : Killing method to use when population reaches a max cap
    mode                        (str)
       : Mode in which to run environment (human/bot)
    screen                      (pygame.display/None)
       : Pygame display
    """

    def __init__(
        self,
        initial_population=10,
        state_size=21,
        action_size=13,
        max_regenerations=0,
        model_updates=10,
        mode="bot",
        log_dir_info=None
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
        mode               (str)
            : Mode in which to run the environment, human - where pygame screen is displayed,
              bot - where pygame screen isn't created
        log_dir_info       (str)
            : To be appended to the log directory name for specifying the task
        """

        self.log_dir = "Players_Data_" + str(round(time.time())) if log_dir_info == None else "Players_Data_" + log_dir_info
        self.initial_population = initial_population
        self.state_size = state_size
        self.action_size = action_size
        self.time = -1

        self.regenerate_times = 0
        self.max_regenerations = max_regenerations
        self.allow_regenerate = True if max_regenerations > 0 else False

        self.food_regen_condition_is_met = False
        self.particles_to_regrow = (
            20,
            40,
        )

        self.initial_energy = 200
        self.state_size = 21

        self.players = np.array([])
        self.killed = np.array([])
        self.food_particles = np.array([])
        self.number_of_particles = random.randint(70, 80)

        self.model = "reinforce"
        self.model_updates = model_updates
        self.speed = 3
        self.max_age = 90
        self.current_population = 0
        self.max_allowed_population = 100
        self.kill_type = "difference"

        # If mode is human then pygame environment is shown
        self.mode = mode

        self.screen = None

        if os.path.exists(self.log_dir):
            shutil.rmtree(self.log_dir)

        os.mkdir(self.log_dir)
        os.mkdir(os.path.join(self.log_dir, "Embeddings"))

        # self.reset_logs()
        self.init()

    def init(self):
        """
        Initialise the environment

        Params
        ======
        model_name (str):
            Name of the model to be used to train agents
        """

        # Generate initial population
        self.time = 0
        self.regenerate_species()
        self.time -= 1

        # Put food particles in the environment
        for j in range(self.number_of_particles):
            self.food_particles = np.append(
                self.food_particles, Particle(mode=self.mode)
            )

        # Remove food particles which either overlap or are very close to another food particle
        self.check_particles()

        # Initialize the model, convert string to name of model and evaluate that to convert to class name
        self.model = model_to_class[self.model](
            self.initial_population, self.state_size, self.action_size
        )

        if self.mode == "human":
            # Initialise pygame
            pygame.init()

            # Title
            pygame.display.set_caption("Prima Vita")

            # Set screen
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

            # Fill the screen with green color
            self.screen.fill((0, 178, 0))

            # Update pygame screen
            pygame.display.update()

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

    def get_current_state(self, idx=None):
        """
        Return the current state of all the agents in the environment

        Params
        ======
        idx (int)
             : Index of current actor

        Returns
        =======
        initial_state (numpy.ndarray)
            : The state of all the agents in the environment, it contains vector (x, y) to
              all the food particles around a fixed radius of an agent, vector (x, y, sex) to
              all the agents in the same radius - these vectors are padded to match state_size - 1
              and the final entry in the state vector is the current energy of the agent
        """

        # If everyone is killed then return -1
        running = True
        if len(self.killed) == len(self.players):
            running = False

        # List containing states of all the agents
        initial_state = []

        # Loop through all of the players
        for i in range(len(self.players)):
            # If a player is not dead then
            if type(self.players[i]) != int:
                # Update only current actor and surrounding player's state
                if (idx == None) or (i in self.players[idx].players_near or i == idx):
                    # Get the food particles in environment
                    env_food_vector, env_particle_distance, env_particle_index = self.food_in_env(
                        self.players[i], get_idx=True
                    )

                    # Get the agents in environment
                    env_player_vector, env_player_distance, env_player_index = self.players_in_env(
                        self.players[i], get_idx=True
                    )

                    # Stack together the food and player vectors
                    temp_state = [env_food_vector, env_player_vector]

                    # Save this as state in current agent's object
                    self.players[i].states.append(
                        np.array(
                            [np.array(env_food_vector, dtype=object), np.array(env_player_vector, dtype=object)],
                            dtype=object,
                        )
                    )

                    # Update food_near and players_near for current player
                    self.players[i].food_near = env_particle_index
                    self.players[i].players_near = env_player_index

                    # Convert the food and player vectors stacked together into a single vector
                    temp_state = sum(temp_state, [])

                    # Pad to state_size - 1
                    temp_state = self.pad_state(np.array(temp_state), self.state_size - 1)

                    # Append energy to state
                    temp_state = np.append(temp_state, [self.players[i].energy])

                    # Append to initial_state
                    initial_state.append(temp_state)
                # Otherwise copy old state
                else:
                    # Convert state to 1D array
                    temp_state = np.hstack(self.players[i].states[-1])

                    # Pad state to state_size - 1
                    temp_state = self.pad_state(np.array(temp_state), self.state_size - 1)

                    # Append energy to state
                    temp_state = np.append(temp_state, [self.players[i].energy])

                    # Append to initial_state
                    initial_state.append(temp_state)
            else:
                # If agent is dead append an array with a single value - zero
                temp_state = np.append(np.zeros(20), [-100])
                initial_state.append(temp_state)

        # Return the state as numpy array
        return np.array(initial_state), running

    def run(self, stop_at=None):
        """
        Take an action, make changes to environment, return rewards

        Params
        ======
        stop_at (int)
            : Stop after generating approximately these many logs
        """

        # Get initial states and running condition
        states, running = self.get_current_state()

        # While agents are alive
        while running:
            # Update time tick
            self.update_time()

            # Check if max logs reached
            if stop_at != None and len(glob.glob(os.path.join(self.log_dir, "*.npy"))) >= stop_at:
                break

            # Loop through all the players
            for i in range(len(self.players)):
                if(type(self.players[i]) != int):
                    # Take an action for current index
                    self.take_action(i, states[i].astype(np.uint8))
                    idx = i if type(self.players[i]) != int else None

                    # Get updated state
                    states, running = self.get_current_state(idx)

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

        # If player is killed then he/she cannot take any action
        if(type(self.players[idx]) == int):
            return

        # Predict action and return embedding using RL model used
        action, embed = self.model.predict_action(idx, state)

        # Convert embedding from tensor to numpy
        temp = embed.cpu().numpy()

        # Set embeddings to current player
        self.players[idx].embeddings = np.add(self.players[idx].embeddings, temp)

        reward = 0
        mate_idx = -1

        if self.mode == "human":
            # Fill the screen with green
            self.screen.fill((0, 178, 0))

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
                self.players[idx].write_data(self.time, self.current_population)
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
                    ].sexual_reproduction(
                        mating_begin_time,
                        len(self.players),
                        True,
                        mate_id=mate_idx,
                        mate_tob=self.players[mate_idx].born_at,
                    )

                    # Perform mating for other parent too but don't generate offsprings
                    self.players[mate_idx].sexual_reproduction(
                        mating_begin_time, len(self.players)
                    )

                    # Add the offsprings to player array
                    for offspring_player in offspring_players:
                        np.append(self.players, offspring_player)

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
        # Action: fight
        elif action == 12:

            # If current agent is not fighting with anyone else
            if self.players[idx].fighting_with == -1:

                # Search enemy (closest agent, no personal grudges :) )
                enemy = self.search_enemy(self.players[idx])

                # If an agent is found in some fixed radius then
                if enemy != -1:

                    # Fighting isn't promoted, so a negative reward is given
                    reward = -1

                    # Fighting action
                    self.players[idx].fighting_with = enemy
                    self.players[enemy].fighting_with = idx
                    self.players[idx].energy -= 10
                    self.players[enemy].energy -= 10
                    self.players[idx].fighting_with = -1
                    self.players[enemy].fighting_with = -1

                    # Log fight action
                    self.players[idx].update_history(
                        action, self.time, reward, fight_with=enemy
                    )

                    # Log fight action
                    self.players[enemy].update_history(
                        action, self.time, reward, fight_with=idx
                    )
                # If there is no agent in agent
                else:
                    reward = -10

                    # Log failed fight action
                    self.players[idx].update_history(action, self.time, reward)
            # If the agent is already fighting with another agent (we do not promote mob fighting)
            else:
                reward = -10

                # Log failed fight action
                self.players[idx].update_history(action, self.time, reward)

        # Log all the movement actions
        if action <= 7:
            # Failed movement action
            if self.players[idx].cannot_move == False:
                self.players[idx].update_history(action, self.time, reward)
            # Successful movement action
            else:
                self.players[idx].update_history(action, self.time, reward)

        # If food regeneration condition is met then regenerate food particles
        if self.food_regen_condition_is_met:
            print("Food regenerated!")
            self.food_particles, _ = self.refresh_particles()
            self.food_regen_condition_is_met = False

        if self.mode == "human":
            # Show all particles
            for j in range(len(self.food_particles)):
                if type(self.food_particles[j]) != int:
                    self.food_particles[j].show_particle(self.screen)

        now_time = self.time

        # Loop through all the players
        for i in range(len(self.players)):
            # If agent is still alive
            if i not in self.killed:
                # Put rewards and scores into players object
                if i == idx:
                    self.model.rewards[idx].append(reward)
                    self.model.scores[idx] += reward

                if self.mode == "human":
                    # Find food particles in fixed radius
                    (
                        env_food_vector,
                        env_particle_distance,
                        env_particles,
                    ) = self.food_in_env(self.players[i], get_idx=True)

                    # Push the food particles near an agent to its object
                    self.players[i].food_near = env_particle_distance

                    # Find players in proximity
                    (
                        env_player_vector,
                        env_player_distance,
                        env_players,
                    ) = self.players_in_env(self.players[i], get_idx=True)

                    # Push the players in proximity to this agent to current agent's object
                    self.players[i].players_near = env_player_distance

                    # Change colors of food particles in proximity
                    for index in range(0, len(env_particles)):
                        local = env_particles[index]
                        if type(self.food_particles[local]) != int:
                            self.food_particles[local].show_close(self.screen)

                    # Change color of players in proximity
                    if not env_players:
                        self.players[i].show_player(self.screen)
                    else:
                        self.players[i].show_close(self.screen)

                # Check if ingestion action is complete or not (if ingesting)
                if (
                    type(self.players[i]) != int
                    and self.players[i].ingesting_begin_time != 0
                    and self.time - self.players[i].ingesting_begin_time >= 1
                ):
                    self.players[i].food_ate += 1
                    self.players[i].ingesting_begin_time = 0
                    self.players[i].cannot_move = False

                # Check if mating action is complete or not (if mating)
                if (
                    type(self.players[i]) != int
                    and self.players[i].mating_begin_time != 0
                    and self.time - self.players[i].mating_begin_time >= 2
                ):
                    self.players[i].mating_begin_time = 0
                    self.players[i].cannot_move = False

                # If the agent's energy is less than or equal to zero (0) kill the agent
                if type(self.players[i]) != int and self.players[i].energy <= 0:
                    self.players[i].write_data(self.time, self.current_population)
                    self.players[i] = 0
                    self.killed = np.append(self.killed, i)
                    self.model.kill_agent(i)

                # If the agent has reached maximum age then kill the agent
                if (
                    type(self.players[i]) != int
                    and now_time - self.players[i].born_at >= self.max_age
                ):
                    self.players[i].write_data(self.time, self.current_population)
                    self.players[i] = 0
                    self.killed = np.append(self.killed, i)
                    self.model.kill_agent(i)

        # Update NN for each agent every self.model_updates time steps
        if now_time % self.model_updates == 0:
            self.model.update_all_agents()

        if self.mode == "human":
            # Update the pygame window
            pygame.display.update()

        # Compute number of alive agents
        self.current_population = len(self.players) - len(self.killed)

        # If current population exceeds a max threshold then kill people randomly
        if self.kill_type != "" and self.current_population > self.max_allowed_population:
            # Compute number of extra agents
            extra_agent_count = (
                self.current_population - self.max_allowed_population
                if self.kill_type == "difference"
                else random.randint(
                    self.current_population - self.max_allowed_population,
                    self.current_population - 1,
                )
            )

            print(
                "Max population exceeded! Number of people to be killed: %d"
                % (extra_agent_count)
            )
            for _ in range(extra_agent_count):
                # Alive agents index
                alive_agents_index = list(
                    set(np.arange(len(self.players))) - set(self.killed)
                )
                idx = random.choice(alive_agents_index)
                self.current_population -= 1
                self.players[idx].write_data(self.time, self.current_population)
                self.players[idx] = 0
                self.killed = np.append(self.killed, idx)
                self.model.kill_agent(idx)

    def update_time(self):
        """
        Update time of the environment
        """

        self.time += 1

    def food_nearby(self, player):
        """
        Find nearby food

        Params
        ======
        player (pygeneses.envs.prima_vita.player_class.Player)
            : The player whose surroundings is to be checked for food particle

        Returns
        =======
        i/-1 (int)
            : The index of closest food particle if available or -1
        """

        # If player is dead then return -1
        if type(player) == int:
            return -1
        # Otherwise loop through all food particles
        for i, food_particle in enumerate(self.food_particles):
            # If food particle hasn't been consumed yet
            if type(food_particle) != int:
                # Compute euclidean distance between player and food particle
                ed = (
                    (food_particle.particleX - (player.playerX + 16)) ** 2
                    + (food_particle.particleY - (player.playerY + 16)) ** 2
                ) ** (1 / 2)

                # If distance is less than or equal to 20 then return index of that food particle
                if ed <= 20:
                    return i

        # If there isn't any food particle in range of the agent then return -1
        return -1

    def food_in_env(self, player, get_idx=False):
        """
        Return all food particles within a fixed radius of the agent

        Params
        ======
        player  (pygeneses.envs.prima_vita.player_class.Player)
            : The player whose surroundings is to be checked for food particle
        get_idx (bool)
            : Boolean to decide whether to return index or not

        Returns
        =======
        vec       (list)
            : The food vector
        distances (list)
            : The distances of food particles from the agent
        env       (list)
            : The index of food particles inside fixed radius of current agent
        """

        # Create empty lists
        env = []
        vec = []
        distances = []

        # If agent is dead return -1
        if type(player) == int:
            return -1

        # Otherwise loop through all food particles
        for i, food_particle in enumerate(self.food_particles):

            # If food particles isn't consumed yet
            if type(food_particle) != int:
                # Compute euclidean distance of food particle and current agent
                ed = (
                    (food_particle.particleX - (player.playerX)) ** 2
                    + (food_particle.particleY - (player.playerY)) ** 2
                ) ** (1 / 2)

                # If distance is less than or equal to 100 then push to lists
                if ed <= 100:
                    env.append(i)
                    vec.append(food_particle.particleX - player.playerX)
                    vec.append(food_particle.particleY - player.playerY)
                    distances.append(ed)

        if not get_idx:
            return vec, distances

        return vec, distances, env

    def players_in_env(self, host, get_idx=False):
        """
        Return all players within a fixed radius of the current player

        Params
        ======
        host    (pygeneses.envs.prima_vita.player_class.Player)
            : The player whose surroundings is to be checked for food particle
        get_idx (bool)
            : Boolean to decide whether to return index or not

        Returns
        =======
        vec       (list)
            : The player vector
        distances (list)
            : The distances of food particles from the agent
        env       (list)
            : The index of players inside fixed radius of current player
        """

        # Create empty lists
        env = []
        vec = []
        distances = []

        # Mapping gender to number
        gender_to_number = {"Female": 1, "Male": 2}

        # If player is dead then return -1
        if type(host) == int:
            return [], []

        # Otherwise loop through all players
        for i, player in enumerate(self.players):
            # If the player is not dead and is not the host itself then
            if (type(player) != int) and (player != host):
                # Compute euclidean distance between two agents
                ed = (
                    (host.playerX - (player.playerX)) ** 2
                    + (host.playerY - (player.playerY)) ** 2
                ) ** (1 / 2)

                # If distance is less than equal to 100 then push to list
                if ed <= 100:
                    env.append(i)
                    vec.append(host.playerX - player.playerX)
                    vec.append(host.playerY - player.playerY)
                    vec.append(gender_to_number[player.gender])
                    distances.append(ed)

        if not get_idx:
            return vec, distances

        return vec, distances, env

    def search_mate(self, host):
        """
        Search for a mate (for sexual reproduction)

        Params
        ======
        host (pygeneses.envs.prima_vita.player_class.Player)
            : The player whose surroundings is to be checked for food particle

        Returns
        =======
        env/-1 (int)
            : Closest agent in proximity to current agent (to mate with)
        """

        env = []

        # If agent is dead then return -1
        if type(host) == int:
            return -1

        # Otherwise loop through all players
        for i, player in enumerate(self.players):
            # If player isn't dead and isn't the host itself and is not impotent
            # and is of appropriate age of reproduction and gender is not opposite of host then
            if (
                (type(player) != int)
                and (player != host)
                and (not player.is_impotent)
                and ((self.time - player.born_at) in range(10, 61))
                and (player.gender != host.gender)
            ):
                # Compute euclidean distance between player and host
                ed = (
                    ((host.playerX + 16) - (player.playerX + 16)) ** 2
                    + ((host.playerY + 16) - (player.playerY + 16)) ** 2
                ) ** (1 / 2)

                # If distance is less than or equal to 30 then append it to env list
                if ed <= 30:
                    env.append(i)

        # Return the closes agent, if there is one else return -1
        return env[np.array(env).argsort()[0]] if len(env) > 0 else -1

    def search_enemy(self, host):
        """
        Search for a player to fight with

        Params
        ======
        host (pygeneses.envs.prima_vita.player_class.Player)
            : The player whose surroundings is to be checked for food particle

        Returns
        =======
        env/-1 (int)
            : Closest agent in proximity to current agent (to fight with)
        """

        env = []

        # If agent is dead then return -1
        if type(host) == int:
            return -1

        # Otherwise loop through all players
        for i, player in enumerate(self.players):
            # If player isn't dead and isn't the host itself and isn't fighting with anyone else
            if (
                (type(player) != int)
                and (player != host)
                and (player.fighting_with == -1)
            ):
                # Compute euclidean distance between player and host
                ed = (
                    ((host.playerX + 16) - (player.playerX + 16)) ** 2
                    + ((host.playerY + 16) - (player.playerY + 16)) ** 2
                ) ** (1 / 2)

                # If distance is less than or equal to 30 then append it to env list
                if ed <= 30:
                    env.append(i)

        # Return the closes agent, if there is one else return -1
        return env[np.array(env).argsort()[0]] if len(env) > 0 else -1

    def check_particles(self):
        """
        Remove particles that are too close to others
        """

        # Loop through all food particles
        for my_particle in self.food_particles:
            # Again loop through all food particles
            for j, my_particle_inner in enumerate(self.food_particles):
                # If food particle isn't consumed then
                if (
                    my_particle_inner != my_particle
                    and type(my_particle) != int
                    and type(my_particle_inner) != int
                ):
                    # Compute euclidean distance
                    ed = (
                        (my_particle.particleX - my_particle_inner.particleX) ** 2
                        + (my_particle.particleY - my_particle_inner.particleY) ** 2
                    ) ** (1 / 2)

                    # If distance is less than 20 then delete the food particle
                    if ed < 20:
                        self.food_particles[j] = 0

    def regenerate_species(self):
        """
        Generate/Regenerate species based on certain initial population count given
        """

        # Loop till iterator reaches initial population count
        for i in range(self.initial_population):
            # Generate a new player and add it to player pool
            self.players = np.append(self.players, Player(i, self.log_dir, self.time, self.initial_energy, mode=self.mode))

    def refresh_particles(self):
        """
        Replenish food particles based on certain conditions
        """

        # Choose the number of particles to be generated
        NEW_PARTICLES = random.randint(
            self.particles_to_regrow[0], self.particles_to_regrow[1]
        )

        # Loop through all new particles
        for j in range(NEW_PARTICLES):
            # Generate food particle and append to food particles pool
            self.food_particles = np.append(
                self.food_particles, Particle(mode=self.mode)
            )

        # Delete food particles which are too close to others
        self.food_particles = self.check_particles()

        # Update the total number of particles
        self.number_of_particles += NEW_PARTICLES
