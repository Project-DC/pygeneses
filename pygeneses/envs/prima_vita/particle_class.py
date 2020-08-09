# Particle class representing food particles in prima vita environment

# Import required libraries
import pygame
import random
import math
import os

# Import global constants
from .global_constants import *


class Particle:
    """
    Food particle class for the species - Prima vita (First life)

    Data members
    ============
    particleImg (pygame.image)
        : Image representing particle in pygame environment
    particleX   (int)
        : x coordinate of food particle in 2D environment
    particleY   (int)
        : y coordinate of food particle in 2D environment
    """

    def __init__(self, mode="bot"):
        """
        Initializer for Particle class

        Params
        ======
        mode (str)
           : Mode in which to run environment (human/bot)
        """

        if(mode == "human"):
            self.particleImg = pygame.image.load(
                os.path.join(os.path.dirname(__file__), "images/food.png")
            )
        self.particleX = random.randint(10, SCREEN_WIDTH - 10)
        self.particleY = random.randint(10, SCREEN_HEIGHT - 10)

    def show_particle(self, screen):
        """
        Show a particle in pygame environment

        Params
        ======
        screen (pygame.display)
            : Pygame display
        """

        screen.blit(self.particleImg, (self.particleX, self.particleY))

    def show_close(self, screen):
        """
        Show a particle when close to an agent

        Params
        ======
        screen (pygame.display)
            : Pygame display
        """

        screen.blit(
            pygame.image.load(
                os.path.join(os.path.dirname(__file__), "images/food_near.png")
            ),
            (self.particleX, self.particleY),
        )
