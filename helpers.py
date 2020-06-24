import time

from player_class import Player

def food_ingesting(player, food_particles):
    if(type(player) == int):
        return -1
    for i, food_particle in enumerate(food_particles):
        if(type(food_particle) != int):
            ed = ((food_particle.particleX - (player.playerX + 16))**2 + (food_particle.particleY - (player.playerY + 16))**2)**(1/2)
            if(ed <= 10):
                return i
    return -1

def check_particles(my_particles):
    for my_particle in my_particles:
        for j, my_particle_inner in enumerate(my_particles):
            if(my_particle_inner != my_particle and type(my_particle) != int and type(my_particle_inner) != int):
                ed = ((my_particle.particleX - my_particle_inner.particleX)**2 + (my_particle.particleY - my_particle_inner.particleY)**2)**(1/2)
                if(ed < 20):
                    my_particles[j] = 0
    return my_particles

def regenerate_species(pop_size, screen, SCREEN_WIDTH, SCREEN_HEIGHT):
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
