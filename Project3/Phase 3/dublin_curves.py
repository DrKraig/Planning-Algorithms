import pygame
import math


# Defining Graph Constants
SCALE = 2
HEIGHT = int(1000/SCALE)
WIDTH = int(1000/SCALE)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
MAGENTA = (255, 0, 255)


def plot_curve(Xi, Yi, Thetai, UL, UR):
    t = 0
    r = 6.6/SCALE     # in cm
    L = 16.0/SCALE    # in cm
    dt = 0.01   # in sec

    # converting rpm into rps
    UL = UL/60
    UR = UR/60

    Xn = Xi
    Yn = Yi
    Thetan = 3.14 * Thetai / 180

    D = 0
    while t < 1:
        t = t + dt
        Xs = Xn
        Ys = Yn
        Xn += 0.5 * r * (UL + UR) * math.cos(Thetan) * dt
        Yn += 0.5 * r * (UL + UR) * math.sin(Thetan) * dt
        Thetan += (r / L) * (UR - UL) * dt
        pygame.draw.line(screen, MAGENTA, [Xs, HEIGHT - Ys], [Xn, HEIGHT - Yn], 2)

    Thetan = 180 * (Thetan) / 3.14
    return D

actions = [[0, 100], [100, 0], [100, 100], [0, 50], [50, 0], [50, 50], [100, 50], [50, 100]]

pygame.init()

screen = pygame.display.set_mode([WIDTH, HEIGHT])

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    for action in actions:
        X1 = plot_curve(100, 100, 0, action[0], action[1])

    pygame.display.flip()

pygame.quit()
