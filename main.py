import pygame

#initialise pygame
pygame.init()

# Size constants
PLAYER_WIDTH = PLAYER_HEIGHT = 32
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

#create a screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Title
pygame.display.set_caption("Chimichangas")

#player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 370

#to capture the movement speed
playerX_change = 0
playerY_change = 0

# Speed
speed = 3

def player(x, y):
    screen.blit(playerImg, (x, y))

#Game loop
running = True
while running:

    #First the screen is filled so that every thing is above the screen
    screen.fill((255, 255, 255))

    for event in pygame.event.get():

        #To check whether the window is quitted or not
        if event.type == pygame.QUIT:
            running = False

        #if key is pressed, check whether it's right, left, up or down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -speed
            if event.key == pygame.K_RIGHT:
                playerX_change = speed
            if event.key == pygame.K_UP:
                playerY_change = -speed
            if event.key == pygame.K_DOWN:
                playerY_change = speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change

    # Don't let the agent get out of the world
    if(playerX <= 0):
        playerX = 0
    elif(playerX >= (SCREEN_WIDTH - PLAYER_WIDTH)):
        playerX = (SCREEN_WIDTH - PLAYER_WIDTH)

    if(playerY <= 0):
        playerY = 0
    elif(playerY >= (SCREEN_HEIGHT - PLAYER_HEIGHT)):
        playerY = (SCREEN_HEIGHT - PLAYER_HEIGHT)

    #Call the player
    player(playerX, playerY)

    #Update the window
    pygame.display.update()
