# PyGame visualizer for an agent from log file

# Import required libraries
import os
import pygame
import sys
import numpy as np
import time
import argparse

# Import global constants, player class and particle class
from pygeneses.envs.prima_vita.global_constants import *
from pygeneses.envs.prima_vita.player_class import Player
from pygeneses.envs.prima_vita.particle_class import Particle


def current_action_time(result, action, timestamp, myfont):
    """
    Convert action from number to text and display in pygame screen along with the time at which the action was performed

    Params
    ======
    result    (str)
        : Empty string in case of successful action else contains the string 'Failed'
    action    (int)
        : Action performed at current time step by the agent
    timestamp (int)
        : Timestamp (in ticks) of current action
    myfont    (pygame.font.SysFont)
        : Font to use for displaying action and time information in screen (monospace 32)

    Returns
    =======
    Surface
        : Action in english instead of integer (to be displayed in screen)
    Surface
        : Time stamp text (to be displayed in screen)
    """

    # Dictionary to map actions from integer to descriptive string
    action_number_to_action = {
        0: "Left",
        1: "Right",
        2: "Up",
        3: "Down",
        4: "Up Left",
        5: "Up Right",
        6: "Down Left",
        7: "Down Right",
        8: "Stay",
        9: "Ingestion",
        10: "Asexual Reproduction",
        11: "Sexual Reproduction",
        12: "Fight",
    }

    # Render the action text using myfont
    actiontext = myfont.render(
        "Action: " + result + action_number_to_action.get(action, "Unknown"),
        1,
        (255, 255, 255),
    )

    # Render time stamp text using myfont
    timetext = myfont.render("Time: " + str(timestamp), 1, (255, 255, 255))

    return actiontext, timetext


def visualize(file_location, speed):
    """
    Convert action from number to text and display in pygame screen along with the time at which the action was performed

    Params
    ======
    file_location  (str)
        : Full path of log file of agent containing all the actions performed by the agent throughout his/her lifetime
    speed          (int)
        : Speed (in seconds) after which the next frame should be loaded (display speed)
    """

    # Initialize pygame
    pygame.init()

    # Set caption for the pygame window
    pygame.display.set_caption("Prima Vita")

    # Set the size of pygame window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Fill the screen in green color
    screen.fill((0, 178, 0))

    # Create font in which everything will be rendered in screen
    myfont = pygame.font.SysFont("monospace", 32)

    # Extract all events in the agent's life
    life_events = np.load(file_location, allow_pickle=True)

    # Get initial position (stored at index 0 of log file)
    x, y = life_events[0][0], life_events[0][1]
    i = 0
    try:
        # Get time of birth (though it is present in the filename itself), this line helps to identify
        # if the agent died without doing anything or not
        tob = life_events[2][1] if len(life_events[1]) == 2 else life_events[1][1]
    except:
        # Agent died without doing anything, exit the visualizer
        print(
            os.path.basename(file_location).split(".")[0].split("-")[1],
            "died without doing anything",
        )
        sys.exit()

    # Get all the actions from life events
    life_events = life_events[2:] if len(life_events[1]) == 2 else life_events[1:]

    # Initialize player object for the current player
    player = Player(i, log_dir=".", tob=tob, energy=200, x=x, y=y, mode="human")

    for life_event in life_events:
        # Extract action result, action and time at which it was done
        result = "" if life_event[2] != -20 else "Failed "
        action = life_event[0]
        timestamp = life_event[1]

        # Get the text for action and timestamp
        actiontext, timetext = current_action_time(result, action, timestamp, myfont)

        # Fill the screen with green color
        screen.fill((0, 178, 0))

        # Find the food particles and players in proximity to current agent
        food_in_proximity = life_event[-1][0]
        players_in_proximity = life_event[-1][1]

        particles = []
        players = []

        # Display the food particle which are in the agent's state
        for i in range(len(food_in_proximity) // 2):
            food_info = food_in_proximity[i : i + 2]
            if len(food_info) > 0:
                particles.append(
                    Particle(
                        x=(player.playerX + food_info[0]),
                        y=(player.playerY + food_info[1]),
                        mode="human",
                    )
                )
                particles[-1].show_close(screen)

        # Display the agents which are in close proximity to current agent
        # All other agents appear yellow (as they are shown using show_close) while the current agent is shown in red color
        for i in range(len(players_in_proximity) // 3):
            player_info = players_in_proximity[i : i + 3]
            if len(player_info) > 0:
                players.append(
                    Player(
                        i=i,
                        tob=i,
                        log_dir=".",
                        energy=200,
                        x=(player.playerX + player_info[0]),
                        y=(player.playerY + player_info[1]),
                        mode="human",
                    )
                )
                players[-1].show_close(screen)

        for event in pygame.event.get():
            pass

        # Action left
        if action == 0:
            player.change_player_xposition(-3)
        # Action right
        elif action == 1:
            player.change_player_xposition(3)
        # Action up
        elif action == 2:
            player.change_player_yposition(-3)
        # Action down
        elif action == 3:
            player.change_player_yposition(3)
        # Action up then left (North-West)
        elif action == 4:
            player.change_player_yposition(-3)
            player.change_player_xposition(-3)
        # Action up then right (North-East)
        elif action == 5:
            player.change_player_yposition(-3)
            player.change_player_xposition(3)
        # Action down then left (South-West)
        elif action == 6:
            player.change_player_yposition(3)
            player.change_player_xposition(-3)
        # Action down then right (South-East)
        elif action == 7:
            player.change_player_yposition(3)
            player.change_player_xposition(3)
        # Action stay
        elif action == 8:
            player.energy -= 2

        # Show current player
        player.show_player(screen)

        # Blit the action text and timestamp text to screen
        screen.blit(actiontext, (5, 10))
        screen.blit(timetext, (5, 30))

        # Update the pygame display
        pygame.display.update()

        # Wait for some time (in seconds) until processing the next action (frame)
        # So that humans can properly see what is going on in an agent's life
        time.sleep(speed)

# If the namespace is __main__ then read from pass_params.txt and pass those params to visualize
if __name__ == "__main__":
    with open("pass_params.txt", "r") as file:
        params = file.read().split("\n")[:-1]
    visualize(params[0], float(params[1]))
