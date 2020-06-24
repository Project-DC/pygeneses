import pygame
import time
import random

from player_class import Player
from particle_class import Particle
from helpers import food_ingesting, regenerate_species, check_particles

# Initialise pygame
pygame.init()

# Size constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

# Create a screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Title
pygame.display.set_caption("Chimichangas")

# Generate initial population
INITIAL_POPULATION = 2
players = regenerate_species(INITIAL_POPULATION, screen, SCREEN_WIDTH, SCREEN_HEIGHT)

# Killed individuals
killed = []

# Allow regeneration of species
allow_regenerate = True
regenerate_times = 0
MAX_REGENERATIONS = 3

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

my_particles = check_particles(my_particles)

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
            if event.key == pygame.K_a:
                print(players[0].is_impotent)
                if(not players[0].is_impotent and type(players[0]) != int and (round(time.time() - players[0].born_at) in range(10, 61))):
                    print("Hello")
                    offspring_players = players[0].asexual_reproduction(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
                    for offspring_player in offspring_players:
                        players.append(offspring_player)
                    INITIAL_POPULATION += len(offspring_players)
                    players[0] = 0
                    killed.append(0)

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

    if(len(killed) == INITIAL_POPULATION and allow_regenerate):
        killed = []
        players = regenerate_species(INITIAL_POPULATION, screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        regenerate_times += 1
    elif(len(killed) == INITIAL_POPULATION and not allow_regenerate):
        running = False

    if(regenerate_times == MAX_REGENERATIONS):
        allow_regenerate = False

    now_time = time.time()
    for i in range(INITIAL_POPULATION):
        if(i not in killed):
            # Move the player
            players[i].move_player()

            # Show the player
            players[i].show_player()

            if(now_time - players[i].born_at >= 90):
                players[i].kill_player()
                players[i] = 0
                killed.append(i)

            food_particle = food_ingesting(players[i], my_particles)
            if(food_particle != -1):
                players[i].ingesting_food(food_particle, time.time())
                my_particles[food_particle] = 0

            if(type(players[i]) != int and players[i].ingesting_begin_time != 0 and time.time() - players[i].ingesting_begin_time >= 2):
                players[i].food_ate += 1
                players[i].ingesting_begin_time = 0
                players[i].cannot_move = False

    # Update the window
    pygame.display.update()
