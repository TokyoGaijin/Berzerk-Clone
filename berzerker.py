import rooms
import pygame
import random
import colorswatch as cs
import chara
import os
import weapon
import cylon as enemy
import explosion as boom
import pygame.freetype
import threading #just in case
from enum import Enum

pygame.init()
pygame.font.init()

# Constants
roomsizeX, roomsizeY = 1000, 800
ROOMSIZE = (roomsizeX, roomsizeY)
WINDOW = pygame.display.set_mode(ROOMSIZE)
TITLEIMAGE = pygame.image.load(os.path.join("othergrafix", "TitleScreen.png"))
STORY = pygame.image.load(os.path.join("othergrafix", "storyscreen.png"))
PAUSE = pygame.image.load(os.path.join("othergrafix", "pausescreen.png"))
DEATH = pygame.image.load(os.path.join("othergrafix", "deathscreen.png"))
ROOMPATTERNS = rooms.ROOMPATTERNS


# Set up the game states
class GameState(Enum):
    TITLE = 0
    STORY = 1
    IN_PLAY = 2
    GAME_OVER = 3

# GUI Classes
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

# Board elements
class Block(object):
    def __init__(self, window, color, width, height, x, y):
        self.window = window
        self.color = color
        self.width = width
        self.height = height
        self.x = x
        self.y = y

        pygame.draw.rect(self.window, self.color, [self.x, self.y, self.width, self.height])

        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def __str__(self):
        return "A simple block object."

class Marker(object):
    def __init__(self, window, x, y):
        self.window = window
        self.x = x
        self.y = y
        self.color = cs.black["pygame"]

        pygame.draw.rect(self.window, self.color, [self.x, self.y, 1, 1])

    def __str__(self):
        return "A marker for initial enemy placement."

# Interactive elements: Player and Enemy
class Player(chara.Character):
    RECHARGE = 30
    def __init__(self, window, posX, posY):
        super().__init__(window, posX, posY)
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
        self.deathscne = True
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
        if self.isfiring:
            shooting = pygame.image.load(os.path.join("player", f"player_shoot_{direction}.png"))
            self.window.blit(shooting, (self.posX, self.posY))
            if len(bulletlist) < 1:
                if direction == "right":
                    bulletlist.append(weapon.Weapon(bulletspeed, cs.tangelo["pygame"], self.posX + self.get_width(), self.posY + 23, 30, 7, direction))
                if direction == "left":
                    bulletlist.append(weapon.Weapon(bulletspeed, cs.tangelo["pygame"], self.posX - 30, self.posY + 23, 30, 7, direction))
                if direction == "up" or direction == "down":
                    bulletlist.append(weapon.Weapon(bulletspeed, cs.tangelo["pygame"], self.posX + self.get_width(), self.posY + 23, 30, 7, direction))
            
            self.pew.play()

    def controller(self):

        keys = pygame.key.get_pressed()

        global whatkilledit, cooldown

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

# Variables
# Declared
whatkilledit = None
bulletspeed = 10
enemycolors = ["blue", "yellow", "gray"]
cooldown = 30
killpoints = 100
roomclearpoints = 500
level = 1
currentLevel = random.randrange(1, len(ROOMPATTERNS))
levelnumber = 0
inPlay = True
FPS = 60
waittime = 0
current_state = None

# Empties
bulletlist = []
enemylist = []
enemybulletlist = []
enemycoordinates = []
explosionlist = []
movetimers = []
scorelist = []
blocks = []
M_list = []
move_direction = None
levelmap = None

# Class Iterations and Objects
keys = pygame.key.get_pressed()
player = Player(WINDOW, 100, 100)
gui = GUIDisplay(WINDOW, 24, 680, 30)
bonusDisplay = ScoreDisplay(WINDOW, 24, 720, 30, timer = FPS * 3)
clock = pygame.time.Clock()
deathsound = pygame.mixer.Sound(os.path.join("sounds", "death.wav"))

