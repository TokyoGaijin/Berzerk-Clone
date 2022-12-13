import pygame
import random
import colorswatch as cs
import chara as character
import os
import weapon
from tkinter import *
from tkinter import messagebox
import cylon as enemy
import explosion as boom
import pygame.freetype
import deathscreen
from collections import namedtuple
import threading
import time


#The main game file

pygame.init()
pygame.font.init()

roomsizeX = 1000
roomsizeY = 800
ROOMSIZE = (roomsizeX, roomsizeY)


#WINDOW = pygame.display.set_mode(ROOMSIZE, pygame.FULLSCREEN)
WINDOW = pygame.display.set_mode(ROOMSIZE)
pygame.display.set_caption("B'Z'RK'R (c)2020 Tokyo Trekker, The T of Doom")

TITLEIMAGE = pygame.image.load(os.path.join("othergrafix", "TitleScreen.png"))
STORY = pygame.image.load(os.path.join("othergrafix", "storyscreen.png"))
PAUSE = pygame.image.load(os.path.join("othergrafix", "pausescreen.png"))
DEATH = pygame.image.load(os.path.join("othergrafix", "deathscreen.png"))

whatkilledit = None

bulletlist = []
bulletspeed = 10

enemylist = []
enemybulletlist = []
enemycoordinates = []
explosionlist = []
enemycolors = ["blue", "yellow", "gray"]

deathsound = pygame.mixer.Sound(os.path.join("sounds", "death.wav"))

cooldown = 30
killpoints = 100
roomclearpoints = 500
lifebonus = 500

level = 1

movetimers = []

scorelist = []



def threadfunc(target):
    t = threading.Thread(target=target)
    t.start()



class Life(object):
    def __init__(self, window):
        self.icon = pygame.image.load(os.path.join("icons", "lives_icon.png"))
        self.window = window
        self.posX = 644
        self.posY = 722
        self.lives = 3
        self.display_font = pygame.font.Font(os.path.join("fonts", "arcade_font.ttf"), 30)

    def addlife(self):
        self.lives += 1

    def draw(self):
        self.window.blit(self.icon, (self.posX, self.posY))
        showtext = self.display_font.render(f"x {self.lives}", 1, cs.white["pygame"])
        self.window.blit(showtext, (723, 751))





class ScoreDisplay:
    def __init__(self, window, posX, posY, size, timer = 0):
        self.window = window
        self.posX = posX
        self.posY = posY
        self.timer = timer
        self.display_font = pygame.font.Font(os.path.join("fonts", "arcade_font.ttf"), size)
        self.ondisplay = True

    def draw(self, text_string):
        showtext = self.display_font.render(text_string, 1, cs.white["pygame"])

        if self.ondisplay:
            self.window.blit(showtext, (self.posX, self.posY))
            self.timer -= 1
        if self.timer == 0:
            self.ondisplay = False



class GUIDisplay(ScoreDisplay):
    def __init__(self, window, posX, posY, size, timer = 0):
        super().__init__(window, posX, posY, size)


    def draw(self, text_string):
        showtext = self.display_font.render(text_string, 1, cs.white["pygame"])
        self.window.blit(showtext, (self.posX, self.posY))




