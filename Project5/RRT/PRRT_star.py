import pygame
import math
import heapq
import time
import functools
import random
import numpy as np


# Defining Graph Constants
HEIGHT = 300
WIDTH = 400
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Node:
    """
    Node class : This class is built to store the node information.
    A node is simply a location on a map. For each node, its neighbours, parents & distance to reach that node is stored.
    """

    def __init__(self, x, y, endX, endY):
        """
        Description: Defining all properties for each node - Neighbours, Parents, Distance.
        """
        self.x = x
        self.y = y
        self.costToCome = 0
        self.costToGo = math.sqrt((x - endX) ** 2 + (y - endY) ** 2)
        self.cost = None
        self.neighbour = {}
        self.parent = None

    def __lt__(self, other):
        return self.cost < other.cost


class Graph:

    def __init__(self, start, end):
        self.visited = {}
        self.endX = end.x
        self.endY = end.y
        self.maxDistanceForNode = 50
        self.CLEARANCE = 15

    def getSamplePoint(self):
        x = random.randint(0, 400)
        y = random.randint(0, 300)
        return Node(x, y, self.endX, self.endY)

    def isInTargetArea(self, i, j):
        """
        Description: Checks if the currentnode is in target area to terminal the program
        Input: Current Node co-ordinates
        Output: Boolean
        """
        if (i - self.endX) ** 2 + (j - self.endY) ** 2 - 100 <= 0:
            return True
        else:
            return False

    def isInCircle(self, x, y):
        """
        Description: Checks if a point is in the circle.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """
        r = 35 + self.CLEARANCE
        if (x - 90) ** 2 + (y - 70) ** 2 - r ** 2 >= 0:
            return False
        else:
            return True

    def isInRectangle(self, x, y):
        """
        Description: Checks if a point is in the rotated rectangle.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """
        circ1 = (x - 48) ** 2 + (y - 108) ** 2 <= self.CLEARANCE ** 2
        circ2 = (x - 170.876) ** 2 + (y - 194.044) ** 2 <= self.CLEARANCE ** 2
        circ3 = (x - 159.4) ** 2 + (y - 210.432) ** 2 <= self.CLEARANCE ** 2
        circ4 = (x - 36.524) ** 2 + (y - 124.387) ** 2 <= self.CLEARANCE ** 2
        side1 = 0.7 * x - y + 74.39 <= 0
        eside1 = 0.7 * x - y + 74.39 - 1.22 * self.CLEARANCE <= 0
        side2 = -1.43 * x - y + 176.55 <= 0
        eside2 = -1.43 * x - y + 176.55 - 1.74 * self.CLEARANCE <= 0
        side3 = 0.7 * x - y + 98.81 >= 0
        eside3 = 0.7 * x - y + 98.81 + 1.22 * self.CLEARANCE >= 0
        side4 = -1.43 * x - y + 438.06 >= 0
        eside4 = -1.43 * x - y + 438.06 + 1.74 * self.CLEARANCE >= 0
        rect1 = eside1 and side2 and eside3 and side4
        rect2 = side1 and eside2 and side3 and eside4

        if rect1 or rect2 or circ1 or circ2 or circ3 or circ4:
            return True
        else:
            return False

    def isInBrokenRectangle(self, x, y):
        """
        Description: Checks if a point is in the top rectangle.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        rect1 = (y <= 280 + self.CLEARANCE) and (y >= 270 - self.CLEARANCE) and (x <= 230) and (x >= 200)
        rect2 = (y <= 280) and (y >= 270) and (x <= 230 + self.CLEARANCE) and (x >= 200 - self.CLEARANCE)
        rect3 = (y <= 270) and (y >= 240) and (x <= 210 + self.CLEARANCE) and (x >= 200 - self.CLEARANCE)
        rect4 = (y <= 240 + self.CLEARANCE) and (y >= 230 - self.CLEARANCE) and (x <= 230) and (x >= 200)
        rect5 = (y <= 240) and (y >= 230) and (x <= 230 + self.CLEARANCE) and (x >= 200 - self.CLEARANCE)
        circ1 = (x - 230) ** 2 + (y - 280) ** 2 <= self.CLEARANCE ** 2
        circ2 = (x - 200) ** 2 + (y - 280) ** 2 <= self.CLEARANCE ** 2
        circ3 = (x - 230) ** 2 + (y - 270) ** 2 <= self.CLEARANCE ** 2
        circ4 = (x - 230) ** 2 + (y - 240) ** 2 <= self.CLEARANCE ** 2
        circ5 = (x - 230) ** 2 + (y - 230) ** 2 <= self.CLEARANCE ** 2
        circ6 = (x - 200) ** 2 + (y - 230) ** 2 <= self.CLEARANCE ** 2

        if rect1 or rect2 or rect3 or rect4 or rect5 or circ1 or circ2 or circ3 or circ4 or circ5 or circ6:
            return True
        else:
            return False

    def isInEllipse(self, x, y):
        """
        Description: Checks if a point is in the Ellipse.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """
        a = 60 + self.CLEARANCE
        b = 30 + self.CLEARANCE
        h = 246
        k = 145
        if ((math.pow((x - h), 2) / math.pow(a, 2)) + (math.pow((y - k), 2) / math.pow(b, 2))) <= 1:
            return True
        else:
            return False

    def isInObstacle(self, x, y):
        """
        Description: Checks if the point (x,y) is inside an obstacle or not.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """
        # return False
        return self.isInEllipse(x, y) or self.isInBrokenRectangle(x, y) or self.isInCircle(x, y) or self.isInRectangle(
            x, y)

    def isOutsideArena(self, x, y):
        """
        Description: Checks if the point (x,y) is outside the areana or not.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        return True if x < self.CLEARANCE or y < self.CLEARANCE or x > 400 - self.CLEARANCE or y > 300 - self.CLEARANCE else False

    def getNearestNeighbour(self, currentNode):

        nearestNode = None
        minDistance = float("inf")
        for node in self.visited:
            currentDistance = self.getEuclidianDistance(currentNode, node)
            if minDistance > currentDistance:
                minDistance = currentDistance
                nearestNode = node
        return nearestNode

    def getEuclidianDistance(self, nearestNode, currentNode):
        parentX = nearestNode.x
        parentY = nearestNode.y
        currentX = currentNode.x
        currentY = currentNode.y
        return math.sqrt((parentX - currentX) ** 2 + (parentY - currentY) ** 2)

    def isBranchInObstacle(self, nearestNode, currentNode):
        points = self.getPoints(nearestNode, currentNode)
        for point in points:
            x = point[0]
            y = point[1]
            if self.isInObstacle(x, y):
                return True
        return False

    def APG(self, currentNode):
        F = np.array([-2*(currentNode.x - self.endX), -2*(currentNode.y - self.endY)])
        F = F/np.linalg.norm(F)
        return F

    def RGD(self,currentNode):
        k = 100
        lam = 0.01
        ds_obs = 0.01
        for n in range(k):
            F = self.APG(currentNode)
            d_min = self.getNearestObstacle(currentNode) ## this lines needs to be changed
            if d_min <= ds_obs:
                return
            else:
                currentNode.x = currentNode.x + lam*F[0]
                currentNode.y = currentNode.y + lam*F[1]
        return

    def getEuclidianDistanceUsingPoints(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        
    def getNearestObstacle(self, currentNode):
        x = currentNode.x
        y = currentNode.y
        pointsOnObstacle = self.getAllPointsOnObstacle()
        minDistance = float("inf")
        minPoint = None
        for point in pointsOnObstacle:
            distance = self.getEuclidianDistanceUsingPoints(point[0], point[1], x,y)
            if minDistance > distance:
                minDistance = distance
                minPoint = point
        return minDistance

    def getAllPointsOnObstacle(self):

        points = []
        CLEARANCE = 0.1

        #Circle 1
        r = 1 + CLEARANCE
        for theta in np.arange(0,360):
            thetaInRadians = (math.pi * theta) /180
            x = 2 + r*math.cos(thetaInRadians)
            y = 2 + r*math.sin(thetaInRadians)
            points.append([x,y])

        #Circle 2
        r = 1 + CLEARANCE
        for theta in np.arange(0,360):
            thetaInRadians = (math.pi * theta) /180
            x = 2 + r*math.cos(thetaInRadians)
            y = 8 + r*math.sin(thetaInRadians)
            points.append([x,y])

        # #Rectangle 1
        r = CLEARANCE
        for theta in np.arange(0,360):
            thetaInRadians = (math.pi * theta) /180
            x = 0.25 + r*math.cos(thetaInRadians)
            y = 5.75 + r*math.sin(thetaInRadians)
            points.append([x,y])
        for theta in np.arange(0,360):
            thetaInRadians = (math.pi * theta) /180
            x = 1.75 + r*math.cos(thetaInRadians)
            y = 5.75 + r*math.sin(thetaInRadians)
            points.append([x,y])
        for theta in np.arange(0,360):
            thetaInRadians = (math.pi * theta) /180
            x = 0.25 + r*math.cos(thetaInRadians)
            y = 4.25 + r*math.sin(thetaInRadians)
            points.append([x,y])
        for theta in np.arange(0,360):
            thetaInRadians = (math.pi * theta) /180
            x = 1.75 + r*math.cos(thetaInRadians)
            y = 4.25 + r*math.sin(thetaInRadians)
            points.append([x,y])
        for x in np.arange(0.25 - CLEARANCE, 1.75 + CLEARANCE, 0.1):
            points.append([x,5.75]) 
        for x in np.arange(0.25 - CLEARANCE, 1.75 + CLEARANCE, 0.1):
            points.append([x,4.25])
        for y in np.arange(4.25 - CLEARANCE, 5.75 + CLEARANCE, 0.1):
            points.append([0.25,y])
        for y in np.arange(4.25- CLEARANCE, 5.75 + CLEARANCE, 0.1):
            points.append([1.75,y])

        
        #Rectangle 2
        r = CLEARANCE
        for theta in np.arange(0,360):
            thetaInRadians = (math.pi * theta) /180
            x = 3.75 + r*math.cos(thetaInRadians)
            y = 5.75 + r*math.sin(thetaInRadians)
            points.append([x,y])
        for theta in np.arange(0,360):
            thetaInRadians = (math.pi * theta) /180
            x = 6.25 + r*math.cos(thetaInRadians)
            y = 5.75 + r*math.sin(thetaInRadians)
            points.append([x,y])
        for theta in np.arange(0,360):
            thetaInRadians = (math.pi * theta) /180
            x = 3.75 + r*math.cos(thetaInRadians)
            y = 4.25 + r*math.sin(thetaInRadians)
            points.append([x,y])
        for theta in np.arange(0,360):
            thetaInRadians = (math.pi * theta) /180
            x = 6.25 + r*math.cos(thetaInRadians)
            y = 4.25 + r*math.sin(thetaInRadians)
            points.append([x,y])
        for x in np.arange(3.75 - - CLEARANCE, 6.25 + CLEARANCE, 0.1):
            points.append([x,5.75])
        for x in np.arange(3.75 - CLEARANCE, 6.25 + CLEARANCE, 0.1):
            points.append([x,3.75])
        for y in np.arange(4.25 - CLEARANCE, 5.75 + CLEARANCE, 0.1):
            points.append([3.75,y])
        for y in np.arange(4.25 - CLEARANCE, 5.75 + CLEARANCE, 0.1):
            points.append([6.25,y])

        
        #Rectangle 3
        r = CLEARANCE
        for theta in np.arange(0,360):
            thetaInRadians = (math.pi * theta) /180
            x = 7.25 + r*math.cos(thetaInRadians)
            y = 4 + r*math.sin(thetaInRadians)
            points.append([x,y])
        for theta in np.arange(0,360):
            thetaInRadians = (math.pi * theta) /180
            x = 8.75 + r*math.cos(thetaInRadians)
            y = 4 + r*math.sin(thetaInRadians)
            points.append([x,y])
        for theta in np.arange(0,360):
            thetaInRadians = (math.pi * theta) /180
            x = 8.75 + r*math.cos(thetaInRadians)
            y = 2 + r*math.sin(thetaInRadians)
            points.append([x,y])
        for theta in np.arange(0,360):
            thetaInRadians = (math.pi * theta) /180
            x = 7.25 + r*math.cos(thetaInRadians)
            y = 2 + r*math.sin(thetaInRadians)
            points.append([x,y])
        for x in np.arange(7.25 - CLEARANCE, 8.75 + CLEARANCE, 0.1):
            points.append([x,2])
        for x in np.arange(7.25 - CLEARANCE, 8.75 + CLEARANCE, 0.1):
            points.append([x,2])
        for y in np.arange(2 - CLEARANCE, 4 + CLEARANCE, 0.1):
            points.append([8.75,y])
        for y in np.arange(2 - CLEARANCE, 4+ CLEARANCE, 0.1):
            points.append([7.25, y])

        return points


    def getPoints(self, nearestNode, currentNode):
        points = []
        x1 = nearestNode.x
        y1 = nearestNode.y

        x2 = currentNode.x
        y2 = currentNode.y
        if x1 == x2:
            if y1 > y2:
                for y in np.arange(y1, y2, -1):
                    points.append([x1, y])
            elif y1 < y2:
                for y in np.arange(y1, y2):
                    points.append([x1, y])
        elif y1 == y2:

            if x1 > x2:
                for x in np.arange(x1, x2, -1):
                    points.append([x, y1])
            elif x1 < x2:
                for x in np.arange(x1, x2):
                    points.append([x, y1])
        else:
            for x in np.arange(min(x1, x2), max(x1, x2) + 1):
                for y in np.arange(min(y1, y2), max(y1, y2) + 1):
                    if y == int(((x - x1) * (y1 - y2)) / (x1 - x2) + y1):
                        points.append([x, y])
        return points

    def getRectifiedPoint(self, points, nearestNode, currentNode):
        prev = None
        print(points)
        for point in points:
            x = point[0]
            y = point[1]
            potentialNode = Node(x, y, self.endX, self.endY)
            if self.isInObstacle(x, y) or self.getEuclidianDistance(nearestNode,
                                                                    potentialNode) > self.maxDistanceForNode:
                return prevNode if prev != None else nearestNode
            prevNode = point
        return potentialNode

    def getneighboursWithinRadius(self, currentNode):
        neighbours = []
        RADIUS = 10
        for node in self.visited.keys():
            distance = self.getEuclidianDistance(currentNode, node)
            if distance < RADIUS:
                neighbours.append(node)
        return neighbours

    def getNodeWithMinCost(self, currentNode, neighbours, start):

        minCost = float("inf")
        nodeWithMinCost = None
        for node in neighbours:
            potentialCost = node.costToCome + self.getEuclidianDistance(currentNode, node)
            if minCost > potentialCost:
                minCost = potentialCost
                nodeWithMinCost = node

        if nodeWithMinCost == None:
            print("didnt find node with minimum cost. Getting nearest as minimum node.")
            nodeWithMinCost = self.getNearestNeighbour(currentNode)
            currentNode.costToCome = (
                        self.getEuclidianDistance(currentNode, nodeWithMinCost) + nodeWithMinCost.costToCome)
        else:
            currentNode.costToCome = minCost

        # nodeWithMinCost.child = currentNode
        return nodeWithMinCost

    def getNearestNeighbour(self, currentNode):

        nearestNode = None
        minDistance = float("inf")
        for node in self.visited:
            currentDistance = self.getEuclidianDistance(currentNode, node)
            if minDistance > currentDistance:
                minDistance = currentDistance
                nearestNode = node
        return nearestNode if nearestNode != None else start

    def canFindPath(self, start, end):
        self.visited[start] = True
        for iterations in range(10000):
            currentNode = self.getSamplePoint()

            self.RGD(currentNode)

            if currentNode in self.visited:
                continue

            # If the sample point is not outside the areana or inside an obstacle
            if (not self.isInObstacle(currentNode.x, currentNode.y)) and (
            not self.isOutsideArena(currentNode.x, currentNode.y)):

                # Getting the neighbours
                neighbours = self.getneighboursWithinRadius(currentNode)
                neighbourWithMinCost = self.getNodeWithMinCost(currentNode, neighbours, start)
                nearestNode = neighbourWithMinCost

                # If the branch is inside an obstacle or distance betwen sample and neareset node is greater than robot's ability
                if self.isBranchInObstacle(nearestNode, currentNode) or self.getEuclidianDistance(nearestNode,
                                                                                                  currentNode) > self.maxDistanceForNode:
                    print("Searching for new point")
                    continue

                nearestNode.neighbour[currentNode] = self.getEuclidianDistance(nearestNode, currentNode)
                currentNode.costToCome = nearestNode.costToCome + self.getEuclidianDistance(nearestNode, currentNode)
                currentNode.cost = currentNode.costToCome + currentNode.costToGo
                currentNode.parent = nearestNode
                pygame.draw.line(gridDisplay, CYAN, [currentNode.x, HEIGHT - currentNode.y],
                                 [nearestNode.x, HEIGHT - nearestNode.y], 2)
                pygame.display.update()
                self.visited[currentNode] = True

                for i in range(len(neighbours)):
                    potentialChild = neighbours[i]
                    if (currentNode.costToCome + self.getEuclidianDistance(currentNode,
                                                                           potentialChild)) < potentialChild.costToCome and (
                    not self.isBranchInObstacle(currentNode, potentialChild)):
                        # print("Rewiring!")

                        pygame.draw.line(gridDisplay, WHITE, [potentialChild.x, HEIGHT - potentialChild.y],
                                         [potentialChild.parent.x, HEIGHT - potentialChild.parent.y], 2)
                        pygame.display.update()
                        # time.sleep(1)

                        potentialChild.parent = currentNode
                        potentialChild.costToCome = (
                                    currentNode.costToCome + self.getEuclidianDistance(currentNode, potentialChild))

                        pygame.draw.line(gridDisplay, CYAN, [currentNode.x, HEIGHT - currentNode.y],
                                         [potentialChild.x, HEIGHT - potentialChild.y], 2)
                        pygame.display.update()
                        # time.sleep(1)
                        self.generateObstacles(start, end)

        return True

    def backTrack(self, child):
        """
        Description: Backtracking from the finishing node to the start node.
        Input: Ending Node
        Output: A animation of the path generated.
        """
        while child != None:
            path.append((child.x, child.y))
            print(child.x, child.y, "Path")
            child = child.parent
        return True

    def getPath(self, start, end):

        priorityQueue = []
        visited_list = {}
        heapq.heappush(priorityQueue, (start.cost, start))
        while len(priorityQueue):
            currentNode = heapq.heappop(priorityQueue)
            currentNode = currentNode[1]
            if self.isInTargetArea(currentNode.x, currentNode.y):
                print("We are doneeeeeeeeeee")
                self.backTrack(currentNode)
                return True
            if tuple([currentNode.x, currentNode.y]) in visited_list:
                continue
            visited_list[tuple([currentNode.x, currentNode.y])] = True
            for neighbour, newDistance in currentNode.neighbour.items():
                heapq.heappush(priorityQueue, (neighbour.cost, neighbour))
        return False

    def generateObstacles(self, start, end):
        """
        Description: Checks if a point is in the Ellipse.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        # Circle
        pygame.draw.circle(gridDisplay, MAGENTA, [90, HEIGHT - 70], 35)

        # Ellipse
        pygame.draw.ellipse(gridDisplay, MAGENTA, [186, HEIGHT - 176, 120, 60], 0)

        # Roatated Rect
        pygame.draw.polygon(gridDisplay, MAGENTA,
                            [(36, HEIGHT - 124), (160, HEIGHT - 210), (170, HEIGHT - 194), (48, HEIGHT - 108)])

        # Broken Rect
        pygame.draw.polygon(gridDisplay, MAGENTA,
                            [(200, HEIGHT - 280), (230, HEIGHT - 280), (230, HEIGHT - 270), (200, HEIGHT - 270)])
        pygame.draw.polygon(gridDisplay, MAGENTA,
                            [(200, HEIGHT - 270), (210, HEIGHT - 270), (210, HEIGHT - 240), (200, HEIGHT - 240)])
        pygame.draw.polygon(gridDisplay, MAGENTA,
                            [(200, HEIGHT - 240), (230, HEIGHT - 240), (230, HEIGHT - 230), (200, HEIGHT - 230)])

        # Starting Circle
        pygame.draw.circle(gridDisplay, BLACK, [start.x, HEIGHT - start.y], 10)

        # Ending Circle
        pygame.draw.circle(gridDisplay, BLACK, [end.x, HEIGHT - end.y], 10)


# x1 = int(input("Enter the x coordiante of the starting point: "))
# y1 = int(input("Enter the y coordiante of the starting point: "))
# print("#############################################")

# x2 = int(input("Enter the x coordiante of the ending point: "))
# y2 = int(input("Enter the y coordiante of the ending point: "))
# print("#############################################")

# MAGNITUDE = int(input("Enter the step size of the robot:  "))
# RADIUS = int(input("Enter the radius of the robot:  "))
# CLEARANCE = int(input("Enter the clearance:  "))

#############################################
# Algorithm Driver
# end = Node(x2, y2, x2, y2)
# start = Node(x1, y1, x2, y2)
end = Node(385, 285, 385, 285)
start = Node(15, 15, 385, 285)
start.costToCome = 0
robot = Graph(start, end)  # Graph(start, end, MAGNITUDE, RADIUS, CLEARANCE)
path = []
pygame.init()  # Setup Pygame
gridDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
gridDisplay.fill(WHITE)

pygame.display.set_caption("PRRT* + A* Algorithm")
exiting = False
clock = pygame.time.Clock()
canvas = Graph(start, end)  # Create Canvas
canvas.generateObstacles(start, end)
if robot.canFindPath(start, end):
    if robot.getPath(start, end):
        print("Printed path")
    path.reverse()
exiting = False

#############################################
# Running the simulation in loop
while not exiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exiting = True

    # Visualizing the final path
    for index in range(len(path)):
        x, y = path[index]
        if index != 0:
            pygame.draw.line(gridDisplay, MAGENTA, [prevX, HEIGHT - prevY], [x, HEIGHT - y], 2)
            pygame.display.update()

        time.sleep(.5)
        prevX = x
        prevY = y

    clock.tick(2000)
    pygame.display.flip()
    exiting = True
# pygame.quit()
#############################################
