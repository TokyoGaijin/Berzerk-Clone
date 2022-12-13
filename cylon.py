import pygame
import colorswatch as cs
import os
import random
import explosion as boom
import threading


pygame.init()

def threadfunc(target):
    t = threading.Thread(target=target)
    t.start()


class Cylon:
    def __init__(self, window, posX, posY, color, speed):
        self.window = window
        self.posX = posX
        self.posY = posY
        self.color = color
        self.standcycle = []
        self.currentframe = 0
        self.speed = speed
        self.end = 0
        self.axis = None
        for i in range (0, 11):
            self.standcycle.append(pygame.image.load(os.path.join("cylon", f"cyclon_stand_{color}_{i}.png")))

        for frames in self.standcycle:
            self.mask = pygame.mask.from_surface(frames)

        self.walkstrip = [pygame.image.load(os.path.join("cylon", f"cyclon_walk_{self.color}_1.png")),pygame.image.load(os.path.join("cylon", f"cyclon_walk_{self.color}_1.png")),pygame.image.load(os.path.join("cylon", f"cyclon_walk_{self.color}_1.png")),pygame.image.load(os.path.join("cylon", f"cyclon_walk_{self.color}_1.png")),pygame.image.load(os.path.join("cylon", f"cyclon_walk_{self.color}_2.png")),pygame.image.load(os.path.join("cylon", f"cyclon_walk_{self.color}_2.png")),pygame.image.load(os.path.join("cylon", f"cyclon_walk_{self.color}_2.png")),pygame.image.load(os.path.join("cylon", f"cyclon_walk_{self.color}_2.png")),]
        self.boomstrip = [pygame.image.load(os.path.join("explosion", f"explode_{i}.png")) for i in range(1, 22)]
        self.maxsteps = 30
        self.currentstep = 0
        self.walkframe = 0
        self.iswalking = False
        self.distance = 0
        self.isalive = True
        self.isexploding = False
        self.inlist = True
        self.height = 75
        self.width = 59
        self.hitbox = pygame.Rect(self.posX, self.posY, self.width, self.height)


   
    def blowup(self):
        self.window.blit(self.boomstrip[self.currentframe], (self.posX, self.posY))
        self.currentframe += 1

        if self.currentframe >= len(self.boomstrip):
            self.currentframe = 20



    def move(self):
        if self.walkframe >= 7:
            self.walkframe = 0

        self.window.blit(self.walkstrip[self.walkframe], (self.posX, self.posY))
        self.walkframe += 1

        
    def draw(self):
        self.hitbox.move(self.posX, self.posY)
        if self.isalive:
            if not self.iswalking:
                if self.currentframe >= len(self.standcycle):
                    self.currentframe = 0

                self.window.blit(self.standcycle[self.currentframe], (self.posX, self.posY))

                self.currentframe += 1
            else:
                self.move()
        else:
            self.blowup()








directions = ["up", "down", "left", "right"]
xdirs = ["left", "right"]
ydirs = ["up", "down"]
axis = ["x", "y"]

##testbed
w = 600
h = 600
window = pygame.display.set_mode((w,h))
pygame.display.set_caption("Testbed")


inPlay = False
FPS = 30
clock = pygame.time.Clock()

movetimer = random.randrange(2, 10) * FPS


blue_cylon = Cylon(window, 150, 150, "blue", 2)



def getplusminus(course):
    if course == "x":
        heading = random.choice(xdirs)
        if heading == "left":
            return -random.randrange(0,11,5) *10
        if heading == "right":
            return random.randrange(0,11,5) * 10
    if course == "y":
        heading = random.choice(ydirs)
        if heading == "up":
            return -random.randrange(0,11,5) * 10
        if heading == "down":
            return random.randrange(0,11,5) * 10

blue_cylon.axis = random.choice(axis)
blue_cylon.end = getplusminus(blue_cylon.axis)
timings = [30, 90]
executetimer = random.choice(timings)

def resetall():
    global movetimer, executetimer
    blue_cylon.axis = random.choice(axis)
    blue_cylon.end = getplusminus(blue_cylon.axis)
    movetimer = random.randrange(2, 10) * FPS
    executetimer = random.choice(timings)
    if blue_cylon.posX > w or blue_cylon.posX < 0:
        blue_cylon.posX = 150
        blue_cylon.posY = 150
    if blue_cylon.posY > h or blue_cylon.posY < 0:
        blue_cylon.posY = 150


        blue_cylon.posY = 150

def update():
    global movetimer, executetimer
    movetimer -= 1

    if movetimer <= 0:
        blue_cylon.move(blue_cylon.axis, getplusminus(blue_cylon.axis))
        executetimer -= 1
        if executetimer <= 0:
            blue_cylon.iswalking = False
        if not blue_cylon.iswalking:
            resetall()


    pygame.display.update()
    window.fill(cs.black["pygame"])

while inPlay:
    clock.tick(FPS)

    blue_cylon.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        inPlay = False

    update()
