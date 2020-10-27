import pickle
import os
import pygame

from .global_constants import *

def save(model, filename="latest_run.pickle"):
    model.screen = None

    if model.mode == "human":
        for i in range(len(model.players)):
            if type(model.players[i]) != int:
                model.players[i].playerImg = ""
                
        for i in range(len(model.food_particles)):
            if type(model.food_particles[i]) != int:
                model.food_particles[i].particleImg = ""
    
    with open(filename, "wb") as file:
        pickle.dump(model, file)

    print(f"Prima vita environment snapshot created successfully at {filename}!")

def load(filename="latest_run.pickle"):
    with open(filename, "rb") as file:
        model = pickle.load(file)
    
    if model.mode == "human":
        pygame.init()
        model.screen = pygame.display.set_mode((1200, 700))

        for i in range(len(model.players)):
            if type(model.players[i]) != int:
                model.players[i].playerImg = pygame.image.load(
                    os.path.join(os.path.dirname(__file__), "images/player.png")
                )
                
        for i in range(len(model.food_particles)):
            if type(model.food_particles[i]) != int:
                model.food_particles[i].particleImg = pygame.image.load(
                    os.path.join(os.path.dirname(__file__), "images/food.png")
                )

    print(f"Prima vita environment snapshot loaded successfully from {filename}!")

    return model
        