ROOMPATTERNS = [["----2211------------",
                 "-----------------1--",
                 "--------------------",
                 "-----111---1111-----",
                 "-------------------2",
                 "-----------22------2",
                 "-------------------2",
                 "-----12-------------"],

                ["1111111------1111111",
                 "1---------E--------1",
                 "1----S--------1----1",
                 "1----1111111111----1",
                 "1----1-------------1",
                 "1-----------E------1",
                 "1---E--------------1",
                 "1111111------1111111"],

                ["1111111------1111111",
                 "1-----1------1-----1",
                 "1---S--------1--E--1",
                 "1--------E----------",
                 "111111--------E-----",
                 "1------------------1",
                 "1-----E------------1",
                 "1111111------1111111"],

                ["1111111------1111111",
                 "1-----1------1-----1",
                 "1-----1----E-1--E--1",
                 "1--S---------------1",
                 "1-------------E----1",
                 "1-----1------1-E---1",
                 "1-----1---E--1---E-1",
                 "1111111------1111111"],

                ["1111111------1111111",
                 "1---------------E--1",
                 "1----111111111-----1",
                 "-----1-------1----E-",
                 "-----1-------1111---",
                 "1--S------E-----1--1",
                 "1-----E---------1--1",
                 "1111111------1111111"],

                ["1111111------1111111",
                 "1-----1------1-----1",
                 "1---S-----------E--1",
                 "1------------------1",
                 "1111111------1111111",
                 "1---E----------E---1",
                 "1-------E----------1",
                 "1111111------1111111",],

                ["1111111------1111111",
                 "1------------1--E--1",
                 "1--S---------1-----1",
                 "1111111------1--E--1",
                 "--------------------",
                 "---E----------------",
                 "1-------------E----1",
                 "11111111111111111111",],

                ["1111111------1111111",
                 "1---------------E--1",
                 "1---S----E---1-----1",
                 "1-----1------1-----1",
                 "1-----1-----E------1",
                 "1--E---------------1",
                 "1111111------1111111"],

                ["1111111------1111111",
                 "1-----1--E---1-----1",
                 "1-----1------1--E--1",
                 "--------------------",
                 "----------E---------",
                 "1-S---1------1---E-1",
                 "1-----1------1-----1",
                 "11111111111111111111"],
               
                ["1111111------1111111",
                 "1------------------1",
                 "1----------E---1---1",
                 "-----11111111111--E-",
                 "-----1--------------",
                 "1------------E-----1",
                 "1---E--------------1",
                 "11111111111111111111"],

                 ["11111111111111111111",
                  "1------------------1",
                  "1--------------E---1",
                  "--------111--------1",
                  "----11111111111-E--1",
                  "1--------E---------1",
                  "1---E--------------1",
                  "11111111111111111111"],

                 ["11111111111111111111",
                  "1------------------1",
                  "1--S-------E-------1",
                  "-----1--------1-----",
                  "-----1----E---1-----",
                  "1---------------E--1",
                  "1----E-------------1",
                  "11111111111111111111"],

                 ["-11---11--1---1-1111",
                  "1----1--1-11-11-1---",
                  "1-11-1111-1-1-1-111-",
                  "1--1-1--1-1---1-1---",
                  "-11--1--1-1---1-1111",
                  "-22--2--2-222-2222--",
                  "2--2-2--2-2---2---2-",
                  "2--2-2--2-22--2222--",
                  "2--2-2--2-2---2---2-",
                  "-22---22--222-2----2",
                  ],

                 ["111-2-----2------1--",
                  "1--1-2-111-2-111-1--",
                  "111-----1----1---1-1",
                  "1--1---1-----1---11-",
                  "111----111---1---1-1",
                  "--------------------",
                  "--2-2--111-1-1------",
                  "--222--1-1-1-1------",
                  "----2--111--11------",
                  "----2--1-----1------",
                  ]
                 ]

class Block(object):
    def __init__(self, window, color, width, height, X, Y):
        self.window = window
        self.color = color
        self.width = width
        self.height = height
        self.X = X
        self.Y = Y

        pygame.draw.rect(self.window, self.color, [self.X, self.Y, self.width, self.height])

        self.hitbox = pygame.Rect(self.X, self.Y, self.width, self.height)

    def __str__(self):
        return "A simple block object."

blocks = []

class Marker(object):
    def __init__(self, window, X, Y):
        self.window = window
        self.x = X
        self.y = Y
        self.color = cs.black["pygame"]

        pygame.draw.rect(self.window, self.color, [self.x, self.y, 1, 1])

    def __str__(self):
        return "A marker for initial enemy placement."

#currentLevel = random.randrange(0, len(ROOMPATTERNS)-1)
currentLevel = random.randrange(1, 12)
levelmap = ""

