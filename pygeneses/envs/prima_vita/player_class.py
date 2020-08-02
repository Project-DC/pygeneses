# Player class representing an agent in prima vita environment

# Import required libraries
import pygame
import random
import time
import numpy as np
import os

# Import global constants
from .global_constants import *


class Player:
    """
    Player class for the species - Prima vita (First life)

    Data members
    ============
    index                    (int)
        : Index of current player among all players
    action_history           (list)
        : List storing logs of all actions (both successful and failed), initial (x, y) coordinates
          and parent id(s)
    playerImg                (pygame.image)
        : Image representing a player in pygame environment
    playerX                  (int)
        : x coordinate or player in 2D environment
    playerY                  (int)
        : y coordinate or player in 2D environment
    PLAYER_WIDTH             (int)
        : Width of player image
    PLAYER_HEIGHT            (int)
        : Height of player image
    born_at                  (int)
        : Time of birth of the player
    food_ate                 (int)
        : Number of food particles consumed
    gender                   (str)
        : Gender of agent (required for mating)
    cannot_move              (bool)
        : Can the agent move or not?
    ingesting_begin_time     (int)
        : The time (in ticks) at which player begins ingesting food (this action takes 1 tick to complete)
    ingesting_particle_index (int)
        : Index of food particle that the agent is ingesting
    food_near                (list)
        : Information about all the food particles nearby
    players_near             (list)
        : Information about all the players nearby
    is_impotent              (bool)
        : Is the agent impotent or potent (impotency leads to failure in reproduction)
    mating_begin_time        (int)
        : Time (in ticks) at which mating began (this action takes 2 ticks to complete)
    fight_with               (int)
        : Id of the player the agent is currently fighting with
    energy                   (int)
        : Energy of the player (when energy is consumed player dies)
    embeddings               (numpy.ndarray)
        : Embeddings of the player (fetched from NN)
    states                   (list)
        : States that the player experiences at each time step
    """

    def __init__(self, i, tob, x=None, y=None):
        """
        Initializer for Player class

        Params
        ======
        i   (int)
            : Id of the player out of all players
        tob (int)
            : Time of birth of the agent (fetched from environment)
        x   (int)
            : Initial x coordinate of the agent (optional)
        y   (int)
            : Initial y coordinate of the agent (optional)
        """

        self.index = i
        self.action_history = (
            []
        )  # [Action, Time, Reward, Energy, num_offspring, [offspring ids]]

        self.playerImg = pygame.image.load(
            os.path.join(os.path.dirname(__file__), "images/player.png")
        )
        self.playerX = x if x is not None else random.randint(32, SCREEN_WIDTH - 32)
        self.playerY = y if y is not None else random.randint(32, SCREEN_HEIGHT - 32)
        self.PLAYER_WIDTH = 32
        self.PLAYER_HEIGHT = 32
        self.born_at = tob
        self.food_ate = 0
        self.gender = np.random.choice(["Male", "Female"], p=[0.5, 0.5])
        self.cannot_move = False
        self.ingesting_begin_time = 0
        self.ingesting_particle_index = 0
        self.food_near = []
        self.players_near = []
        self.is_impotent = np.random.choice([True, False], p=[0.3, 0.7])
        self.mating_begin_time = 0
        self.fighting_with = -1
        self.energy = 200

        self.embeddings = np.array([0])
        self.states = []

        # Add the initial x, y coordinates as first entry in logs
        self.action_history.append([self.playerX, self.playerY])

    def Add_Parent(self, id, tob, mate_id = -1, mate_tob = -1):
        """
        Add parent information to logs
        """
        if mate_id == -1:
            self.action_history.append(np.array([id, tob]))
        else:
            self.action_history.append(np.array([[id, tob],[mate_id, mate_tob]]))


    def write_data(self, time):
        """
        Write logs to npy file when player dies

        Params
        ======
        time (int)
            : Time (in ticks) of death of the player
        """

        # Show in front end API
        print(f"RIP {self.born_at}-{self.index}")

        # Form filename to save logs into
        file_name = str(self.born_at) + "-" + str(self.index)

        # Open file at location to dump logs
        file = open("Players_Data/" + file_name + ".npy", "wb")
        np.save(file, np.array(self.action_history))
        file.close()

        # Average embeddings over entire life
        self.embeddings = self.embeddings / (time - self.born_at)

        # Open file at location to dump embeddings
        file = open("Players_Data/Embeddings/" + file_name + ".npy", "wb")
        np.save(file, self.embeddings)
        file.close()

    def update_history(
        self,
        action,
        time,
        reward,
        num_offspring=-1,
        offspring_ids=-1,
        mate_id=-1,
        fight_with=-1,
    ):
        """
        Update logs of player according to current action

        Params
        ======
        action        (int)
            : Action chosen by the player
        time          (int)
            : Time at which action is taken
        reward        (int)
            : Reward recieved for taking the action
        num_offspring (int)
            : Number of offsprings generated (optional)
        offspring_ids (list)
            : Ids of offsprings (optional)
        mate_id       (int)
            : Id of player with which current player mated (optional)
        fight_with    (int)
            : Id of player with which current agent fought (optional)
        """

        # If action is failed then denote it in logs as negative action
        # (eg: -10 for failed asexual reproduction)
        if type(action) != int:
            if "Failed" in action:
                self.action_history.append(
                    np.array(
                        [
                            -action,
                            time,
                            reward,
                            self.energy,
                            self.playerX,
                            self.playerY,
                            self.states[-1],
                        ]
                    )
                )

        # If action number is less than or equal to 9 (i.e. movement in 8 directions, stay or ingestion) then
        elif action <= 9:
            self.action_history.append(
                np.array(
                    [
                        action,
                        time,
                        reward,
                        self.energy,
                        self.playerX,
                        self.playerY,
                        self.states[-1],
                    ]
                )
            )
        # If action number is 10 (i.e. asexual reproduction)
        elif action == 10:
            self.action_history.append(
                np.array(
                    [
                        action,
                        time,
                        reward,
                        self.energy,
                        num_offspring,
                        np.array(offspring_ids),
                        self.playerX,
                        self.playerY,
                        self.states[-1],
                    ]
                )
            )
        # If action number is 11 (i.e. sexual reproduction)
        elif action == 11:
            self.action_history.append(
                np.array(
                    [
                        action,
                        time,
                        reward,
                        self.energy,
                        num_offspring,
                        np.array(offspring_ids),
                        mate_id,
                        self.playerX,
                        self.playerY,
                        self.states[-1],
                    ]
                )
            )
        # If action number is 12 (i.e. fight)
        elif action == 12:
            self.action_history.append(
                np.array(
                    [
                        action,
                        time,
                        reward,
                        self.energy,
                        fight_with,
                        self.playerX,
                        self.playerY,
                        self.states[-1],
                    ]
                )
            )

    def change_player_xposition(self, x):
        """
        Update player's x coordinate

        Params
        ======
        x (int)
            : Add to player's current x coordinate the value x (either positive or negative)
        """

        # If agent can move
        if not self.cannot_move:
            # Update current x coordinate by adding new x
            self.playerX += x

            # If x coordinate goes out of bounds of the pygame screen then adjust it
            if self.playerX <= 0:
                self.playerX = 0
            elif self.playerX >= (SCREEN_WIDTH - self.PLAYER_WIDTH):
                self.playerX = SCREEN_WIDTH - self.PLAYER_WIDTH

            # Reduce energy by 5 for movement
            self.energy -= 5

    def change_player_yposition(self, y):
        """
        Update player's y coordinate

        Params
        ======
        y (int)
            : Add to player's current y coordinate the value x (either positive or negative)
        """

        # If agent can move
        if not self.cannot_move:
            # Update current y coordinate by adding new y
            self.playerY += y

            # If y coordinate goes out of bounds of the pygame screen then adjust it
            if self.playerY <= 0:
                self.playerY = 0
            elif self.playerY >= (SCREEN_HEIGHT - self.PLAYER_HEIGHT):
                self.playerY = SCREEN_HEIGHT - self.PLAYER_HEIGHT

            # Reduce energy by 5 for movement
            self.energy -= 5

    def asexual_reproduction(self, lenPlayers, time_given):
        """
        Perform asexual reproduction action

        Params
        ======
        lenPlayers (int)
            : Number of players currently in environment
        time_given (int)
            : Current time (taken from environment)

        Returns
        =======
            offspring_players (list)
                : Player class' object for offsprings
            offspring_ids     (list)
                : Unique ids for offsprings
        """

        # Create empty lists
        offspring_players = []
        offspring_ids = []

        # Select random number of offsprings in range [2, 8]
        num_offspring = random.randint(2, 8)

        # Reduce energy by 30 for asexual reproduction
        self.energy -= 30

        # Loop through offspring count
        for i in range(num_offspring):
            # Create offspring ids and append it to list
            id_offspring = lenPlayers
            offspring_ids.append(id_offspring)

            lenPlayers = lenPlayers + 1

            # Create new Player objects and add as offsprings
            offspring_players.append(Player(id_offspring, time_given))

            # Add current player as parent to all offspring objects
            offspring_players[i].Add_Parent(self.index, self.born_at)

        return offspring_players, offspring_ids

    def sexual_reproduction(self, mating_begin_time, lenPlayers, gen_offspring=False, mate_id = -1, mate_tob = -1):
        """
        Perform sexual reproduction action

        Params
        ======
        mating_begin_time (int)
            : The time at which mating process begins (takes 2 ticks of time to complete)
        lenPlayers        (int)
            : Number of players currently in environment
        gen_offspring     (bool)
            : Whether to generate
        mate_id           (int)
            : Id of the mate
        mate_tob          (int)
            : Time of birth of the mate
        Returns
        =======
            offspring_players (list)
                : Player class' object for offsprings
            offspring_ids     (list)
                : Unique ids for offsprings
        """

        # Stop the agent from moving
        self.cannot_move = True

        # Set mating beginning time (in ticks)
        self.mating_begin_time = mating_begin_time

        # Reduce energy by 30 for sexual reproduction action
        self.energy -= 30

        # Create empty lists
        offspring_ids = []
        offspring_players = []

        # If gen_offspring is true then parent will give birth (only one parent gives birth)
        if gen_offspring:
            # Select randomly number of offsprings in range [2, 8]
            INITIAL_POPULATION = random.randint(2, 8)

            # Loop through offspring count
            for i in range(INITIAL_POPULATION):
                # Create offspring ids and append it to list
                id_offspring = lenPlayers
                offspring_ids.append(id_offspring)
                lenPlayers = lenPlayers + 1

                # Create new Player objects and add as offsprings
                offspring_players.append(Player(id_offspring, mating_begin_time))

                # Add current player as parent to all offspring objects
                offspring_players[i].Add_Parent(self.index, self.born_at, mate_id, mate_tob)

            return offspring_players, offspring_ids

    def ingesting_food(self, idx, time_given):
        """
        Perform food ingestion action

        Params
        ======
        idx        (int)
            : Id of the food particle being consumed
        time_given (int)
            : Time at which food ingestion started
        """

        # Player cannot move during this time
        self.cannot_move = True

        # Set ingestion time and food particle id
        self.ingesting_begin_time = time_given
        self.ingesting_particle_index = idx

        # Add energy of 25 points for ingestion action
        self.energy += 25

    def show_player(self):
        """
        Show the player in pygame environment
        """

        screen.blit(self.playerImg, (self.playerX, self.playerY))

    def show_close(self):
        """
        Show the player in pygame environment when it is close to another or is mating with another
        """

        if self.mating_begin_time != 0:
            screen.blit(
                pygame.image.load(
                    os.path.join(os.path.dirname(__file__), "images/player_mating.png")
                ),
                (self.playerX, self.playerY),
            )
        else:
            screen.blit(
                pygame.image.load(
                    os.path.join(os.path.dirname(__file__), "images/player_near.png")
                ),
                (self.playerX, self.playerY),
            )
