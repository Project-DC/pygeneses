import pygame
import time
import random

from player_class import Player

from particle_class import Particle

# Initialise pygame
pygame.init()

# Size constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

# Create a screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Title
pygame.display.set_caption("Chimichangas")

# Player
INITIAL_POPULATION = 10
players = []
i = 0
while(i < INITIAL_POPULATION):
    print("Born", (i+1), "/", INITIAL_POPULATION)
    player = Player(screen, 'player.png', 32, 32, SCREEN_WIDTH, SCREEN_HEIGHT)
    players.append(player)
    ## TODO: Remove this time.sleep when testing is done
    time.sleep(1)
    i += 1

print(len(players))

killed = []

# Speed
speed = 1

# Generate Food particle
number_of_particles = random.randint(50, 100)
my_particles = []
j = 0
while(j < number_of_particles):
    particle = Particle(screen, 'food.png', 10, 10, SCREEN_WIDTH, SCREEN_HEIGHT)
    my_particles.append(particle)
    j += 1

# Game loop
running = True
while running:
    
    # First the screen is filled so that every thing is above the screen
    screen.fill((0, 178, 0))

    for event in pygame.event.get():

        #To check whether the window is quitted or not
        if event.type == pygame.QUIT:
            running = False

        # If key is pressed, check whether it's right, left, up or down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                for i in range(INITIAL_POPULATION):
                    if(i not in killed):
                        players[i].change_player_xposition(-speed)
            if event.key == pygame.K_RIGHT:
                for i in range(INITIAL_POPULATION):
                    if(i not in killed):
                        players[i].change_player_xposition(speed)
            if event.key == pygame.K_UP:
                for i in range(INITIAL_POPULATION):
                    if(i not in killed):
                        players[i].change_player_yposition(-speed)
            if event.key == pygame.K_DOWN:
                for i in range(INITIAL_POPULATION):
                    if(i not in killed):
                        players[i].change_player_yposition(speed)
                        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                for i in range(INITIAL_POPULATION):
                    if(i not in killed):
                        players[i].change_player_xposition(0)
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                for i in range(INITIAL_POPULATION):
                    if(i not in killed):
                        players[i].change_player_yposition(0)

    # Show particles
    for j in range(number_of_particles):
        my_particles[j].show_particle()
    
    now_time = time.time()
    for i in range(INITIAL_POPULATION):
        if(i not in killed):
            # Move the player
            players[i].move_player()

            # Show the player
            players[i].show_player()

            if(now_time - players[i].born_at >= 15):
                players[i].kill_player()
                players[i] = 0
                killed.append(i)

    # Update the window
    pygame.display.update()
