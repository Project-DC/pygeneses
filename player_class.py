import pygame
import random
import time
import numpy as np

from global_constants import *

class Player():

    def __init__(self):
        self.playerImg = pygame.image.load('player.png')
        self.playerX = random.randint(32, SCREEN_WIDTH - 32)
        self.playerY = random.randint(32, SCREEN_HEIGHT - 32)
        self.playerX_change = 0
        self.playerY_change = 0
        self.PLAYER_WIDTH = 32
        self.PLAYER_HEIGHT = 32
        self.born_at = time.time()
        self.food_ate = 0
        self.gender = np.random.choice(['Male', 'Female'], p=[0.5, 0.5])
        self.cannot_move = False
        self.ingesting_begin_time = 0
        self.ingesting_particle_index = 0
        self.food_near = []
        self.players_near = []
        self.is_impotent = np.random.choice([True, False], p=[0.3, 0.7])
        self.mating_begin_time = 0
        self.fighting_with = -1
        self.energy = 200

    def change_player_xposition(self, x):
        self.playerX_change = x
        self.energy -= 5

    def change_player_yposition(self, y):
        self.playerY_change = y
        self.energy -= 5

    def asexual_reproduction(self):
        offspring_players = []
        for i in range(INITIAL_POPULATION):
            print("Born", (i+1), "/", INITIAL_POPULATION)
            offspring_players.append(Player())
        return offspring_players

    def sexual_reproduction(self, mating_begin_time, gen_offspring=False):
        self.cannot_move = True
        self.mating_begin_time = mating_begin_time
        self.energy -= 30
        if(gen_offspring):
            INITIAL_POPULATION = random.randint(2, 8)
            offspring_players = []
            for i in range(INITIAL_POPULATION):
                print("Born", (i+1), "/", INITIAL_POPULATION)
                offspring_players.append(Player())
            return offspring_players

    def ingesting_food(self, idx, time):
        self.cannot_move = True
        self.ingesting_begin_time = time
        self.ingesting_particle_index = idx
        self.energy += 25

    def show_player(self):
        screen.blit(self.playerImg, (self.playerX, self.playerY))

    def show_close(self):
        if(self.mating_begin_time != 0):
            screen.blit(pygame.image.load('player_mating.png'), (self.playerX, self.playerY))
        else:
            screen.blit(pygame.image.load("player_near.png"), (self.playerX, self.playerY))

    def move_player(self, kill=False):              #convert changes to be updated to actual new position
        if(not self.cannot_move):
            self.playerX += self.playerX_change
            self.playerY += self.playerY_change

            # Don't let the agent get out of the world
            if(self.playerX <= 0):
                self.playerX = 0
            elif(self.playerX >= (SCREEN_WIDTH - self.PLAYER_WIDTH)):
                self.playerX = (SCREEN_WIDTH - self.PLAYER_WIDTH)

            if(self.playerY <= 0):
                self.playerY = 0
            elif(self.playerY >= (SCREEN_HEIGHT - self.PLAYER_HEIGHT)):
                self.playerY = (SCREEN_HEIGHT - self.PLAYER_HEIGHT)

    def kill_player(self):
        self.is_killed = True
