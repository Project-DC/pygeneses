# Functions to load and save Prima vita environment

# Import required libraries
import pickle
import os
import pygame

# Import other classes
from .global_constants import *

def save(model, filename="latest_run.pickle"):
    """
    Saves the Prima vita object's snapshot in pickle format

    Params
    ======
    model    (pygeneses.envs.prima_vita.prima_vita.PrimaVita)
            : Current model object (this will be saved as pickle file)
    filename (str)
            : File where environment snapshot will be saved 
    """

    # Screen need not be saved as it can be rebuilt when loading
    model.screen = None

    if model.mode == "human":
        # Player images cannot be serialized, hence killing these pygame.Surface objects
        for i in range(len(model.players)):
            if type(model.players[i]) != int:
                model.players[i].playerImg = ""

        # Food particle images cannot be serialized, hence killing these pygame.Surface objects    
        for i in range(len(model.food_particles)):
            if type(model.food_particles[i]) != int:
                model.food_particles[i].particleImg = ""
    
    # Dump into pickle file
    with open(filename, "wb") as file:
        pickle.dump(model, file)

    print(f"Prima vita environment snapshot created successfully at {filename}!")

def load(filename="latest_run.pickle"):
    """
    Loads the Prima vita object's snapshot from pickle file

    Params
    ======
    filename (str)
            : File where environment snapshot is saved

    Returns
    =======
    model    (pygeneses.envs.prima_vita.prima_vita.PrimaVita)
            : Prima vita object with snapshot loaded from pickle file
    """

    # Load environment from pickle dump
    with open(filename, "rb") as file:
        model = pickle.load(file)
    
    if model.mode == "human":
        # Initialize pygame screen if in human mode
        pygame.init()
        model.screen = pygame.display.set_mode((1200, 700))

        # Set player images as they weren't saved
        for i in range(len(model.players)):
            if type(model.players[i]) != int:
                model.players[i].playerImg = pygame.image.load(
                    os.path.join(os.path.dirname(__file__), "images/player.png")
                )
        
        # Set food particle images as they weren't saved       
        for i in range(len(model.food_particles)):
            if type(model.food_particles[i]) != int:
                model.food_particles[i].particleImg = pygame.image.load(
                    os.path.join(os.path.dirname(__file__), "images/food.png")
                )

    print(f"Prima vita environment snapshot loaded successfully from {filename}!")

    # Return environment object
    return model
        