import pygame
import random
import time
import numpy as np

class Player():

    def __init__(self, screen, img, width, height, screen_width, screen_height):
        self.screen = screen
        self.playerImg = pygame.image.load(img)
        self.playerX = random.randint(32, screen_width - 32)
        self.playerY = random.randint(32, screen_height - 32)
        self.playerX_change = 0
        self.playerY_change = 0
        self.PLAYER_WIDTH = width
        self.PLAYER_HEIGHT = height
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.is_killed = False
        self.born_at = time.time()
        self.food_ate = 0
        self.gender = np.random.choice(['male', 'female'])
        self.cannot_move = False
        self.ingesting_begin_time = 0
        self.ingesting_particle_index = 0
        self.food_near = []
        self.players_near = []
        # self.energy = 100

    def show_player(self):
        if(self.is_killed):
            self.screen.blit(pygame.image.load('dead-player.png'), (self.playerX, self.playerY))
        else:
            self.screen.blit(self.playerImg, (self.playerX, self.playerY))


    def show_close(self):
        if(self.is_killed):
            self.screen.blit(pygame.image.load('dead-player.png'), (self.playerX, self.playerY))
        else:
            self.screen.blit(pygame.image.load("player_near.png"), (self.playerX, self.playerY))



    def change_player_xposition(self, x):           #set change to be updated in x
        self.playerX_change = x

    def change_player_yposition(self, y):           #set change to be updated in y
        self.playerY_change = y

    def move_player(self, kill=False):              #convert changes to be updated to actual new position
        if(not self.cannot_move):
            self.playerX += self.playerX_change
            self.playerY += self.playerY_change

            # Don't let the agent get out of the world
            if(self.playerX <= 0):
                self.playerX = 0
            elif(self.playerX >= (self.SCREEN_WIDTH - self.PLAYER_WIDTH)):
                self.playerX = (self.SCREEN_WIDTH - self.PLAYER_WIDTH)

            if(self.playerY <= 0):
                self.playerY = 0
            elif(self.playerY >= (self.SCREEN_HEIGHT - self.PLAYER_HEIGHT)):
                self.playerY = (self.SCREEN_HEIGHT - self.PLAYER_HEIGHT)

    def kill_player(self):    
        self.is_killed = True

    def ingesting_food(self, idx, time):
        self.cannot_move = True
        self.ingesting_begin_time = time
        self.ingesting_particle_index = idx
    
            

