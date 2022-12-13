import pygame
import colorswatch as cs

pygame.init()

class Weapon(object):
    def __init__(self, speed, color, x, y, w, h, direction):
        self.constructor(speed, color, x, y, w, h, direction)


    def constructor(self, speed, color, x, y, w, h, direction):
        self.speed = speed
        self.color = color
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hitbox = pygame.Rect(x, y, w, h)
        self.imagerect = pygame.Rect(x, y, w, h)
        self.direction = direction
        self.imagerect = None

    def update(self, direction):
        #single axis
        if self.direction == "left":
            self.x -= self.speed
        if self.direction == "up":
            self.y -= self.speed
        if self.direction == "right":
            self.x += self.speed
        if self.direction == "down":
            self.y += self.speed

        #diagonals
        #NW
        if self.direction == ("left", "up"):
            self.x -= self.speed
            self.y -= self.speed
        #NE
        if self.direction ==("right", "up"):
            self.x += self.speed
            self.y -= self.speed
        #SE
        if self.direction == ("right", "down"):
            self.x += self.speed
            self.y += self.speed
        #SW
        if self.direction == ("left", "down"):
            self.x -= self.speed
            self.y += self.speed

        self.hitbox.x = self.x
        self.hitbox.y = self.y

    def draw(self, window):
        if self.direction == "left" or self.direction == "right":
            self.imagerect = pygame.draw.rect(window,self.color,self.hitbox)
        else:
            new_w = self.h
            new_h = self.w
            self.imagerect = pygame.draw.rect(window, self.color, [self.x, self.y, new_w, new_h])