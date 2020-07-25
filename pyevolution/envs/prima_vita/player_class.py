import pygame
import random
import time
import numpy as np
import os

from .global_constants import *


class Player:
    def __init__(self, i, tob):
        self.index = i
        # Lists to Store history
        self.action_history = (
            []
        )  # [Action, Time, Reward, Energy, num_offspring, [offspring ids]]

        self.playerImg = pygame.image.load(
            os.path.join(os.path.dirname(__file__), "images/player.png")
        )
        self.playerX = random.randint(32, SCREEN_WIDTH - 32)
        self.playerY = random.randint(32, SCREEN_HEIGHT - 32)
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
        self.Parent = []

    def Add_Parent(self, id, tob):
        self.Parent.append([id, tob])

    def write_data(self):
        file_name = "Players_Data/" + str(self.born_at) + "-" + str(self.index) + ".npy"
        file = open(file_name, "wb")
        np.save(file, self.action_history)
        file.close()

    def update_history(
        self,
        action,
        time,
        reward,
        num_offspring=None,
        offspring_ids=None,
        mate_id=None,
        fight_with=None,
    ):

        if type(action) != int:
            if "Failed" in action:
                self.action_history.append(
                    [action, time, reward, self.energy, self.Parent]
                )
        elif action <= 9:
            self.action_history.append([action, time, reward, self.energy, self.Parent])
        elif action == 10:
            self.action_history.append(
                [
                    action,
                    time,
                    reward,
                    self.energy,
                    num_offspring,
                    offspring_ids,
                    self.Parent,
                ]
            )
        elif action == 11:
            self.action_history.append(
                [
                    action,
                    time,
                    reward,
                    self.energy,
                    num_offspring,
                    offspring_ids,
                    mate_id,
                    self.Parent,
                ]
            )
        elif action == 12:
            self.action_history.append(
                [action, time, reward, self.energy, fight_with, self.Parent]
            )

    def change_player_xposition(self, x):
        if not self.cannot_move:
            self.playerX += x

            if self.playerX <= 0:
                self.playerX = 0
            elif self.playerX >= (SCREEN_WIDTH - self.PLAYER_WIDTH):
                self.playerX = SCREEN_WIDTH - self.PLAYER_WIDTH

            self.energy -= 5

    def change_player_yposition(self, y):
        if not self.cannot_move:
            self.playerY += y

            if self.playerY <= 0:
                self.playerY = 0
            elif self.playerY >= (SCREEN_HEIGHT - self.PLAYER_HEIGHT):
                self.playerY = SCREEN_HEIGHT - self.PLAYER_HEIGHT

            self.energy -= 5

    def asexual_reproduction(self, lenPlayers, time_given):
        offspring_players = []
        num_offspring = random.randint(2, 8)
        offspring_ids = []
        self.energy -= 30
        for i in range(num_offspring):
            id_offspring = lenPlayers
            offspring_ids.append(id_offspring)
            lenPlayers = lenPlayers + 1
            offspring_players.append(Player(id_offspring, time_given))
            offspring_players[i].Add_Parent(self.index, self.born_at)
        return offspring_players, offspring_ids

    def sexual_reproduction(self, mating_begin_time, lenPlayers, gen_offspring=False):
        self.cannot_move = True
        self.mating_begin_time = mating_begin_time
        self.energy -= 30
        offspring_ids = []
        if gen_offspring:
            INITIAL_POPULATION = random.randint(2, 8)
            offspring_players = []
            for i in range(INITIAL_POPULATION):
                id_offspring = lenPlayers
                offspring_ids.append(id_offspring)
                lenPlayers = lenPlayers + 1
                offspring_players.append(Player(id_offspring, mating_begin_time))
                offspring_players[i].Add_Parent(self.index, self.born_at)
            return offspring_players, offspring_ids

    def ingesting_food(self, idx, time_given):
        self.cannot_move = True
        self.ingesting_begin_time = time_given
        self.ingesting_particle_index = idx
        self.energy += 25

    def show_player(self):
        screen.blit(self.playerImg, (self.playerX, self.playerY))

    def show_close(self):
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