class Player(character.Character):
    RECHARGE = 30
    def __init__(self, window, posx, posy):
        super().__init__(window, posx, posy)
        self.lives = 3
        self.score = 0
        self.deathstrip = [pygame.image.load(os.path.join("player", f"player_death_{i}.png")) for i in range(0, 13)]
        self.deathframe = 0
        self.ashframe = 0
        self.deathloop = 0
        self.deathscene = True
        self.deathfactor = 1
        self.pulsetimer = 0
        self.gotim = pygame.mixer.Sound(os.path.join("sounds", "player_killed.wav"))
        self.walldeath = pygame.mixer.Sound(os.path.join("sounds", "wall_death.wav"))


    def die(self, deathtype):
        self.die_anim(deathtype)


    def die_anim(self, death):
        self.deathscene = True
        if death == "shot":
            self.gotim.play()
        elif death == "wall":
            self.walldeath.play()



        self.window.blit(self.deathstrip[self.deathframe], (self.posX, self.posY))
        self.deathframe += 1

        if self.deathframe > 12:
            self.deathframe = 12
            self.deathscene = False





    def move(self, direction):
        if self.alive:
            super().move(direction)
            self.hitbox.move(self.posX, self.posY)




    def fire(self, direction = "right"):
        if player.isfiring:
            shooting = pygame.image.load(os.path.join("player", f"player_shoot_{direction}.png"))
            self.window.blit(shooting, (self.posX, self.posY))
            if len(bulletlist) < 1:
                if direction == "right":
                    bulletlist.append(weapon.Weapon(bulletspeed, cs.tangelo["pygame"], self.posX + player.get_width(), self.posY + 23, 30, 7, direction))
                if direction == "left":
                    bulletlist.append(weapon.Weapon(bulletspeed, cs.tangelo["pygame"], self.posX - 30, self.posY + 23, 30, 7, direction))
                if direction == "up" or direction == "down":
                    bulletlist.append(
                        weapon.Weapon(bulletspeed, cs.tangelo["pygame"], self.posX + player.get_width(), self.posY + 23, 30, 7, direction))


                self.pew.play()





    def controller(self):
        global whatkilledit, cooldown
        keys = pygame.key.get_pressed()
        if self.alive:
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
                cooldown -= 1


            if keys[pygame.K_x]:
                self.alive = False
                whatkilledit = "wall"




class Enemy(enemy.Cylon):
    def __init__(self, window, posX, posY, color, speed):
        super().__init__(window, posX, posY, color, speed)

        self.fire_countdown = random.randrange(30, 300)
        self.fire_speed = 5
        self.pew = pygame.mixer.Sound(os.path.join("sounds", "enemy_fire.wav"))



    def fire(self, direction):
        BUFFER = 20
        if len(enemybulletlist) <= 1:
            if direction == "left":
                enemybulletlist.append(weapon.Weapon(self.fire_speed, cs.cornflower_blue["pygame"], self.posX - self.width / 2, self.posY + 20, 30,7,direction))
            if direction == "right":
                enemybulletlist.append(
                    weapon.Weapon(self.fire_speed, cs.cornflower_blue["pygame"], self.posX + self.width, self.posY + 20, 30, 7,
                                direction))
            if direction == "up":
                enemybulletlist.append(
                    weapon.Weapon(self.fire_speed, cs.cornflower_blue["pygame"], self.posX + 10, self.posY - BUFFER, 30, 7, direction))
            if direction == "down":
                enemybulletlist.append(
                    weapon.Weapon(self.fire_speed, cs.cornflower_blue["pygame"], self.posX + 10, self.posY + self.height + BUFFER, 30, 7,
                                direction))
        else:
            pass



#construction block
M_list = []
levelnumber = 0


def drawlevel(number):
    global blocks, levelmap, M_list, thislevel, levelnumber
    levelmap = ROOMPATTERNS[number]
    e_count = 0
    w, h = 50, 80
    x, y = 0, 0

    for row in levelmap:
        for col in row:
            if col == "1":
                blocks.append(Block(WINDOW, cs.cornflower_blue["pygame"], w, h, x, y))
            if col == "2":
                blocks.append(Block(WINDOW, cs.tangelo["pygame"], w, h, x, y))
            if col == "E":
                e_count += 1
                while len(enemycoordinates) < e_count:
                    enemycoordinates.append([x,y])

            x += w
        y += h
        x = 0

    levelnumber = number



def getenemies():
    global enemylist
    for i in range(0, len(enemycoordinates)):
        enemylist.append(Enemy(WINDOW, enemycoordinates[i][0], enemycoordinates[i][1], random.choice(enemycolors), 5))



player = Player(WINDOW,100, 100)



inplay = True
FPS = 60
clock = pygame.time.Clock()
waittime = 0
move_direction = ""

def drawlives():
    pass


def startscreen():
    ontitle = True

    while ontitle:
        threadfunc(clock.tick(FPS))

        WINDOW.blit(TITLEIMAGE, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ontitle = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_HOME]:
            storyscreen()
        if keys[pygame.K_ESCAPE]:
            pygame.display.quit()
            pygame.quit()


        pygame.display.update()
        WINDOW.fill(cs.black["pygame"])


