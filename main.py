import pygame
import time
import random

from player_class import Player
from particle_class import Particle
from helpers import food_ingesting

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
INITIAL_POPULATION = 2
players = []
i = 0
while(i < INITIAL_POPULATION):
    print("Born", (i+1), "/", INITIAL_POPULATION)
    player = Player(screen, 'player.png', 32, 32, SCREEN_WIDTH, SCREEN_HEIGHT)
    players.append(player)
    ## TODO: Remove this time.sleep when testing is done
    time.sleep(3)
    i += 1

killed = []

# Speed
speed = 3

# Generate Food particle
number_of_particles = random.randint(50, 100)
my_particles = []
j = 0
while(j < number_of_particles):
    particle = Particle(screen, 'food.png', 10, 10, SCREEN_WIDTH, SCREEN_HEIGHT)
    my_particles.append(particle)
    j += 1


my_particles = Particle.check_particles(my_particles)

# Game loop
running = True
while running:

    # First the screen is filled so that every thing is above the screen
    screen.fill((0, 178, 0))

    for event in pygame.event.get():

        #To check whether the window is quitted or not
        if event.type == pygame.QUIT:
            with open('info-run-alive-' + str(round(time.time(), 0)) + '.txt', 'w') as file:
                for i, player in enumerate(players):
                    if(type(player) != int):
                        file.write("Chimichanga #" + str(i+1) + " ate " + str(player.food_ate) + " food particles.\n")
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
        if(type(my_particles[j]) != int):
            my_particles[j].show_particle()

    now_time = time.time()
    for i in range(INITIAL_POPULATION):
        if(i not in killed):
            # Move the player
            players[i].move_player()

            # Show the player
            players[i].show_player()

            if(now_time - players[i].born_at >= 30):
                players[i].kill_player()
                with open('info-run-dead-' + str(i+1) + '.txt', 'w') as file:
                    file.write("Chimichanga #" + str(i+1) + " ate " + str(players[i].food_ate) + " food particles.\n")
                players[i] = 0
                killed.append(i)

            food_particle = food_ingesting(players[i], my_particles)
            if(food_particle != -1):
                players[i].ingesting_food(food_particle, time.time())
                my_particles[food_particle] = 0

            if(type(players[i]) != int and players[i].ingesting_begin_time != 0 and time.time() - players[i].ingesting_begin_time >= 2):
                players[i].food_ate += 1
                print(i, players[i].food_ate)
                players[i].ingesting_begin_time = 0
                players[i].cannot_move = False

    # Update the window
    pygame.display.update()
