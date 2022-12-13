import pygame
pygame.init()

class Character:
    def __init__(self, window, w, h):
        self.constructor(window, w, h)
        """
        Warning: Do NOT modify this particular function unless you intend
        to add arguments (not recommended.  It's recommended to pass your
        arguments into the UPDATE and DRAW methods
        """

    def constructor(self, window, w, h):
        self.patternlist = []
        self.window = window
        self.w = w
        self.h = h



    def update(self):
        pass
        #TODO: Make your frame-by-frame update arguments here.


    def draw(self, x, y, color):

        for row in self.patternlist:
            for col in row:
                if col == "1":
                    self.patternlist.append(pygame.draw.rect(self.window, color, [x, y, self.w, self.h]))
                x += self.w
            y += self.h
            x = 0



class Player(Character):

    def constructor(self, window, w, h):
        super().constructor(window, w, h)
        self.patternlist = [ ["---11---",
                              "---11---",
                              "--------",
                              "--1111--",
                              "-1-11-1-",
                              "-1-11-1-",
                              "---11---",
                              "---11---",
                              "---11---",
                              "---11---",
                              "---111--"]]

    def draw(self, x, y, color):
        super().draw(x, y, color)