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
