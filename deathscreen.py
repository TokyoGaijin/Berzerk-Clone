import pygame
import colorswatch
import os

pygame.init()
pygame.font.init()

roomsizeX = 1000
roomsizeY = 800
ROOMSIZE = (roomsizeX, roomsizeY)

WINDOW = pygame.display.set_mode(ROOMSIZE)

isplaying = False

deathcycle = [pygame.image.load(os.path.join("player", f"player_death_{i}.png")) for i in range(0, 13)]



def die():
    currentframe = 0
    framecount = len(deathcycle)
    currentimage = deathcycle[currentframe]

    if currentframe == 0:
        isplaying = True
        currentframe += 1
    if currentframe == framecount:
        isplaying = False

    WINDOW.blit(currentimage, (500,400))
