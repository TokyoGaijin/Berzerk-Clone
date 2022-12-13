"""
This is a typical class template for Pygame main game
classes.  Use this to organize the entirety of your
game into one main file.

The algorythm design is based off of XNA Game Studio
class structure of CONSTRUCTOR/INITIATOR, UPDATE and DRAW
methods, organized of easy and neat readability.
"""

import pygame
import colorswatch as cs

pygame.init()

#TODO: Hard-code your numbers into this class.
		#WARNING: DO NOT MODIFY THESE unless otherwise specified

sizeX = 640 #TODO: set your window width
sizeY = 480 #TODO: set your window height
ROOMSIZE = (sizeX, sizeY)

#The Window
WINDOW = pygame.display.set_mode(ROOMSIZE)
pygame.display.set_caption("Untitled") #TODO: Name your game
CLOCK = pygame.time.Clock()


class Game:
	def __init__(self):
		self.constructor()
		"""
		Will automatically call your variables and objects that you declare
		in the contructor method.

		DO NOT modify this method directly.
		"""


	def constructor(self):
		#Loop bool
		self.gameon = True #Rename to whatever you wish.  RECOMMENDED: gameloop, gameon, inplay, playing, etc.
		
		#Update Ticker
		self.FPS = 60 #TODO: NOT a constant.  Set to whatever you like

		self.imagerect = pygame.Rect(20,20,20,20)
		self.icon = None
		



	def draw(self):
		self.icon = pygame.draw.rect(WINDOW,cs.tangelo["pygame"], self.imagerect)





	def update(self):
		while self.gameon:
			CLOCK.tick(self.FPS)


			#Event handling the closing of the window
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.gameon = False


			self.draw()

			pygame.display.update()
			WINDOW.fill((0,0,0))









#Activates and plays the game
#WARNING: DO NOT MODIFY UNLESS ABSOLUTELY NECESSARY
game = Game()
if __name__ == "__main__":
	game.update()

