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

screen.fill((0, 178, 0))

for event in pygame.event.get():
    pass

pygame.display.update()

def actions(idx, action):
    global INITIAL_POPULATION

    reward = 0

    screen.fill((0, 178, 0))

    for event in pygame.event.get():
        pass

    print("action ", action)
    if action == 0: # Left
        players[idx].change_player_xposition(-SPEED)
        reward = -2
    elif action == 1: # Right
        players[idx].change_player_xposition(SPEED)
        reward = -2
    elif action == 2: # Up
        players[idx].change_player_yposition(-SPEED)
        reward = -2
    elif action == 3: # Down
        players[idx].change_player_yposition(SPEED)
        reward = -2
    elif action == 4: # Up Left
        players[idx].change_player_yposition(-SPEED)
        players[idx].change_player_xposition(-SPEED)
        reward = -2
    elif action == 5: # Up Right
        players[idx].change_player_yposition(-SPEED)
        players[idx].change_player_xposition(SPEED)
        reward = -2
    elif action == 6: # Down Left
        players[idx].change_player_yposition(SPEED)
        players[idx].change_player_xposition(-SPEED)
        reward = -2
    elif action == 7: # Down Right
        players[idx].change_player_yposition(SPEED)
        players[idx].change_player_xposition(SPEED)
        reward = -2
    elif action == 8: # Stay
        players[idx].energy -= 2
        reward = -5
    elif action == 9: # Eat
        food_particle = food_nearby(players[idx], my_particles)
        if(food_particle != -1):
            players[idx].ingesting_food(food_particle, time.time())
            my_particles[food_particle] = 0
    elif action == 10:   # Mate Asexual
        if(type(players[idx]) != int and not players[idx].is_impotent and (round(time.time() - players[idx].born_at) in range(10, 61))):
            offspring_players = players[idx].asexual_reproduction()
            for offspring_player in offspring_players:
                players.append(offspring_player)
            INITIAL_POPULATION += len(offspring_players)
            players[idx] = 0
            killed.append(idx)
    elif action == 11:     #Mate Sexual
        mate_idx = search_mate(players[idx],players)
        print(mate_idx)
        if(mate_idx != -1):
            mating_begin_time = time.time()
            offspring_players = players[idx].sexual_reproduction(mating_begin_time, True)
            players[mate_idx].sexual_reproduction(mating_begin_time)
            for offspring_player in offspring_players:
                players.append(offspring_player)
            INITIAL_POPULATION += len(offspring_players)
    elif action == 12:          #fight
        if(players[idx].fighting_with == -1):
            enemy = search_enemy(players[idx], players)
            if(enemy != -1):
                players[0].fighting_with = enemy
                players[enemy].fighting_with = 0
                players[0].energy -= 10
                players[enemy].energy -= 10
                players[0].fighting_with = -1
                players[enemy].fighting_with = -1

    # Show particles
    for j in range(NUMBER_OF_PARTICLES):
        if(type(my_particles[j]) != int):
            my_particles[j].show_particle()

    now_time = time.time()

    for i in range(INITIAL_POPULATION):
        if(i not in killed):

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

    time.sleep(0.001)

    return reward, killed

agent = 0
for i in range(100):
    if(agent in killed):
        break
    print(i)
    actions(0, 0)
    actions(1, 0)
