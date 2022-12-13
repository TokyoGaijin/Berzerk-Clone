"""
SWATCH USE
As variables: in any argument requiring a color value,
indicate the name of the color and its dictionary key.

Simply run:
    import colorswatch

Call Example:
    import colorswatch as cs

    pygame:
        import pygame
        pygame.draw.rect(display, cs.blue["pygame"], [x,y,sizeX,sizeY])
    tkinter:
        from tkinter import *
        something = label(root, text="Something", fg=cs.puke["tk"], bg=cs.cornflower_blue["tk"])
"""

cornflower_blue = {"pygame": (100,149,237), "tk": "#6495ED"}
tangelo = {"pygame": (249,77,0), "tk": "#F94D00"}
black = {"pygame": (0,0,0), "tk": "#000000"}
white = {"pygame": (255,255,255), "tk": "#FFFFFF"}
red ={"pygame": (255,0,0), "tk": "#FF0000"}
green ={"pygame": (0,255,0), "tk": "#00FF00"}
blue = {"pygame": (0,0,255), "tk": "#000FF"}
fuchsia = {"pygame": (255,25,255), "tk": "#FF19FF"}
puke = {"pygame": (68,102,0), "tk": "#446600"}
sky_blue = {"pygame":(51,153,255), "tk": "#3399FF"}
mustard = {"pygame": (255,255,77), "tk": "#FFE14D"}
gold = {"pygame": (204,170,0), "tk": "#CCAA00"}
purple_rain = {"pygame": (106,77,255), "tk": "#6A4DFF"}
bile = {"pygame": (0,102,17), "tk": "#006611"}
golden_shower = {"pygame": (204,204,0), "tk": "#CCCC00"}
shit = {"pygame": (77,51,0), "tk": "#4D3300"}
gray = {"pygame": (150,150,150), "tk": "#969696"}