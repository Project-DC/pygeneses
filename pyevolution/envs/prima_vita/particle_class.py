import pygame
import random
import math
import os

from .global_constants import *


class Particle:
    def __init__(self):
        self.particleImg = pygame.image.load(
            os.path.join(os.path.dirname(__file__), "images/food.png")
        )
        self.particleX = random.randint(10, SCREEN_WIDTH - 10)
        self.particleY = random.randint(10, SCREEN_HEIGHT - 10)

    def show_particle(self):
        screen.blit(self.particleImg, (self.particleX, self.particleY))

    def show_close(self):  # testing function
        screen.blit(
            pygame.image.load(
                os.path.join(os.path.dirname(__file__), "images/food_near.png")
            ),
            (self.particleX, self.particleY),
        )
