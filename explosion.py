import pygame
import os
pygame.init()

class Explosion(object):
    def __init__(self, window, x, y):
        self.filmstrip = [pygame.image.load(os.path.join("explosion", f"explode_{i}.png")) for i in range(1, 22)]
        self.currentframe = 0
        self.isvisible = True
        self.window = window
        self.x = x
        self.y = y

    def blowup(self):
        if self.isvisible:
            self.window.blit(self.filmstrip[self.currentframe], (self.x, self.y))
            self.currentframe += 1

            if self.currentframe >= len(self.filmstrip):
                self.isvisible = False

