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
from collections import namedtuple

pygame.init()
pygame.font.init()

roomsizeX = 1000
roomsizeY = 800
ROOMSIZE = (roomsizeX, roomsizeY)

WINDOW = pygame.display.set_mode(ROOMSIZE)
pygame.display.set_caption("Room Constructor and Test Level")

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

movetimers = []

scorelist = []

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
        self.deathstrip = []
        self.ashstrip = []
        self.deathframe = 0
        self.ashframe = 0
        self.deathloop = 0
        self.deathscene = True
        self.deathfactor = 1
        self.pulsetimer = 0
        self.gotim = pygame.mixer.Sound(os.path.join("sounds", "player_killed.wav"))
        self.walldeath = pygame.mixer.Sound(os.path.join("sounds", "wall_death.wav"))
        for i in range(0,5):
            for j in range(0,30):
                self.deathstrip.append(pygame.image.load(os.path.join("player", f"player_death_{i}.png")))
        for i in range(5, 13):
            self.ashstrip.append(pygame.image.load(os.path.join("player", f"player_death_{i}.png")))
        for i in range(0, len(self.ashstrip)):
            self.deathstrip.append(self.ashstrip[i])




    def die(self, deathtype):
        self.die_anim(deathtype)



    def die_anim(self, death):
        zapping = True
        ashes = False
        if death == "shot":
            self.gotim.play()
        elif death == "wall":
            self.walldeath.play()

        blankimage = pygame.image.load(os.path.join("player", "player_death_12.png"))

        if self.deathscene:
            if zapping:
                self.window.blit(self.deathstrip[self.deathframe], (self.posX, self.posY))
                self.deathframe += 1
                if self.deathframe >= len(self.deathstrip):
                    zapping = False
                    ashes = True
            if ashes:
                self.deathframe = 0
                self.window.blit(self.ashstrip[self.deathframe], (self.posX, self.posY))
                self.deathframe += 1
                if self.deathframe >= len(self.ashstrip):
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
    for i in range(0, len(enemycoordinates)):
        enemylist.append(Enemy(WINDOW, enemycoordinates[i][0], enemycoordinates[i][1], "blue", 5))



player = Player(WINDOW,100, 100)



inplay = True
FPS = 35
clock = pygame.time.Clock()
waittime = 0
move_direction = ""



def gameover():
    global currentLevel
    currentLevel = -1
    gameover = True
    while gameover:
        clock.tick(FPS)
        drawlevel(currentLevel)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            gameover = False



        pygame.display.update()
        WINDOW.fill(cs.black["pygame"])

##Enemy declaration

drawlevel(currentLevel)
getenemies()
for i in range(0, len(enemylist)):
    movetimers.append(random.randrange(FPS, FPS * 5))

#(WINDOW, 24, 687, 39)
gui = GUIDisplay(WINDOW, 24, 680, 30)
bonusDisplay = ScoreDisplay(WINDOW, 24, 720, 30, timer = FPS * 3)

def maingame():
    global inplay, cooldown
    global whatkilledit, move_direction



    def timer():
        global waittime
        cooldown = random.randrange(FPS, FPS * 10)
        waittime += 1

        if waittime >= cooldown:
            waittime = 0


    def redrawelements():
        global inplay
        global FPS

        drawlevel(currentLevel)



        for bullet in bulletlist:
            bullet.draw(WINDOW)
            bullet.update(bullet.direction)


        for enemy in enemylist:
            enemy.draw()

        for enemybullet in enemybulletlist:
            enemybullet.draw(WINDOW)

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
        redrawelements()
        gui.draw(f"SCORE: {player.score}")




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
            inplay = False

        # enemy firing manager


        # temporary boundry settings
        if player.posX > roomsizeX:
            player.posX = 0
        if player.posX < -45:
            player.posX = roomsizeX
        if player.posY > roomsizeY:
            player.posY = -80
        if player.posY < -80:
            player.posY = roomsizeY


        # all collisions
        for bullet in bulletlist:
            if bullet.x > roomsizeX or bullet.x < 0 - bullet.w:
                bulletlist.remove(bullet)
            if bullet.y > roomsizeY or bullet.y < 0 - bullet.h:
                bulletlist.remove(bullet)



        for block in blocks[:]:
            if block.hitbox.colliderect(player.hitbox):
                player.alive = False
                player.die("wall")
            for bullet in bulletlist[:]:
                if bullet.hitbox.colliderect(block.hitbox):
                    bulletlist.remove(bullet)
            for bullet in enemybulletlist[:]:
                if bullet.hitbox.colliderect(block.hitbox):
                    enemybulletlist.remove(bullet)

        for bullet in enemybulletlist[:]:
            if bullet.hitbox.colliderect(player.hitbox):
                if player.alive:
                    player.die("shot")
                player.alive = False
                enemybulletlist.remove(bullet)


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


        if len(enemylist) <= 0:
            bonusDisplay.draw(f"ROOM CLEAR BONUS: {roomclearpoints}")


        for explosions in explosionlist:
            explosions.blowup()
            if not explosions.isvisible:
                explosionlist.remove(explosions)

        #print(enemylist)

        for enemy in enemylist:
            if player.hitbox.colliderect(enemy.hitbox):
                player.alive = False
                player.die("shot")
            #print(enemy.isexploding)

        for score in scorelist[:]:
            score.draw(f"{killpoints}")
            if score.timer == 0:
                scorelist.remove(score)


        #Firing at the player
        for enemy in enemylist[:]:
            direction = ""
            if len(enemybulletlist) < 5:
                #left view
                if player.posX < enemy.posX and player.posY == enemy.posY and player.posY <= enemy.posY + enemy.height:
                    direction = "left"
                #right view
                if player.posX > enemy.posX and player.posY == enemy.posY and player.posY <= enemy.posY + enemy.height:
                    direction = "right"
                #above
                if player.posY < enemy.posY and player.posX == enemy.posX and player.posX <= enemy.posX + enemy.width:
                    direction = "up"
                #below
                if player.posY > enemy.posY and player.posX == enemy.posX and player.posX <= enemy.posX + enemy.width:
                    direction = "down"
                enemy.fire(direction)


        for enemy in enemylist[:]:
            direction = ""
            if player.posX < enemy.posX and player.posY == enemy.posY and player.posY <= enemy.posY + enemy.height:
                direction = "left"
                # right view
            if player.posX > enemy.posX and player.posY == enemy.posY and player.posY <= enemy.posY + enemy.height:
                direction = "right"
                # above
            if player.posY < enemy.posY and player.posX == enemy.posX and player.posX <= enemy.posX + enemy.width:
                direction = "up"
                # below
            if player.posY > enemy.posY and player.posX == enemy.posX and player.posX <= enemy.posX + enemy.width:
                direction = "down"
            else:
                enemy.iswalking = False



        for bullet in enemybulletlist:
            bullet.update(direction)

        #If no more enemies on the screen,
        #clear the enemy bullet list
        if len(enemylist) == 0:
            for bullet in enemybulletlist[:]:
                enemybulletlist.remove(bullet)

        for bullet in bulletlist:
            for e_bullet in enemybulletlist[:]:
                if bullet.hitbox.colliderect(e_bullet.hitbox):
                    bulletlist.remove(bullet)
                    enemybulletlist.remove(e_bullet)

        for bullet in enemybulletlist:
            if bullet.x < 0 or bullet.x > roomsizeX or bullet.y < 0 or bullet.y > roomsizeY:
                enemybulletlist.remove(bullet)








        pygame.display.update()
        WINDOW.fill(cs.black["pygame"])



if __name__ == "__main__":
    maingame()
