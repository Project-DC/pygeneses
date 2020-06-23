# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 10:45:47 2020

@author: dhairya
"""

import pygame

#initialise pygame
pygame.init()

#create a screen
screen = pygame.display.set_mode((800, 800))

#Title
pygame.display.set_caption("Chimichangas")

#player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 370

def player():
    screen.blit(playerImg, (playerX, playerY))

#Game loop
running = True
while running:
    
    #First the screen is filled so that every thing is above the screen
    screen.fill((255, 255, 255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
    #Call the player
    player()
    
    #Update the window
    pygame.display.update()