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
        self.vertspeed = 4
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





class Player(Character):
    def __init__(self, window, posx, posy):
        super().__init__(window, posx, posy)
        self.lives = 3
        self.points = 0

    def controller(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.currentdirection = self.trigger[0]
            self.firingdirection = self.trigger[0]
            self.moving = True
            self.isRight = False
            self.isLeft = True
            self.move(self.currentdirection)

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.currentdirection = self.trigger[2]
            self.firingdirection = self.trigger[2]
            self.moving = True
            self.isRight = True
            self.isLeft = False
            self.move(self.currentdirection)

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.firingdirection = self.trigger[1]
            self.moving = True
            self.move(self.trigger[1])

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.firingdirection = self.trigger[3]
            self.moving = True
            self.move(self.trigger[3])

        if keys[pygame.K_SPACE]:
            self.isfiring = True
            self.fire(self.firingdirection)





#Testbed
"""
The below is absolutely imperitive in order to make the player move.
Use below as a point of reference.
"""
w = 1000
h = 800
window = pygame.display.set_mode((w,h))
pygame.display.set_caption("Testbed")

inPlay = False

player = Player(window, 50, 575)
FPS = 30
clock = pygame.time.Clock()

while inPlay:
    clock.tick(FPS)

    player.draw(player.currentdirection, vertical=player.orientation, moving = player.moving, firing = player.isfiring)

    player.controller()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYUP and (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
            player.moving = False
        if event.type == pygame.KEYUP and (event.key == pygame.K_LEFT or event.key == pygame.K_a):
            player.moving = False
        if event.type == pygame.KEYUP and (event.key == pygame.K_UP or event.key == pygame.K_w):
            player.moving = False
        if event.type == pygame.KEYUP and (event.key == pygame.K_DOWN or event.key == pygame.K_s):
            player.moving = False
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            player.isfiring = False



    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        inPlay = False


    if player.posX > w:
        player.posX = 0
    if player.posX < -45:
        player.posX = w
    if player.posY > h:
        player.posY = -80
    if player.posY < -80:
        player.posY = h

    pygame.display.update()
    window.fill(cs.black["pygame"])