for i in range(0, len(enemylist)):
    movetimers.append(random.randrange(FPS, FPS * 5))

# In-Game Functions
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

def clearlists():
    global enemylist, blocks, bulletlist, enemybulletlist, enemycoordinates
    enemylist = []
    enemycoordinates = []
    blocks = []
    enemybulletlist = []

def levelup():
    global level
    if player.score % 2000 == 0:
        level += 1

def getnextroom():
    global currentLevel, blocks
    clearlists()
    player.alive = True
    player.posX, player.posY = 100, 100
    player.hitbox.x, player.hitbox.y = player.posX, player.posY
    currentLevel = random.randrange(1, len(ROOMPATTERNS) -2)
    drawlevel(currentLevel)
    getenemies()


def checkWalk(element):
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




def draw():
    global inplay, FPS, current_state




    if current_state == GameState.IN_PLAY:
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
                current_state = GameState.GAME_OVER
        else:
            player.draw(player.currentdirection, vertical = player.orientation, moving = player.moving, firing = player.isfiring)
            gui.draw(f"SCORE: {player.score}")

        for score in scorelist[:]:
            score.draw(f"{killpoints}")



    if current_state == GameState.TITLE:
        WINDOW.blit(TITLEIMAGE, (0, 0))

    if current_state == GameState.STORY:
        WINDOW.blit(STORY, (0,0))

    if current_state == GameState.GAME_OVER:
        display_font = pygame.font.Font(os.path.join("fonts", "arcade_font.ttf"), 20)
        show_score = display_font.render(f"Your score: {player.score}", 1, cs.white["pygame"])
        WINDOW.blit(DEATH, (0, 0))
        WINDOW.blit(show_score, (346, 400))





def update():
    global inPlay, currentLevel, movespeed, current_state
    global bulletlist, enemybulletlist
    

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_ESCAPE]:
        pygame.display.quit()
        pygame.quit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
            pygame.quit()
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



    if current_state == GameState.IN_PLAY:
       
        player.controller()
        

        if player.score % 5000:
            for enemy in enemylist:
                enemy.fire_speed += 8
                movespeed += 3

                if enemy.fire_speed >= 10:
                    enemy.fire_speed = 10
                if movespeed >= 6:
                    movespeed = 6

       
        if player.posX > roomsizeX or player.posX < -45 or player.posY > roomsizeY - 200 or player.posY < -45:
            currentLevel = random.randrange(1, 12)

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
            pass # May need to be continued

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
            if score.timer == 0:
                scorelist.remove(score)

        for bullet in enemybulletlist:
            bullet.update(direction)

        if len(enemylist) == 0:
            enemybulletlist = []

        try:
            for bullet in bulletlist:
                for e_bullet in enemybulletlist[:]:
                    if bullet.hitbox.colliderect(e_bullet.hitbox):
                        bulletlist.remove(bullet)
                        enemybulletlist.remove(e_bullet)
        except ValueError:
            pass

        levelup()

            
    if current_state == GameState.TITLE:
        if keys[pygame.K_HOME] or keys[pygame.K_RETURN]:
            current_state = GameState.STORY

    if current_state == GameState.STORY:
        if keys[pygame.K_RETURN]:
            player.posX, player.posY, player.hitbox.x, player.hitbox.y = 100, 100, 100, 100
            currentLevel = random.randrange(1, len(ROOMPATTERNS) - 2)
            player.isAlive = True
            current_state = GameState.IN_PLAY
  
    if current_state == GameState.GAME_OVER:
        if keys[pygame.K_RETURN]:
            player.score = 0
            current_state = GameState.TITLE
       


    pygame.display.update()
    WINDOW.fill(cs.black["pygame"])



def maingame(gameState):
    global current_state, movespeed
    current_state = gameState
    clock.tick(FPS)
    movespeed = 2
   
    getenemies()
    #drawlevel(currentLevel)

    while inPlay:
        draw()
        update()


if __name__ == "__main__":
    maingame(GameState.TITLE)


