import pygame
import math
import heapq
import time
import functools
import random
import numpy as np


# Defining Graph Constants
HEIGHT = 500
WIDTH = 500
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
        self.costToGo = 2.5*math.sqrt((x - endX) ** 2 + (y - endY) ** 2)
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
        self.maxDistanceForNode = 8
        self.CLEARANCE = 0.2

    def getSamplePoint(self):
        x = np.random.uniform(0,10) * 1000 
        x = int(x)/1000
        y = np.random.uniform(0, 10) * 1000
        y = int(y) / 1000
        return Node(x, y, self.endX, self.endY)

    def isInTargetArea(self, i, j):
        """
        Description: Checks if the currentnode is in target area to terminal the program
        Input: Current Node co-ordinates
        Output: Boolean
        """
        if (i - self.endX) ** 2 + (j - self.endY) ** 2 - 0.01 <= 0:
            return True
        else:
            return False

    def isInCircle1(self, x, y):
        """
        Description: Checks if a point is in the circle.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """
        r = 1 + self.CLEARANCE
        if (x - 2) ** 2 + (y - 2) ** 2 - r ** 2 >= 0:
            return False
        else:
            return True

    def isInCircle2(self, x, y):
        """
        Description: Checks if a point is in the circle.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """
        r = 1 + self.CLEARANCE
        if (x - 2) ** 2 + (y - 8) ** 2 - r ** 2 >= 0:
            return False
        else:
            return True

    def isInRectangle1(self, x, y):
        """
        Description: Checks if a point is in the rotated rectangle.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """
        circ1 = (x - 0.25) ** 2 + (y - 5.75) ** 2 <= self.CLEARANCE ** 2
        circ2 = (x - 1.75) ** 2 + (y - 5.75) ** 2 <= self.CLEARANCE ** 2
        circ3 = (x - 0.25) ** 2 + (y - 4.25) ** 2 <= self.CLEARANCE ** 2
        circ4 = (x - 1.75) ** 2 + (y - 4.25) ** 2 <= self.CLEARANCE ** 2
        side1 = x <= 1.75
        eside1 = x <= 1.75 + self.CLEARANCE
        side2 = y <= 5.75
        eside2 = y <= 5.75 + self.CLEARANCE
        side3 = x >= 0.25
        eside3 = x >= 0.25 - self.CLEARANCE
        side4 = y >= 4.25
        eside4 = y >= 4.25 - self.CLEARANCE
        rect1 = eside1 and side2 and eside3 and side4
        rect2 = side1 and eside2 and side3 and eside4

        if rect1 or rect2 or circ1 or circ2 or circ3 or circ4:
            return True
        else:
            return False

    def isInRectangle2(self, x, y):
        """
        Description: Checks if a point is in the rotated rectangle.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """
        circ1 = (x - 3.75) ** 2 + (y - 5.75) ** 2 <= self.CLEARANCE ** 2
        circ2 = (x - 6.25) ** 2 + (y - 5.75) ** 2 <= self.CLEARANCE ** 2
        circ3 = (x - 3.75) ** 2 + (y - 4.25) ** 2 <= self.CLEARANCE ** 2
        circ4 = (x - 6.25) ** 2 + (y - 4.25) ** 2 <= self.CLEARANCE ** 2
        side1 = x <= 6.25
        eside1 = x <= 6.25 + self.CLEARANCE
        side2 = y <= 5.75
        eside2 = y <= 5.75 + self.CLEARANCE
        side3 = x >= 3.75
        eside3 = x >= 3.75 - self.CLEARANCE
        side4 = y >= 4.25
        eside4 = y >= 4.25 - self.CLEARANCE
        rect1 = eside1 and side2 and eside3 and side4
        rect2 = side1 and eside2 and side3 and eside4

        if rect1 or rect2 or circ1 or circ2 or circ3 or circ4:
            return True
        else:
            return False

    def isInRectangle3(self, x, y):
        """
        Description: Checks if a point is in the rotated rectangle.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """
        circ1 = (x - 7.25) ** 2 + (y - 4) ** 2 <= self.CLEARANCE ** 2
        circ2 = (x - 8.75) ** 2 + (y - 4) ** 2 <= self.CLEARANCE ** 2
        circ3 = (x - 8.75) ** 2 + (y - 2) ** 2 <= self.CLEARANCE ** 2
        circ4 = (x - 7.25) ** 2 + (y - 2) ** 2 <= self.CLEARANCE ** 2
        side1 = x <= 8.75
        eside1 = x <= 8.75 + self.CLEARANCE
        side2 = y <= 4
        eside2 = y <= 4 + self.CLEARANCE
        side3 = x >= 7.25
        eside3 = x >= 7.25 - self.CLEARANCE
        side4 = y >= 2
        eside4 = y >= 2 - self.CLEARANCE
        rect1 = eside1 and side2 and eside3 and side4
        rect2 = side1 and eside2 and side3 and eside4

        if rect1 or rect2 or circ1 or circ2 or circ3 or circ4:
            return True
        else:
            return False

    def isInObstacle(self, x, y):
        """
        Description: Checks if the point (x,y) is inside an obstacle or not.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        return self.isInCircle1(x, y) or self.isInCircle2(x, y) or self.isInRectangle1(x, y) or self.isInRectangle2(x, y) or self.isInRectangle3(x, y)

    def isOutsideArena(self, x, y):
        """
        Description: Checks if the point (x,y) is outside the areana or not.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        return True if x < self.CLEARANCE or y < self.CLEARANCE or x > 10 - self.CLEARANCE or y > 10 - self.CLEARANCE else False


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

    def getPoints(self, nearestNode, currentNode):
        points = []
        x1 = nearestNode.x
        y1 = nearestNode.y

        x2 = currentNode.x
        y2 = currentNode.y
        dist = self.getEuclidianDistance(nearestNode,currentNode)

        v1 = (x2-x1)/dist
        v2 = (y2-y1)/dist
        for mag in np.arange(0, dist, 0.01):
            x = x1 + mag*v1
            y = y1 + mag*v2
            points.append([x, y])
        return points

    def getRectifiedPoint(self, points, nearestNode, currentNode):
        prev = None
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
        RADIUS = 5
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
        CLEARANCE = self.CLEARANCE
        #Circle 1
        r = 1 + self.CLEARANCE
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
        for x in np.arange(0.25, 1.75, 0.1):
            points.append([x,5.75 + CLEARANCE]) 
        for x in np.arange(0.25 , 1.75 , 0.1):
            points.append([x,4.25 - CLEARANCE])
        for y in np.arange(4.25 , 5.75 , 0.1):
            points.append([0.25 - CLEARANCE,y])
        for y in np.arange(4.25, 5.75 , 0.1):
            points.append([1.75 + CLEARANCE,y])

        
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
        for x in np.arange(3.75, 6.25, 0.1):
            points.append([x,5.75 + CLEARANCE])
        for x in np.arange(3.75, 6.25, 0.1):
            points.append([x,3.75 - CLEARANCE])
        for y in np.arange(4.25, 5.75, 0.1):
            points.append([3.75 - CLEARANCE,y])
        for y in np.arange(4.25, 5.75, 0.1):
            points.append([6.25 + CLEARANCE,y])

        
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
        for x in np.arange(7.25, 8.75 , 0.1):
            points.append([x,2 - CLEARANCE])
        for x in np.arange(7.25 , 8.75 , 0.1):
            points.append([x,4 + CLEARANCE])
        for y in np.arange(2 , 4, 0.1):
            points.append([8.75 + CLEARANCE,y])
        for y in np.arange(2, 4, 0.1):
            points.append([7.25 - CLEARANCE, y])

        return points

    def APG(self, currentNode):
        F = np.array([-2*(currentNode.x - self.endX), -2*(currentNode.y - self.endY)])
        F = F/np.linalg.norm(F)
        return F

    def RGD(self,currentNode, end):
        k = 10
        lam = 0.1
        ds_obs = 0.001
        for n in range(k):
            F = self.APG(currentNode)
            
            d_min = self.getNearestObstacle(currentNode) ## this lines needs to be changed
            if d_min <= ds_obs:
                currentNode.costToGo = 2.5*(math.sqrt((currentNode.x - end.x) ** 2 + (currentNode.y - end.y) ** 2))
                return currentNode
            else:
                Fx = F[0] * 1000
                Fx = int(Fx)/ 1000
                Fy = F[1] * 1000
                Fy = int(Fy)/ 1000
                currentNode.x = currentNode.x + lam*Fx
                currentNode.y = currentNode.y + lam*Fy

        currentNode.costToGo = 2.5*(math.sqrt((currentNode.x - end.x) ** 2 + (currentNode.y - end.y) ** 2))
        return currentNode


    def canFindPath(self, start, end):
        self.visited[start] = True
        for iterations in range(100):
            currentNode = self.getSamplePoint()
            prevCurrentNode = currentNode
            #pygame.draw.circle(gridDisplay, MAGENTA, [50 * currentNode.x, HEIGHT - 50 * currentNode.y], 5)
            #pygame.display.update()
            #time.sleep(0.50)
            #print(currentNode.x, currentNode.y)
            currentNode = self.RGD(currentNode, end)
            #pygame.draw.circle(gridDisplay, BLACK, [50 * currentNode.x, HEIGHT - 50 * currentNode.y], 5)
            #pygame.display.update()
            #time.sleep(1)
            
            #pygame.draw.line(gridDisplay, BLACK, [50*currentNode.x, HEIGHT - 50*currentNode.y],[50*prevCurrentNode.x, HEIGHT - 50*prevCurrentNode.y], 2)
            #pygame.display.update()

            print(currentNode.x, currentNode.y)
            print("######################")
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
                pygame.draw.line(gridDisplay, CYAN, [50*currentNode.x, HEIGHT - 50*currentNode.y],
                                 [50*nearestNode.x, HEIGHT - 50*nearestNode.y], 2)
                pygame.display.update()
                self.visited[currentNode] = True

                for i in range(len(neighbours)):
                    potentialChild = neighbours[i]
                    if (currentNode.costToCome + self.getEuclidianDistance(currentNode,
                                                                           potentialChild)) < potentialChild.costToCome and (
                    not self.isBranchInObstacle(currentNode, potentialChild)):
                        # print("Rewiring!")

                        pygame.draw.line(gridDisplay, WHITE, [50*potentialChild.x, HEIGHT - 50*potentialChild.y],
                                         [50*potentialChild.parent.x, HEIGHT - 50*potentialChild.parent.y], 2)
                        pygame.display.update()
                        # time.sleep(1)

                        potentialChild.parent = currentNode
                        potentialChild.costToCome = (
                                    currentNode.costToCome + self.getEuclidianDistance(currentNode, potentialChild))

                        pygame.draw.line(gridDisplay, CYAN, [50*currentNode.x, HEIGHT - 50*currentNode.y],
                                         [50*potentialChild.x, HEIGHT - 50*potentialChild.y], 2)
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

        #gridDisplay.fill(WHITE)

        # Circles
        pygame.draw.circle(gridDisplay, MAGENTA, [100, HEIGHT - 100], 50)
        pygame.draw.circle(gridDisplay, MAGENTA, [100, HEIGHT - 400], 50)

        # Rectangles
        pygame.draw.polygon(gridDisplay, MAGENTA, [(50 * 0.25, HEIGHT - 50 * 5.75), (50 * 1.75, HEIGHT - 50 * 5.75),
                                                   (50 * 1.75, HEIGHT - 50 * 4.25), (50 * 0.25, HEIGHT - 50 * 4.25)])
        pygame.draw.polygon(gridDisplay, MAGENTA, [(50 * 3.75, HEIGHT - 50 * 5.75), (50 * 6.25, HEIGHT - 50 * 5.75),
                                                   (50 * 6.25, HEIGHT - 50 * 4.25), (50 * 3.75, HEIGHT - 50 * 4.25)])
        pygame.draw.polygon(gridDisplay, MAGENTA,
                            [(50 * 7.25, HEIGHT - 50 * 4), (50 * 8.75, HEIGHT - 50 * 4), (50 * 8.75, HEIGHT - 50 * 2),
                             (50 * 7.25, HEIGHT - 50 * 2)])

        # Starting Circle
        pygame.draw.circle(gridDisplay, BLACK, [50*start.x, HEIGHT - 50*start.y], 10)

        # Ending Circle
        pygame.draw.circle(gridDisplay, BLACK, [50*end.x, HEIGHT - 50*end.y], 10)


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
end = Node(9, 9, 9, 9)
start = Node(0.3, 0.3, 9, 9)
start.costToCome = 0
robot = Graph(start, end)  # Graph(start, end, MAGNITUDE, RADIUS, CLEARANCE)
path = []
pygame.init()  # Setup Pygame
gridDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
gridDisplay.fill(WHITE)

pygame.display.set_caption("PRRT* + A* Algorithm ")
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
            pygame.draw.line(gridDisplay, MAGENTA, [50*prevX, HEIGHT - 50*prevY], [50*x, HEIGHT - 50*y], 2)
            pygame.display.update()

        time.sleep(.5)
        prevX = x
        prevY = y

    clock.tick(2000)
    pygame.display.flip()
    exiting = True
# pygame.quit()
#############################################
