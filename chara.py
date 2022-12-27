import pygame
import colorswatch as cs
import os
import cylon as enemy

pygame.init()

class Character:
    def __init__(self, window, posx, posy):
        self.window = window
        self.posX = posx
        self.posY = posy
        self.alive = True
        self.horizspeed = 10
        self.vertspeed = 5
        self.walkcycle = [pygame.image.load(os.path.join("player", "player_run_right_1.png")),pygame.image.load(os.path.join("player", "player_run_right_1.png")),pygame.image.load(os.path.join("player", "player_run_right_1.png")),pygame.image.load(os.path.join("player", "player_run_right_1.png")),pygame.image.load(os.path.join("player", "player_run_right_2.png")),pygame.image.load(os.path.join("player", "player_run_right_2.png")),pygame.image.load(os.path.join("player", "player_run_right_2.png")),pygame.image.load(os.path.join("player", "player_run_right_2.png")),]
        self.stand_right = "player_stand_right.png"
        self.shoot_right = pygame.image.load(os.path.join("player", "player_shoot_right.png"))
        self.imagefile = self.stand_right
        self.currentimage = pygame.image.load(os.path.join("player", self.imagefile))
        self.mask = pygame.mask.from_surface(self.currentimage)
        self.pew = pygame.mixer.Sound(os.path.join("sounds", "player_fire.wav"))
        self.trigger = ["left", "up", "right", "down", "firing", "walking"]
        self.frameCount = 0
        self.currentdirection = self.trigger[2]
        self.orientation = None
        self.moving = False
        self.isLeft = False
        self.isRight = True
        self.isfiring = False
        self.firingdirection = "right"
        self.width = self.currentimage.get_width()
        self.height = self.currentimage.get_height()
        self.hitbox = pygame.Rect(self.posX, self.posY, self.width, self.height)


    def draw(self, direction = "right", vertical = None, moving = False, firing = False):
        self.orientation = vertical
        self.moving = moving
        self.isfiring = firing
        #default draw condition
        if self.alive:
            if not moving and not firing:
                if direction == self.trigger[2]:
                    self.window.blit(self.currentimage, (self.posX, self.posY))
                if direction == self.trigger[0]:
                    self.window.blit(pygame.transform.flip(self.currentimage, True, False), (self.posX, self.posY))


    def get_height(self):
        return self.currentimage.get_height()

    def get_width(self):
        return self.currentimage.get_width()

    def animate(self):
        if self.frameCount >= 7:
            self.frameCount = 0

        if self.isRight:
            self.window.blit(self.walkcycle[self.frameCount], (self.posX, self.posY))

        if self.isLeft:
            self.window.blit(pygame.transform.flip(self.walkcycle[self.frameCount], True, False), (self.posX, self.posY))

        self.frameCount += 1



    def move(self, direction):
        if self.moving and not self.isfiring:
            ##Left
            if direction == self.trigger[0]:
                self.posX -= self.horizspeed

            ##Right
            if direction == self.trigger[2]:
                self.posX += self.horizspeed

            ##Up
            if direction == self.trigger[1]:
                self.posY -= self.vertspeed

            ##down
            if direction == self.trigger[3]:
                self.posY += self.vertspeed

            self.hitbox.x = self.posX
            self.hitbox.y = self.posY

            self.animate()






