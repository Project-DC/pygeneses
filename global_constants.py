import pygame
import random

# Size constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

INITIAL_POPULATION = 2

MAX_REGENERATIONS = 3

MAX_AGE = 90

# Speed
SPEED = 3

# Create a screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

NUMBER_OF_PARTICLES = random.randint(30, 50)
