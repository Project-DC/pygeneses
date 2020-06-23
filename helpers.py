def food_ingesting(player, food_particles):
    if(type(player) == int):
        return -1
    for i, food_particle in enumerate(food_particles):
        if(type(food_particle) != int):
            ed = ((food_particle.particleX - (player.playerX + 16))**2 + (food_particle.particleY - (player.playerY + 16))**2)**(1/2)
            if(ed <= 10):
                return i
    return -1
