import pygame
import time
import random
import numpy as np

from player_class import Player
from particle_class import Particle
from helpers import *
from global_constants import *

# Initialise pygame
pygame.init()

# Title
pygame.display.set_caption("Chimichangas")

# Generate initial population
players = regenerate_species()

gender_ratio(players)

# Killed individuals
killed = []

# Allow regeneration of species
allow_regenerate = True
regenerate_times = 0

# Generate Food particle
my_particles = []
for j in range(NUMBER_OF_PARTICLES):
    my_particles.append(Particle())

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
                        players[i].change_player_xposition(-SPEED)
            if event.key == pygame.K_RIGHT:
                for i in range(INITIAL_POPULATION):
                    if(i not in killed):
                        players[i].change_player_xposition(SPEED)
            if event.key == pygame.K_UP:
                for i in range(INITIAL_POPULATION):
                    if(i not in killed):
                        players[i].change_player_yposition(-SPEED)
            if event.key == pygame.K_DOWN:
                for i in range(INITIAL_POPULATION):
                    if(i not in killed):
                        players[i].change_player_yposition(SPEED)
            if event.key == pygame.K_a:
                if(type(players[0]) != int and not players[0].is_impotent and type(players[0]) != int and (round(time.time() - players[0].born_at) in range(10, 61))):
                    offspring_players = players[0].asexual_reproduction()
                    for offspring_player in offspring_players:
                        players.append(offspring_player)
                    INITIAL_POPULATION += len(offspring_players)
                    players[0] = 0
                    killed.append(0)
            if event.key == pygame.K_b:
                mate_idx = search_mate(players[0],players)
                print(mate_idx)
                if(mate_idx != -1):
                    mating_begin_time = time.time()
                    offspring_players = players[0].sexual_reproduction(mating_begin_time, True)
                    players[mate_idx].sexual_reproduction(mating_begin_time)
                    for offspring_player in offspring_players:
                        players.append(offspring_player)
                    INITIAL_POPULATION += len(offspring_players)
            if event.key == pygame.K_c:
                food_particle = food_nearby(players[0], my_particles)
                print(food_particle)
                if(food_particle != -1):
                    players[i].ingesting_food(food_particle, time.time())
                    my_particles[food_particle] = 0
            if event.key == pygame.K_d:
                if(players[0].fighting_with == -1):
                    enemy = search_enemy(players[0], players)
                    if(enemy != -1):
                        print(players[0].energy, players[enemy].energy)
                        players[0].fighting_with = enemy
                        players[enemy].fighting_with = 0
                        players[0].energy -= 10
                        players[enemy].energy -= 10
                        players[0].fighting_with = -1
                        players[enemy].fighting_with = -1

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
    for j in range(NUMBER_OF_PARTICLES):
        if(type(my_particles[j]) != int):
            my_particles[j].show_particle()

    if(len(killed) == INITIAL_POPULATION and allow_regenerate):
        killed = []
        players = regenerate_species()
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

            env_particles,env_particle_distance = food_in_env(players[i], my_particles)
            players[i].food_near = env_particle_distance

            env_players, env_player_distance = players_in_env(players[i],players)
            players[i].players_near = env_player_distance

            for index in range(0, len(env_particles)):                #change color of food in env_particles
                local = env_particles[index]
                if type(my_particles[local]) != int:
                    my_particles[local].show_close()

            if not env_players:
                players[i].show_player()
            else:
                players[i].show_close()

            if(type(players[i]) != int and players[i].ingesting_begin_time != 0 and time.time() - players[i].ingesting_begin_time >= 1):
                players[i].food_ate += 1
                players[i].ingesting_begin_time = 0
                players[i].cannot_move = False

            if(type(players[i]) != int and players[i].mating_begin_time != 0 and time.time() - players[i].mating_begin_time >= 2):
                players[i].mating_begin_time = 0
                players[i].cannot_move = False

            if(players[i].energy <= 0):
                killed.append(i)

            if(now_time - players[i].born_at >= MAX_AGE):
                players[i].kill_player()
                players[i] = 0
                killed.append(i)

    # Update the window
    pygame.display.update()
