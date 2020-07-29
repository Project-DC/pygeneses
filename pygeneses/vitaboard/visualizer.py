import pygame
import sys
import numpy as np
import time

from pygeneses.envs.prima_vita.global_constants import *
from pygeneses.envs.prima_vita.player_class import Player

pygame.init()

pygame.display.set_caption("Prima Vita")

screen.fill((0, 178, 0))

for event in pygame.event.get():
    pass

pygame.display.update()

myfont = pygame.font.SysFont("monospace", 32)

def current_action(action):
    action_number_to_action = {0: 'Left', 1: 'Right', 2: 'Up', 3: 'Down', 4: 'Up Left',
    5: 'Up Right', 6: 'Down Left', 7: 'Down Right', 8: 'Stay'}

    actiontext = myfont.render("Action: " + action_number_to_action[action], 1, (255, 255, 255))

    return actiontext

file_location = sys.argv[1]

life_events = np.load(file_location, allow_pickle=True)

x, y = life_events[0][0], life_events[0][1]
i = 0
tob = life_events[2][1] if len(life_events[1]) == 2 else life_events[1][1]

life_events = life_events[2:] if len(life_events[1]) == 2 else life_events[1:]

player = Player(i, tob, x, y)

for life_event in life_events:
    action = life_event[0]
    scoretext = current_action(action)

    screen.fill((0, 178, 0))

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

    player.show_player()
    screen.blit(scoretext, (5, 10))

    pygame.display.update()

    time.sleep(0.5)
