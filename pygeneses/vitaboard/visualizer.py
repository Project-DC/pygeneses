import os
import pygame
import sys
import numpy as np
import time

from pygeneses.envs.prima_vita.global_constants import *
from pygeneses.envs.prima_vita.player_class import Player
from pygeneses.envs.prima_vita.particle_class import Particle

pygame.init()

pygame.display.set_caption("Prima Vita")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

screen.fill((0, 178, 0))

myfont = pygame.font.SysFont("monospace", 32)


def current_action_time(result, action, timestamp):
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
        12: "Fight"
    }

    actiontext = myfont.render(
        "Action: " + result + action_number_to_action.get(action, "Unknown"), 1, (255, 255, 255)
    )

    timetext = myfont.render(
        "Time: " + str(timestamp), 1, (255, 255, 255)
    )

    return actiontext, timetext


file_location = sys.argv[1]

life_events = np.load(file_location, allow_pickle=True)

x, y = life_events[0][0], life_events[0][1]
i = 0
try:
    tob = life_events[2][1] if len(life_events[1]) == 2 else life_events[1][1]
except:
    print(os.path.basename(file_location).split(".")[0].split("-")[1], "died without doing anything")
    sys.exit()

life_events = life_events[2:] if len(life_events[1]) == 2 else life_events[1:]

player = Player(i, tob, x, y, mode="human")

for life_event in life_events:
    result = "" if life_event[2] != -10 else "Failed "
    action = life_event[0]
    timestamp = life_event[1]

    actiontext, timetext = current_action_time(result, action, timestamp)

    screen.fill((0, 178, 0))

    food_in_proximity = life_event[-1][0]
    players_in_proximity = life_event[-1][1]

    particles = []
    players = []

    for i in range(len(food_in_proximity)//2):
        food_info = food_in_proximity[i:i+2]
        if(len(food_info) > 0):
            particles.append(Particle(x=(player.playerX + food_info[0]), y=(player.playerY + food_info[1]), mode='human'))
            particles[-1].show_close(screen)

    for i in range(len(players_in_proximity)//3):
        player_info = players_in_proximity[i:i+3]
        if(len(player_info) > 0):
            players.append(Player(i=i, tob=i, x=(player.playerX + player_info[0]), y=(player.playerY + player_info[1]), mode='human'))
            players[-1].show_close(screen)

    for event in pygame.event.get():
        pass

    if action == 0:  # Left
        player.change_player_xposition(-3)

    elif action == 1:  # Right
        player.change_player_xposition(3)

    elif action == 2:  # Up
        player.change_player_yposition(-3)

    elif action == 3:  # Down
        player.change_player_yposition(3)

    elif action == 4:  # Up Left
        player.change_player_yposition(-3)
        player.change_player_xposition(-3)

    elif action == 5:  # Up Right
        player.change_player_yposition(-3)
        player.change_player_xposition(3)

    elif action == 6:  # Down Left
        player.change_player_yposition(3)
        player.change_player_xposition(-3)

    elif action == 7:  # Down Right
        player.change_player_yposition(3)
        player.change_player_xposition(3)

    elif action == 8:  # Stay
        player.energy -= 2

    player.show_player(screen)
    screen.blit(actiontext, (5, 10))
    screen.blit(timetext, (5, 30))

    pygame.display.update()

    time.sleep(0.5)
