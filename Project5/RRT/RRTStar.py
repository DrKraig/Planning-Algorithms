import pygame
import math
import heapq
import time
import functools
import random

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
        self.costToCome = None
        self.costToGo = math.sqrt((x - endX) ** 2 + (y - endY) ** 2)
        self.cost = None
        self.neighbour = {}
        self.parent = None
        self.child = None

    def __lt__(self, other):
        return self.cost < other.cost

class Graph:

    def __init__(self, start, end):
        self.visited = {}
        self.endX = end.x
        self.endY = end.y
        self.maxDistanceForNode = 200
        self.CLEARANCE = 15

    def getSamplePoint(self):
        x = random.randint(0, 400)
        y = random.randint(0, 300)
        return Node(x,y, self.endX, self.endY)

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
        if (x - 90) ** 2 + (y - 70) ** 2 - r**2 >= 0:
            return False
        else:
            return True

    def isInRectangle(self, x, y):
        """
        Description: Checks if a point is in the rotated rectangle.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """
        circ1 = (x-48)**2 + (y-108)**2 <= self.CLEARANCE**2
        circ2 = (x-170.876)**2 + (y-194.044)**2 <= self.CLEARANCE**2
        circ3 = (x-159.4)**2 + (y-210.432)**2 <= self.CLEARANCE**2
        circ4 = (x-36.524)**2 + (y-124.387)**2 <= self.CLEARANCE**2
        side1 = 0.7*x - y + 74.39 <= 0
        eside1 = 0.7*x - y + 74.39 - 1.22*self.CLEARANCE <= 0
        side2 = -1.43*x - y + 176.55 <= 0
        eside2 = -1.43*x - y + 176.55 - 1.74*self.CLEARANCE <= 0
        side3 = 0.7*x - y + 98.81 >= 0
        eside3 = 0.7*x - y + 98.81 + 1.22*self.CLEARANCE >= 0
        side4 = -1.43*x - y + 438.06 >= 0
        eside4 = -1.43*x - y + 438.06 + 1.74*self.CLEARANCE >= 0
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
        return self.isInEllipse(x, y) or self.isInBrokenRectangle(x, y) or self.isInCircle(x, y) or self.isInRectangle(x, y)

    def isOutsideArena(self, x, y):
        """
        Description: Checks if the point (x,y) is outside the areana or not.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """
    
        return True if x < self.CLEARANCE or y < self.CLEARANCE or x > 400-self.CLEARANCE or y > 300-self.CLEARANCE else False

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

    def isBranchInObstacle(self,nearestNode, currentNode):
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
        if x1 == x2:
            if y1 > y2:
                for y in range(y1,y2, -1):
                    points.append([x1, y])
            elif y1 < y2:
                for y in range(y1, y2):
                    points.append([x1, y])        
        elif y1 == y2:

            if x1 > x2:
                for x in range(x1,x2,-1):
                    points.append([x, y1])
            elif x1 < x2:
                for x in range(x1, x2):
                    points.append([x, y1])
        else:
            for x in range(min(x1,x2), max(x1,x2)+1):
                for y in range(min(y1,y2), max(y1,y2)+1):
                    if y == int(((x - x1) * (y1 - y2))/(x1-x2) + y1):
                        points.append([x, y])
        return points

    def getRectifiedPoint(self, points, nearestNode, currentNode):
        prev = None
        for point in points:
            x = point[0]
            y = point[1]
            potentialNode = Node(x,y, self.endX, self.endY)
            if self.isInObstacle(x, y) or self.getEuclidianDistance(nearestNode, potentialNode) > self.maxDistanceForNode:
                return prevNode if prev != None else nearestNode
            prevNode = point
        return potentialNode

    def getneighboursWithinRadius(self, currentNode):
        neighbours = []
        RADIUS = 400
        for node in self.visited:
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
                print("inside")
                minCost = potentialCost
                nodeWithMinCost = node
        
        if nodeWithMinCost == None:
            nodeWithMinCost = start

        nodeWithMinCost.child = currentNode
        currentNode.parent = nodeWithMinCost
        currentNode.costToCome = minCost
        return nodeWithMinCost
        
    def canFindPath(self, start, end):
        graphGenerated = False
        self.visited[start] = True
        for _ in range(100000):
            currentNode = self.getSamplePoint()

            #Discard point if visited already
            if currentNode in self.visited:
                continue
            
            #If the sample point is not outside the areana or inside an obstacle
            if not self.isInObstacle(currentNode.x, currentNode.y) and not self.isOutsideArena(currentNode.x, currentNode.y):
                
                #Getting the neighbours
                neighbours = self.getneighboursWithinRadius(currentNode)

                #Get the nearest node with minimum cost
                neighbourWithMinCost = self.getNodeWithMinCost(currentNode, neighbours, start)
                nearestNode = neighbourWithMinCost 

                #Rewiring

                for i in range(len(neighbours)):
                    for j in range(len(neighbours)):
                        if i != j:

                            child = neighbours[i]
                            parent = neighbours[j]

                            if parent.child != child:
                                if parent.costToCome + self.getEuclidianDistance(child, parent) < child.costToCome:
                                    child.parent = parent
                                    parent.child = child
                                    child.costToCome = parent.costToCome + self.getEuclidianDistance(child, parent)
                                    pygame.draw.line(gridDisplay, CYAN, [child.x, HEIGHT - child.y], [parent.x, HEIGHT - parent.y], 2)
                                    pygame.display.update()
                                    pygame.draw.line(gridDisplay, WHITE, [child.x, HEIGHT - child.y], [child.parent.x, HEIGHT - child.parent.y], 2)
                                    pygame.display.update()

                print(nearestNode.x, nearestNode.y, "Nearest Node")

                #If the branch is inside an obstacle or distance betwen sample and neareset node is greater than robot's ability
                if self.isBranchInObstacle(nearestNode, currentNode) or self.getEuclidianDistance(nearestNode, currentNode) > self.maxDistanceForNode:
                    print("Searching for new point")
                    points = self.getPoints(nearestNode, currentNode)
                    currentNode = self.getRectifiedPoint(points, nearestNode, currentNode)

                    #If it is visited
                    if currentNode in self.visited:
                        continue
                
                #If reached the goal
                if self.isInTargetArea(currentNode.x, currentNode.y):
                    pygame.draw.line(gridDisplay, CYAN, [currentNode.x, HEIGHT - currentNode.y], [nearestNode.x, HEIGHT - nearestNode.y], 2)
                    pygame.display.update()
                    nearestNode.neighbour[currentNode] = self.getEuclidianDistance(nearestNode, currentNode)
                    currentNode.costToCome = nearestNode.costToCome + self.getEuclidianDistance(nearestNode, currentNode)
                    currentNode.cost = currentNode.costToCome + currentNode.costToGo
                    currentNode.parent = nearestNode
                    graphGenerated = True
                    print("Generated a graph!")
                    return True
                
                self.visited[currentNode] = True
               
                nearestNode.neighbour[currentNode] = self.getEuclidianDistance(nearestNode, currentNode)
                currentNode.costToCome = nearestNode.costToCome + self.getEuclidianDistance(nearestNode, currentNode)
                currentNode.cost = currentNode.costToCome + currentNode.costToGo
                currentNode.parent = nearestNode
                print(currentNode.x, currentNode.y, "Sample")
                print(self.getEuclidianDistance(nearestNode, currentNode), "Cost to Come")
                print(currentNode.costToGo, "Cost to Go")
                pygame.draw.line(gridDisplay, CYAN, [currentNode.x, HEIGHT - currentNode.y], [nearestNode.x, HEIGHT - nearestNode.y], 2)
                pygame.display.update()
            else:
                print("Bad random sample generated - either inside the obs or greater than self.maxDistance")

            if graphGenerated:
                return True
            print("#########################")

    def backTrack(self, child):
        """
        Description: Backtracking from the finishing node to the start node.
        Input: Ending Node
        Output: A animation of the path generated.
        """
        print(child, "This is the child")
        while child != None:
            path.append((child.x, child.y))
            print(child.x, child.y, "Path")
            child = child.parent
        return True

    def getPath(self, start, end):  

        priorityQueue = []
        heapq.heappush(priorityQueue, (start.cost, start))
        while len(priorityQueue):
            currentNode = heapq.heappop(priorityQueue)
            currentNode = currentNode[1]
            print(currentNode, self.isInTargetArea(currentNode.x, currentNode.y))
            if self.isInTargetArea(currentNode.x, currentNode.y):
                print("We are doneeeeeeeeeee")  
                self.backTrack(currentNode)              
                return True
            for neighbour, newDistance in currentNode.neighbour.items():
                # pygame.draw.line(gridDisplay, MAGENTA, [currentNode.x, HEIGHT - currentNode.y], [neighbour.x, HEIGHT - neighbour.y], 2)
                # pygame.display.update()
                # time.sleep(0.01)
                heapq.heappush(priorityQueue, (neighbour.cost, neighbour))
        return False

    def generateObstacles(self, start, end):
        """
        Description: Checks if a point is in the Ellipse.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        # Make background White
        gridDisplay.fill(WHITE)

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

        #Starting Circle
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
robot = Graph(start, end)#Graph(start, end, MAGNITUDE, RADIUS, CLEARANCE)
path = []
pygame.init()  # Setup Pygame
gridDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RRT + A* Algorithm - Rigid Robot")
exiting = False
clock = pygame.time.Clock()
canvas = Graph(start, end)  # Create Canvas
canvas.generateObstacles(start, end)
if robot.canFindPath(start, end):
    robot.getPath(start, end)
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

        time.sleep(.1)
        prevX = x
        prevY = y

    clock.tick(2000)
    pygame.display.flip()
    exiting = True
#pygame.quit()
#############################################
