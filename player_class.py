import pygame
import time

class Player():

    def __init__(self, screen, img, width, height, screen_width, screen_height):
        self.screen = screen
        self.playerImg = pygame.image.load(img)
        self.playerX = 370
        self.playerY = 370
        self.playerX_change = 0
        self.playerY_change = 0
        self.PLAYER_WIDTH = width
        self.PLAYER_HEIGHT = height
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.is_killed = False
        self.born_at = time.time()

    def show_player(self):
        if(self.is_killed):
            self.screen.blit(pygame.image.load('dead-player.png'), (self.playerX, self.playerY))
        else:
            self.screen.blit(self.playerImg, (self.playerX, self.playerY))

    def change_player_position(self, x, y):
        self.playerX_change = x
        self.playerY_change = y

    def move_player(self, kill=False):
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
