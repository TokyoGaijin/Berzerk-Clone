
import pygame
import character
import colorswatch as cs


pygame.init()

# WARNING: DO NOT MODIFY THESE unless otherwise specified

sizeX = 640  # TODO: set your window width
sizeY = 480  # TODO: set your window height
ROOMSIZE = (sizeX, sizeY)

# The Window
WINDOW = pygame.display.set_mode(ROOMSIZE)
pygame.display.set_caption("Testing Field")
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
        self.player = character.Player(WINDOW, 56, 80)
        self.gameon = True

        # Update Ticker
        self.FPS = 60


    def draw(self):
        self.player.draw(sizeX / 2, sizeY / 2, cs.tangelo["pygame"])


    def update(self):
        while self.gameon:
            CLOCK.tick(self.FPS)

            self.draw()

            # Event handling the closing of the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameon = False



            pygame.display.update()
            WINDOW.fill(cs.black["pygame"])


# Activates and plays the game
# WARNING: DO NOT MODIFY UNLESS ABSOLUTELY NECESSARY
game = Game()
if __name__ == "__main__":
    game.update()
    print(character.patternlist)

