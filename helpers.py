import time
import numpy as np

from player_class import Player

def food_nearby(player, food_particles):         #returns food particle index if food is nearby, else returns -1
    if(type(player) == int):
        return -1
    for i, food_particle in enumerate(food_particles):
        if(type(food_particle) != int):
            ed = ((food_particle.particleX - (player.playerX + 16))**2 + (food_particle.particleY - (player.playerY + 16))**2)**(1/2)
            if(ed <= 10):
                return i
    return -1


def food_in_env(player, food_particles):         #returns food particle index if food is nearby, else returns -1
    env = []
    distances = []
    if(type(player) == int):
        return [],[]
    for i, food_particle in enumerate(food_particles):
        if(type(food_particle) != int):
            ed = ((food_particle.particleX - (player.playerX))**2 + (food_particle.particleY - (player.playerY))**2)**(1/2)
            if(ed <= 100):
                env.append(i)
                distances.append(ed)
    # print("ENV :", env)
    return env,distances


def players_in_env(host, players):
    env = []
    distances = []
    # if(type(host) == int):
    #     return [],[]
    if (host.is_killed == True):
        return [],[]
    for i, player in enumerate(players):
        # if (type(player) != int) and (player != host):
        if (player.is_killed == False) and (player != host):
            ed = ((host.playerX - (player.playerX ))**2 + (host.playerY - (player.playerY ))**2)**(1/2)
            # print("DIST B/W ", host," AND ",player," = ",ed)
            if(ed <= 100):
                env.append(i)
                distances.append(ed)
    return env,distances

def search_mate(host, players):
    env = []
    # if(type(host) == int):
    #     return [],[]
    if (host.is_killed == True):
        return [],[]
    for i, player in enumerate(players):
        # if (type(player) != int) and (player != host):
        if (player.is_killed == False) and (player != host) and (not player.is_impotent) and ((round(time.time() - player.born_at) in range(10, 61))) and (player.gender != host.gender):
            ed = ((host.playerX - (player.playerX ))**2 + (host.playerY - (player.playerY ))**2)**(1/2)
            # print("DIST B/W ", host," AND ",player," = ",ed)
            if(ed <= 20):
                env.append(i)
    return env[np.array(env).argsort()[0]] if len(env) > 0 else -1


def check_particles(my_particles):              #checks if food particles are clustered ande removes any closer than 20px
    for my_particle in my_particles:
        for j, my_particle_inner in enumerate(my_particles):
            if(my_particle_inner != my_particle and type(my_particle) != int and type(my_particle_inner) != int):
                ed = ((my_particle.particleX - my_particle_inner.particleX)**2 + (my_particle.particleY - my_particle_inner.particleY)**2)**(1/2)
                if(ed < 20):
                    my_particles[j] = 0
    return my_particles

def regenerate_species(pop_size, screen, SCREEN_WIDTH, SCREEN_HEIGHT):         #regenerates creatures, returns list of new species
    INITIAL_POPULATION = pop_size
    players = []
    i = 0
    while(i < INITIAL_POPULATION):
        print("Born", (i+1), "/", INITIAL_POPULATION)
        player = Player(screen, 'player.png', 32, 32, SCREEN_WIDTH, SCREEN_HEIGHT)
        players.append(player)
        ## TODO: Remove this time.sleep when testing is done
        time.sleep(2)
        i += 1
    return players
