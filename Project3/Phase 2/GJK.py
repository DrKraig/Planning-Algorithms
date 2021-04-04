import numpy as np
from math import pi
import time
import cv2


def vec3prod(A, B, C):
    dp1 = np.dot(A, C)
    dp2 = np.dot(A, B)
    tp = dp1*A - dp2*C
    return tp


class Circle:

    def __init__(self, xcord, ycord, radius):
        self.center = np.array([xcord, ycord])
        self.r = radius

    def sf(self, sv):
        direction = np.array(sv)
        x = self.center[0] + self.r*direction[0]
        y = self.center[1] + self.r*direction[1]
        point = np.array([x, y])
        return point


class Ellipse:

    def __init__(self, xcord, ycord, xaxis, yaxis):
        self.center = np.array([xcord, ycord])
        self.a = xaxis
        self.b = yaxis

    def sf(self, sv):
        direction = np.array(sv)
        x = self.center[0] + self.a*direction[0]
        y = self.center[1] + self.b*direction[1]
        point = np.array([x, y])
        return point


class Rect:

    def __init__(self, corners):
        self.vertex = np.array(corners)
        self.center = self.vertex.sum(axis=0)/4

    def sf(self, sv):
        direction = np.array(sv)
        dp = np.dot(self.vertex, direction)
        point = np.array(self.vertex[np.argmax(dp)])
        return point


def support(shape1, shape2, sv):
    direction = np.array(sv)
    support_point = shape1.sf(direction) - shape2.sf(-direction)
    return support_point


def handleSimplex(simplex, svl):
    if len(simplex) == 2:
        return lineCase(simplex, svl)
    return triangleCase(simplex, svl)


def lineCase(simplex, svl):
    pB = np.array(simplex[0])
    pA = np.array(simplex[1])
    pAB = pB - pA
    pABp = vec3prod(pAB, -pA, pAB)
    pABp = pABp/np.linalg.norm(pABp)
    svl.clear()
    svl.append(pABp.tolist())
    return 0


def triangleCase(simplex, svl):
    pC = np.array(simplex[0])
    pB = np.array(simplex[1])
    pA = np.array(simplex[2])
    pAB = pB - pA
    pAC = pC - pA
    pABp = vec3prod(pAC, pAB, pAB)
    pACp = vec3prod(pAB, pAC, pAC)
    if np.dot(pABp, -pA) > 0:
        simplex.pop(2)
        svl.clear()
        svl.append(pABp.tolist())
        return 0
    elif np.dot(pACp, -pA) > 0:
        simplex.pop(1)
        svl.clear()
        svl.append(pACp.tolist())
        return 0
    return 1


def gjk(s1, s2):

    d = s2.center - s1.center
    d = d/np.linalg.norm(d)
    mp = support(s1, s2, d)
    simplex = [mp.tolist()]
    d = -mp/np.linalg.norm(mp)
    while True:
        mp = support(s1,s2,d)
        if np.dot(mp, d) < 0:
            return 0
        simplex.append(mp.tolist())
        support_vector = [d.tolist()]
        if handleSimplex(simplex, support_vector):
            return 1
        d = np.array(support_vector[0])


class obstacle_space:

    def __init__(self, c):
        self.clearance = c
        self.cor1 = np.array([[192, 48], [105.956, 170.876], [89.568, 159.400], [175.613, 36.524]])
        self.cor2 = np.array([[70, 200], [70, 230], [60, 230], [60, 200]])
        self.cor3 = np.array([[60, 200], [60, 210], [30, 210], [30, 200]])
        self.cor4 = np.array([[30, 200], [30, 230], [20, 230], [20, 200]])
        self.eh = 155
        self.ek = 246
        self.ea = 30
        self.eb = 60
        self.ch = 230
        self.ck = 90
        self.radius = 35

    def chk(self, x, y):
        bot = Circle(x, y, self.clearance)
        circ = Circle(self.ch, self.ck, self.radius)
        elip = Ellipse(self.eh, self.ek, self.ea, self.eb)
        rect1 = Rect(self.cor1)
        rect2 = Rect(self.cor2)
        rect3 = Rect(self.cor3)
        rect4 = Rect(self.cor4)

        return gjk(bot, circ) or gjk(bot, elip) or gjk(bot, rect1) or gjk(bot, rect2) or gjk(bot, rect3) or gjk(bot, rect4)

o_space = obstacle_space(15)

start_time = time.time()

value = o_space.chk(i,j)

print("--- %s seconds ---" % (time.time() - start_time))
print(value)
