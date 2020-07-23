import time
import numpy as np
import random

from player_class import Player
from particle_class import Particle
from global_constants import INITIAL_POPULATION, TIME, PARTICLES_TO_REGROW

def food_nearby(player, food_particles):         #returns food particle index if food is nearby, else returns -1
    if(type(player) == int):
        return -1
    for i, food_particle in enumerate(food_particles):
        if(type(food_particle) != int):
            ed = ((food_particle.particleX - (player.playerX+16))**2 + (food_particle.particleY - (player.playerY+16))**2)**(1/2)
            if(ed <= 20):
                return i
    return -1

def food_in_env(player, food_particles):         #returns food particle index if food is nearby, else returns -1
    env = []
    distances = []
    if(type(player) == int):
        return -1
    for i, food_particle in enumerate(food_particles):
        if(type(food_particle) != int):
            ed = ((food_particle.particleX - (player.playerX))**2 + (food_particle.particleY - (player.playerY))**2)**(1/2)
            if(ed <= 100):
                env.append(i)
                distances.append(ed)

    return env,distances

def players_in_env(host, players):
    env = []
    distances = []
    if (type(host) == int):
        return [],[]
    for i, player in enumerate(players):
        if (type(player) != int) and (player != host):
            ed = ((host.playerX - (player.playerX))**2 + (host.playerY - (player.playerY ))**2)**(1/2)
            if(ed <= 100):
                env.append(i)
                distances.append(ed)

    return env,distances

def getPlayerVector(host, env_players, all_players):
    X = []
    Y = []
    sex = []
    if (type(host) == int):
        return [],[]
    gender_to_number = {'Female': 1, 'Male': 2}
    for idx in (env_players):
        if (type(all_players[idx]) != int) and (all_players[idx] != host):
            X.append( (host.playerX - all_players[idx].playerX ) )
            Y.append( (host.playerY - all_players[idx].playerY ) )
            sex.append(gender_to_number[all_players[idx].gender])

    if(len(X) == 0):
        X.append(0)
        Y.append(0)
        sex.append(0)

    return list([X,Y,sex])

def getFoodVector(player, env_particles, all_particles):
    X = []
    Y = []
    if (type(player) == int):
        return [],[]
    for idx in (env_particles):
        if type(all_particles[idx]) != int :
            X.append( (player.playerX - all_particles[idx].particleX ) )
            Y.append( (player.playerY - all_particles[idx].particleY ) )

    if(len(X) == 0):
        X.append(0)
        Y.append(0)

    return list([X,Y])

def search_mate(host, players, TIME):
    env = []
    if (type(host) == int):
        return -1
    for i, player in enumerate(players):
        if (type(player) != int) and (player != host) and (not player.is_impotent) and ((TIME - player.born_at) in range(10, 61)) and (player.gender != host.gender):
            ed = (((host.playerX+16) - (player.playerX+16))**2 + ((host.playerY+16) - (player.playerY+16))**2)**(1/2)
            if(ed <= 30):
                env.append(i)

    return env[np.array(env).argsort()[0]] if len(env) > 0 else -1

def search_enemy(host, players):
    env = []
    if (type(host) == int):
        return -1
    for i, player in enumerate(players):
        if (type(player) != int) and (player != host) and (player.fighting_with == -1):
            ed = (((host.playerX+16) - (player.playerX+16))**2 + ((host.playerY+16) - (player.playerY+16))**2)**(1/2)
            if(ed <= 30):
                env.append(i)

    return env[np.array(env).argsort()[0]] if len(env) > 0 else -1

def check_particles(my_particles):
    for my_particle in my_particles:
        for j, my_particle_inner in enumerate(my_particles):
            if(my_particle_inner != my_particle and type(my_particle) != int and type(my_particle_inner) != int):
                ed = ((my_particle.particleX - my_particle_inner.particleX)**2 + (my_particle.particleY - my_particle_inner.particleY)**2)**(1/2)
                if(ed < 20):
                    my_particles[j] = 0
    return my_particles

def regenerate_species(TIME):
    players = []
    for i in range(INITIAL_POPULATION):
        players.append(Player(i, TIME))
    return players

def refreshParticles(particles, NUMBER_OF_PARTICLES):
    NEW_PARTICLES = random.randint(PARTICLES_TO_REGROW[0],PARTICLES_TO_REGROW[1])
    for j in range(NEW_PARTICLES):
        particles.append(Particle())
    particles = check_particles(particles)
    NUMBER_OF_PARTICLES+=NEW_PARTICLES
    return particles,NUMBER_OF_PARTICLES
