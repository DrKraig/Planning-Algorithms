import pygame
import math
import heapq
import time
import functools

import sys, pygame
from pygame.locals import*

width=1000
height=500
Color_screen=(49,150,100)
Color_line=(255,0,0)

def main():
    screen=pygame.display.set_mode((width,height))
    screen.fill(Color_screen)
    pygame.draw.line(screen, Color_line, (60.25, 80.55), (130.73, 100.93))
    pygame.draw.line(screen, (0,255,0), (65.75, 80.55), (130.73, 100.93))
    pygame.display.flip()
    while True:
        for events in pygame.event.get():
            if events.type == QUIT:

                sys.exit(0)
main()
pygame.display.flip()

