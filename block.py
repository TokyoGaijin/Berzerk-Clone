import pygame
#TODO: Import necessary libraries here

class Block(object):
	def __init__(self, window, color, width, height, x, y):
		self.constructor(window, color, width, height, x, y)
		"""
		Warning: Do NOT modify this particular function unless you intend
		to add arguments (not recommended.  It's recommended to pass your
		arguments into the UPDATE and DRAW methods
		"""

	def constructor(self, window, color, width, height, x, y):
		self.window = window
		self.color = color
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.hitbox = None


	def update(self):
		pass
		#TODO: Make your frame-by-frame update arguments here.


	def draw(self):
		pygame.draw.rect(self.window, self.color, [self.x, self.y, self.width, self.height])
		self.hitbox = pygame.Rect(self.x, self.y, self.x+self.width, self.y+self.height)