def gameover():
    gameover = True

    display_font = pygame.font.Font(os.path.join("fonts", "arcade_font.ttf"), 20)
    show_score = display_font.render(f"Your Score: {player.score}", 1, cs.white["pygame"])

    while gameover:
        clock.tick(FPS)
        clearlists()

        WINDOW.blit(DEATH, (0, 0))
        WINDOW.blit(show_score, (346, 400))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.display.quit()
            pygame.quit()
        if keys[pygame.K_RETURN]:
            player.score = 0
            startscreen()

        pygame.display.update()
        threadfunc(WINDOW.fill(cs.black["pygame"]))




def storyscreen():
    onstory = True
    global currentLevel

    while onstory:
        clock.tick(FPS)

        WINDOW.blit(STORY, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ontitle = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            player.posX, player.posY, player.hitbox.x, player.hitbox.y = 100, 100, 100, 100
            currentLevel = random.randrange(1, len(ROOMPATTERNS) - 2)
            player.alive = True
            maingame()
        if keys[pygame.K_ESCAPE]:
            pygame.display.quit()
            pygame.quit()


        pygame.display.update()
        WINDOW.fill(cs.black["pygame"])


def pause():
    paused = True
    global currentLevel

    while paused:
        clock.tick(FPS)

        WINDOW.blit(PAUSE, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ontitle = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_PAUSE]:
            currentLevel = random.randrange(1, len(ROOMPATTERNS) - 2)
            player.alive = True
            clearlists()
            player.posX, player.posY = 100, 100
            maingame()
        if keys[pygame.K_ESCAPE]:
            pygame.display.quit()
            pygame.quit()

        pygame.display.update()
        WINDOW.fill(cs.black["pygame"])


for i in range(0, len(enemylist)):
    movetimers.append(random.randrange(FPS, FPS * 5))

#(WINDOW, 24, 687, 39)
gui = GUIDisplay(WINDOW, 24, 680, 30)
bonusDisplay = ScoreDisplay(WINDOW, 24, 720, 30, timer = FPS * 3)



def clearlists():
    global enemylist, blocks, bulletlist, enemybulletlist, enemycoordinates
    enemylist = []
    enemycoordinates = []
    blocks = []
    bulletlist = []
    enemybulletlist = []



life = Life(WINDOW)



def levelup():
    global level
    if player.score % 2000 == 0:
        level += 1




def maingame():
    global inplay, cooldown
    global whatkilledit, move_direction

    

    player.alive = True



    drawlevel(currentLevel)
    getenemies()



    def getnextroom():
        global currentLevel, blocks
        clearlists()
        player.alive = True
        player.posX = 100
        player.posY = 100
        player.hitbox.x, player.hitbox.y = player.posX, player.posY
        currentLevel = random.randrange(1, len(ROOMPATTERNS)-2)
        drawlevel(currentLevel)
        getenemies()
        life.draw()





    def timer():
        global waittime
        cooldown = random.randrange(FPS, FPS * 10)
        waittime += 1

        if waittime >= cooldown:
            waittime = 0


    def redrawelements():
        global inplay
        global FPS

        threadfunc(drawlevel(currentLevel))




        for bullet in bulletlist:
            threadfunc(bullet.draw(WINDOW))
            threadfunc(bullet.update(bullet.direction))


        for enemy in enemylist:
            threadfunc(enemy.draw())

        for enemybullet in enemybulletlist:
            threadfunc(enemybullet.draw(WINDOW))

        if not player.alive:
            player.die_anim(whatkilledit)
            if not player.deathscene:
                gameover()
        else:
            player.draw(player.currentdirection, vertical=player.orientation, moving=player.moving,
                        firing=player.isfiring)




    while inplay:
        clock.tick(FPS)
        player.controller()
        threadfunc(redrawelements())
        threadfunc(gui.draw(f"SCORE: {player.score}"))

         #difficulty management
        ##increase enemy bullet speed
        movespeed = 2
        if player.score > 5000:
            for enemy in enemylist:
                enemy.fire_speed = 8
                movespeed = 3
        if player.score > 10000:  #max level
            for enemy in enemylist:
                enemy.fire_speed = 10


    


        # enemy movement
        def checkWalk(element):
            # To be used within a FOR loop within a list to check for walking eligibility
            if player.posX < element.posX and player.posY == element.posY and player.posY <= element.posY + element.height:
                element.iswalking = True
                element.posX -= movespeed
                element.hitbox.x -= movespeed
                element.move()
            elif player.posX > element.posX and player.posY == element.posY and player.posY <= element.posY + element.height:
                element.iswalking = True
                element.posX += movespeed
                element.hitbox.x += movespeed
                element.move()
            elif player.posY < element.posY and player.posX == element.posX and player.posX <= element.posX + element.width:
                element.iswalking = True
                element.posY -= movespeed
                element.hitbox.y -= movespeed
            elif player.posY > element.posY and player.posX == element.posX and player.posX <= element.posX + element.width:
                element.iswalking = True
                element.posY += movespeed
                element.hitbox.y += movespeed
                element.move()
            else:
                element.iswalking = False



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inplay = False
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
                cooldown = 30



        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.display.quit()
            pygame.quit()
        if keys[pygame.K_PAUSE]:
            pause()


        if player.posX > roomsizeX or player.posX < -45 or player.posY > roomsizeY - 200 or player.posY < -45:
            getnextroom()


        # all collisions
        for bullet in bulletlist[:]:
            if bullet.x > roomsizeX or bullet.x < 0 - bullet.w:
                bulletlist.remove(bullet)
            if bullet.y > roomsizeY  or bullet.y < 0 - bullet.h:
                bulletlist.remove(bullet)

        for bullet in enemybulletlist[:]:
            if bullet.x > roomsizeX or bullet.x < 0 - bullet.w:
                enemybulletlist.remove(bullet)
            if bullet.y > roomsizeY  or bullet.y < 0 - bullet.h:
                enemybulletlist.remove(bullet)



        for block in blocks[:]:
            if block.hitbox.colliderect(player.hitbox):
                if player.alive:
                    player.die("wall")
                    player.alive = False
            for bullet in bulletlist[:]:
                if bullet.hitbox.colliderect(block.hitbox):
                    bulletlist.remove(bullet)
            for bullet in enemybulletlist[:]:
                if bullet.hitbox.colliderect(block.hitbox):
                    enemybulletlist.remove(bullet)

        try:
            for bullet in enemybulletlist[:]:
                if bullet.hitbox.colliderect(player.hitbox):
                    if player.alive:
                        player.die("shot")
                        player.alive = False
                        enemybulletlist.remove(bullet)
        except ValueError:
            continue



        for bullet in bulletlist:
            for enemy in enemylist[:]:
                if bullet.hitbox.colliderect(enemy.hitbox):
                    enemy.blowup()
                    deathsound.play()
                    bulletlist.remove(bullet)
                    enemy.isalive = False
                    scorelist.append(ScoreDisplay(WINDOW, enemy.posX, enemy.posY, 14, FPS))
                if not enemy.isalive:
                    explosionlist.append(boom.Explosion(WINDOW, enemy.posX, enemy.posY))
                    enemylist.remove(enemy)
                    player.score += killpoints
                if len(enemylist) <= 0:
                    player.score += roomclearpoints


        for bullet in enemybulletlist:
            for enemy in enemylist[:]:
                if bullet.hitbox.colliderect(enemy.hitbox):
                    enemy.blowup()
                    deathsound.play()
                    enemybulletlist.remove(bullet)
                    enemy.isalive = False
                    scorelist.append(ScoreDisplay(WINDOW, enemy.posX, enemy.posY, 14, FPS))
                if not enemy.isalive:
                    explosionlist.append(boom.Explosion(WINDOW, enemy.posX, enemy.posY))
                    enemylist.remove(enemy)
                    player.score += killpoints
                if len(enemylist) <= 0:
                    player.score += roomclearpoints


        for block in blocks[:]:
            for enemy in enemylist[:]:
                if block.hitbox.colliderect(enemy.hitbox):
                    if enemy.isalive:
                        enemy.isalive = False
                        enemy.blowup()
                        deathsound.play()
                        scorelist.append(ScoreDisplay(WINDOW, enemy.posX, enemy.posY, 14, FPS))
                    if not enemy.isalive:
                        explosionlist.append(boom.Explosion(WINDOW, enemy.posX, enemy.posY))
                        enemylist.remove(enemy)
                        player.score += killpoints
                if len(enemylist) <= 0:
                    player.score += roomclearpoints

        for enemy in enemylist[:]:
            direction = ""
            if player.hitbox.colliderect(enemy.hitbox):
                player.die("shot")
                player.alive = False

            #Enemy moves only within "line of sight"
            if player.score >= 2500 and enemy.color == enemycolors[2]:
                checkWalk(enemy)
            #Enemy chases player when player is moving
            if (player.score >= 4000 and player.moving and enemy.color == enemycolors[1]) or (player.score >= 10000 and enemy.color == enemycolors[2]):
                if player.posX < enemy.posX or player.posY == enemy.posY and player.posY <= enemy.posY + enemy.height:
                    enemy.iswalking = True
                    enemy.posX -= movespeed
                    enemy.hitbox.x -= movespeed
                    enemy.move()
                elif player.posX > enemy.posX or player.posY == enemy.posY and player.posY <= enemy.posY + enemy.height:
                    enemy.iswalking = True
                    enemy.posX += movespeed
                    enemy.hitbox.x += movespeed
                    enemy.move()
                elif player.posY < enemy.posY and player.posX == enemy.posX or player.posX <= enemy.posX + enemy.width:
                    enemy.iswalking = True
                    enemy.posY -= movespeed
                    enemy.hitbox.y -= movespeed
                    enemy.move()
                elif player.posY > enemy.posY and player.posX == enemy.posX or player.posX <= enemy.posX + enemy.width:
                    enemy.iswalking = True
                    enemy.posY += movespeed
                    enemy.hitbox.y += movespeed
                    enemy.move()
                else:
                    enemy.iswalking = False
            #Enemy chases player, whether or not player is moving
            if player.score >= 10000 and enemy.color == enemycolors[1]:
                if player.posX < enemy.posX or player.posY == enemy.posY and player.posY <= enemy.posY + enemy.height:
                    enemy.iswalking = True
                    enemy.posX -= movespeed
                    enemy.hitbox.x -= movespeed
                    enemy.move()
                elif player.posX > enemy.posX or player.posY == enemy.posY and player.posY <= enemy.posY + enemy.height:
                    enemy.iswalking = True
                    enemy.posX += movespeed
                    enemy.hitbox.x += movespeed
                    enemy.move()
                elif player.posY < enemy.posY and player.posX == enemy.posX or player.posX <= enemy.posX + enemy.width:
                    enemy.iswalking = True
                    enemy.posY -= movespeed
                    enemy.hitbox.y -= movespeed
                    enemy.move()
                elif player.posY > enemy.posY and player.posX == enemy.posX or player.posX <= enemy.posX + enemy.width:
                    enemy.iswalking = True
                    enemy.posY += movespeed
                    enemy.hitbox.y += movespeed
                    enemy.move()
                else:
                    enemy.iswalking = False
        


            #Firing at the player
            if len(enemybulletlist) < 5:
                #left view
                if player.posX < enemy.posX and player.posY == enemy.posY and player.posY <= enemy.posY + enemy.height:
                    direction = "left"
                #right view
                elif player.posX > enemy.posX and player.posY == enemy.posY and player.posY <= enemy.posY + enemy.height:
                    direction = "right"
                #above
                elif player.posY < enemy.posY and player.posX == enemy.posX and player.posX <= enemy.posX + enemy.width:
                    direction = "up"
                #below
                elif player.posY > enemy.posY and player.posX == enemy.posX and player.posX <= enemy.posX + enemy.width:
                    direction = "down"
                else:
                    enemy.iswalking = False
                enemy.fire(direction)



        if len(enemylist) <= 0:
            bonusDisplay.draw(f"ROOM CLEAR BONUS: {roomclearpoints}")


        for explosions in explosionlist:
            explosions.blowup()
            if not explosions.isvisible:
                explosionlist.remove(explosions)


        for score in scorelist[:]:
            score.draw(f"{killpoints}")
            if score.timer == 0:
                scorelist.remove(score)


        for bullet in enemybulletlist:
            bullet.update(direction)

        #If no more enemies on the screen,
        #clear the enemy bullet list
        if len(enemylist) == 0:
            for bullet in enemybulletlist[:]:
                enemybulletlist.remove(bullet)

        try:
            for bullet in bulletlist:
                for e_bullet in enemybulletlist[:]:
                    if bullet.hitbox.colliderect(e_bullet.hitbox):
                        bulletlist.remove(bullet)
                        enemybulletlist.remove(e_bullet)
        except ValueError:
            continue

        for bullet in enemybulletlist:
            if bullet.x < 0 or bullet.x > roomsizeX or bullet.y < 0 or bullet.y > roomsizeY:
                enemybulletlist.remove(bullet)


        levelup()

        threadfunc(pygame.display.update())
        WINDOW.fill(cs.black["pygame"])



if __name__ == "__main__":
    startscreen()
    # maingame()
