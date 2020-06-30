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

FOOD_REGEN_CONDITION_IS_MET = False                    #temporary value

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
    elif action == 9: #Ingestion
        food_particle = food_nearby(players[idx], my_particles)
        if(food_particle != -1):
            players[idx].ingesting_food(food_particle, TIME)
            my_particles[food_particle] = 0
    elif action == 10:  #asexual_reproduction
        if(type(players[idx]) != int and not players[idx].is_impotent and type(players[idx]) != int and (TIME - players[idx].born_at) in range(10, 61))):
            offspring_players, offspring_ids = players[idx].asexual_reproduction(len(players))
            for offspring_player in offspring_players:
                players.append(offspring_player)
            INITIAL_POPULATION += len(offspring_players)
            players[idx].update_history(action, TIME, reward, num_offspring = len(offspring_ids), offspring_ids = offspring_ids)
            players[idx].write_data()   #Writes data to file
            players[idx] = 0
            killed.append(idx)
    elif action == 11:  #sexual_reproduction
        mate_idx = search_mate(players[idx],players)
        print(mate_idx)
        if(mate_idx != -1):
            mating_begin_time = TIME
            reward = -30
            offspring_players, offspring_ids = players[idx].sexual_reproduction(mating_begin_time, len(players), True)
            players[mate_idx].sexual_reproduction(mating_begin_time, len(players))
            for offspring_player in offspring_players:
                players.append(offspring_player)
            INITIAL_POPULATION += len(offspring_players)
            players[idx].update_history(action, mating_begin_time, reward, num_offspring = len(offspring_ids), offspring_ids = offspring_ids, mate_id = mate_idx)
            players[mate_idx].update_history(action, mating_begin_time, reward, num_offspring = len(offspring_ids), offspring_ids = offspring_ids, mate_id = idx)
    elif action == 12:      #Fight
        if(players[idx].fighting_with == -1):
            enemy = search_enemy(players[idx], players)
            if(enemy != -1):
                players[idx].fighting_with = enemy
                players[enemy].fighting_with = idx
                players[idx].energy -= 10
                players[enemy].energy -= 10
                players[idx].fighting_with = -1
                players[enemy].fighting_with = -1

            players[idx].update_history(action, TIME, reward, fight_with = enemy )
            players[enemy].update_history(action, TIME, reward, fight_with = idx)

    if action <=9 :
        players[idx].update_history(action, TIME, reward)
        
    if (FOOD_REGEN_CONDITION_IS_MET):                                       #FOOD REGEN PART always false for now
        my_particles,NUMBER_OF_PARTICLES = refreshParticles(my_particles,NUMBER_OF_PARTICLES)

    # Show particles
    for j in range(NUMBER_OF_PARTICLES):
        if(type(my_particles[j]) != int):
            my_particles[j].show_particle()

    now_time = TIME

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

            if(type(players[i]) != int and players[i].ingesting_begin_time != 0 and TIME - players[i].ingesting_begin_time >= 1):
                players[i].food_ate += 1
                players[i].ingesting_begin_time = 0
                players[i].cannot_move = False

            if(type(players[i]) != int and players[i].mating_begin_time != 0 and TIME - players[i].mating_begin_time >= 2):
                players[i].mating_begin_time = 0
                players[i].cannot_move = False

            if(players[i].energy <= 0):
                players[i].write_data()
                killed.append(i)

            if(now_time - players[i].born_at >= MAX_AGE):
                players[i].kill_player()
                players[i] = 0
                players[i].write_data()
                killed.append(i)

    # Update the window
    pygame.display.update()

    TIME += 1

    return reward, killed
#
# agent = 0
# for i in range(100):
#     if(agent in killed):
#         break
#     print(i)
#     actions(0, 0)
#     actions(1, 0)
#     actions(0, 10)
#     actions(1, 9)

time_tot = 0
for _ in range(10):
    start = time.time()
    actions(0, 0)
    end = time.time()
    time_tot += (end - start)
print(time_tot / 10.)
