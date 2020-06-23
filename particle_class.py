import pygame
import random


class Particle():
    
    def __init__(self, screen, img, width, height, screen_width, screen_height):
        self.screen = screen
        self.particleImg = pygame.image.load(img)
        self.particleX = random.randint(10, screen_width - 10)
        self.particleY = random.randint(10, screen_height - 10)
        self.PARTICLE_WIDTH = width
        self.PARTICLE_HEIGHT = height
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
    
    
    def show_particle(self):
        self.screen.blit(self.particleImg, (self.particleX, self.particleY))