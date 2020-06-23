import pygame
import random


class Particle():
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (255, 255, 0)
        self.thickness = 1

    def display(self, screen):
        self.screen = screen
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size, self.thickness)