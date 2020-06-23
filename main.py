import pygame
import time

from player_class import Player

# Initialise pygame
pygame.init()

# Size constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

# Create a screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Title
pygame.display.set_caption("Chimichangas")

# Player
player = Player(screen, 'player.png', 32, 32, SCREEN_WIDTH, SCREEN_HEIGHT)

# Speed
speed = 1

# Seconds font
seconds = pygame.font.Font('freesansbold.ttf', 32)

def show_seconds(t):
    time_rem = seconds.render("Zindagi ke: " + str(t) + " s", True, (255, 255, 255))
    screen.blit(time_rem, (10, 10))

# Game loop
running = True
while running:

    # First the screen is filled so that every thing is above the screen
    screen.fill((0, 178, 0))

    for event in pygame.event.get():

        #To check whether the window is quitted or not
        if event.type == pygame.QUIT:
            running = False

        # If key is pressed, check whether it's right, left, up or down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.change_player_position(-speed, 0)
            if event.key == pygame.K_RIGHT:
                player.change_player_position(speed, 0)
            if event.key == pygame.K_UP:
                player.change_player_position(0, -speed)
            if event.key == pygame.K_DOWN:
                player.change_player_position(0, speed)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change_player_position(0, 0)
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player.change_player_position(0, 0)

    # Move the player
    player.move_player()

    # Show the player
    player.show_player()

    if(time.time() - player.born_at >= 90):
        player.kill_player()
        del player
        running = False
    else:
        show_seconds(round(time.time() - player.born_at, 0))

    # Update the window
    pygame.display.update()
