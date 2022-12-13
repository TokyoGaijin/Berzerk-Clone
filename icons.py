import pygame
import colorswatch as cs

class block(object):
    def __init__(self, window, color, X, Y):
        self.window = window
        self.color = color
        self.X = X
        self.Y = Y
        pygame.draw.rect(self.window, self.color,[self.X, self.Y, 7, 7])



icons = [["--11---",
          "--11---",
          "-------",
          "-1111--",
          "1-11-1-",
          "1-11-1-",
          "--11---",
          "--11---",
          "--11---",
          "--11---",
          "--111--"]]

pygame.init()
roomsize = (56, 80)
window = pygame.display.set_mode(roomsize)
clock = pygame.time.Clock()
FPS = 30

display = True
while display:
    clock.tick(FPS)
    blocklist = []
    icon = icons[0]
    x, y, = 0, 0

    for row in icon:
        for col in row:
            if col == "1":
                blocklist.append(block(window, cs.tangelo["pygame"], x, y))
            x += 7
        y += 7
        x = 0

        pygame.display.update()
        window.fill(cs.black["pygame"])