import pygame
import random
import math

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
        
    def check_particles(self, arr):
        i = 0
        j = 1
        for i in range(len(arr)):
            for j in range(len(arr)):
                if(type(arr[j]) != int and type(arr[i] != int)):
                    x1 = arr[i].particleX
                    y1 = arr[i].particleY
                    x2 = arr[j].particleX
                    y2 = arr[j].particleY
                    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                    if distance < 11:
                        arr[j] = 0
                j += 1
            i += 1
        return arr                    