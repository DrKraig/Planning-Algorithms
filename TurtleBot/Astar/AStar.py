# https://github.com/DrKraig/Planning-Algorithms
# Output Videos can be found in the 'Output' folder.

import pygame
import math
import heapq
import time
import functools

# Defining Graph Constants
HEIGHT = 300
WIDTH = 400
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
MAGENTA = (255, 0, 255)


class Node:
    """
    Node class : This class is built to store the node information.
    A node is simply a location on a map. For each node, its neighbours, parents & distance to reach that node is stored.
    """

    def __init__(self, i, j, endI, endJ, theta):
        """
        Description: Defining all properties for each node - Neighbours, Parents, Distance.
        """
        self.i = i
        self.j = j
        self.theta = theta
        self.costToCome = float('inf')
        self.costToGo = math.sqrt((i - endI) ** 2 + (j - endJ) ** 2)
        self.cost = None
        self.neighbours = {}
        self.parent = None

    def __lt__(self, other):
        return self.cost < other.cost


class Graph:
    """
    Graph class : This class defines all methods to generate a graph and perform AStar Algorithm.
    """

    def __init__(self, start, end, MAGNITUDE, RADIUS, CLEARANCE):
        self.visited = {}
        self.endI = end.i
        self.endJ = end.j
        self.MAGNITUDE = MAGNITUDE
        self.RADIUS = RADIUS
        self.CLEARANCE = CLEARANCE + self.RADIUS

    def getNeighbours(self, currentNode):
        """
        Description: Returns neighbours for the currentNode.
        """
        i, j, theta = currentNode.i, currentNode.j, currentNode.theta
        neighbours = {}
        

        for deltaTheta in range(-60, 60, 30):
            x, y, newTheta = self.getNewCoordiantes(i, j, theta, deltaTheta)
            if (not self.isOutsideArena(x, y)) and (not self.isAnObstacle(x, y)):
                newNode = Node(x, y, self.endI, self.endJ, newTheta)
                neighbours[newNode] = 1
        return neighbours

    def getNewCoordiantes(self, i, j, theta, deltaTheta):
        newTheta = theta + deltaTheta

        if newTheta > 0:
            newTheta = newTheta % 360
        elif newTheta < 0:
            newTheta = (newTheta + 360) % 360

        newI = i + self.MAGNITUDE * math.cos((math.pi / 180) * newTheta)
        newJ = j + self.MAGNITUDE * math.sin((math.pi / 180) * newTheta)

        newI = self.getRoundedNumber(newI)
        newJ = self.getRoundedNumber(newJ)

        return newI, newJ, newTheta

    def getRoundedNumber(self, i):

        decimal = i - int(i)
        if decimal > 0.5:
            if decimal >= 0.75:
                return math.ceil(i)
            else:
                return int(i) + .5
        elif decimal < 0.5:
            if decimal < 0.25:
                return math.floor(i)
            else:
                return int(i) + .5
        return i

    def generateGraph(self, ):
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

    def performAStar(self, start, end):
        """
        Description: Defining initial constants - Visited array, Rows, Cols, Target String.
        Input: Starting and ending node for the robot to browse.
        Output: Returns True or False to define if an optimal path can be found or not.
        """

        # Checking is start and end are in obstancle.
        if self.isAnObstacle(start.i, start.j) and self.isAnObstacle(end.i, end.j):
            print("Starting and ending point are inside the obstacle!")
            return

        if self.isAnObstacle(start.i, start.j):
            print("Starting point is inside the obstacle!")
            return
        if self.isAnObstacle(end.i, end.j):
            print("Ending point is inside the obstacle!")
            return

        if self.isOutsideArena(start.i, start.j):
            print("Starting point is outside the arena!")
            print("Starting point should be between (15,15) and (385,285)")
            return

        if self.isOutsideArena(end.i, end.j):
            print("Ending point is outside the arena!")
            print("Ending point should be between (15,15) and (385,285)")
            return

        print("Finding path...")
        priorityQueue = []
        heapq.heappush(priorityQueue, (start.cost, start))
        while len(priorityQueue):
            currentNode = heapq.heappop(priorityQueue)
            currentNode = currentNode[1]
            if self.isInTargetArea(currentNode.i, currentNode.j):
                print("Found a path!")
                return True

            currentDistance = currentNode.costToCome
            neighbours = self.getNeighbours(currentNode)
            currentNode.neighbours = neighbours
            for neighbourNode, newDistance in neighbours.items():
                neighbourNode.costToCome = currentDistance + newDistance
                neighbourNode.cost = neighbourNode.costToCome + neighbourNode.costToGo
                neighbourNode.parent = currentNode
                heapq.heappush(priorityQueue, (neighbourNode.cost, neighbourNode))
        print("Cannot find a path :(")
        return False

    def visualizeAStar(self, start, end):
        """
        Description: Visualization of the algorithm.
        Input: Starting and ending node for the robot to browse.
        Output: A animation of nodes which are browsed and the path generated.
        """

        self.visited = {}
        priorityQueue = []
        heapq.heappush(priorityQueue, (start.cost, start))
        pygame.draw.circle(gridDisplay, BLACK, [start.i, HEIGHT - start.j], 10)
        pygame.draw.circle(gridDisplay, BLACK, [end.i, HEIGHT - end.j], 10)
        pygame.display.update()
        while len(priorityQueue):

            currentNode = heapq.heappop(priorityQueue)
            currentNode = currentNode[1]

            if self.isInTargetArea(currentNode.i, currentNode.j):
                self.backTrack(currentNode)
                print("Distance Required to reach from start to end is:", currentNode.costToCome)
                return

            currentDistance = currentNode.costToCome
            for neighbourNode, newDistance in currentNode.neighbours.items():
                i = neighbourNode.i
                j = neighbourNode.j
                pygame.draw.line(gridDisplay, CYAN, [currentNode.i, HEIGHT - currentNode.j], [i, HEIGHT - j], 2)
                pygame.display.update()
                time.sleep(0.1)

                heapq.heappush(priorityQueue, (neighbourNode.cost, neighbourNode))

        return

    def isInTargetArea(self, i, j):
        """
        Description: Checks if the currentnode is in target area to terminal the program
        Input: Current Node co-ordinates
        Output: Boolean
        """
        if (i - self.endI) ** 2 + (j - self.endJ) ** 2 - 100 <= 0:
            return True
        else:
            return False

    def backTrack(self, child):
        """
        Description: Backtracking from the finishing node to the start node.
        Input: Ending Node
        Output: A animation of the path generated.
        """
        while child != None:
            path.append((child.i, child.j))
            print(child.i, child.j, "Path")
            child = child.parent
        return True

    def isinStartingCircle(self, start, i, j):
        """
        Description: Checks if a point is in the starting circle from where the robot will start,
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        if (i - start.i) ** 2 + (j - start.j) ** 2 - 100 <= 0:
            return True
        else:
            return False

    def isInStartingSquare(self, start, i, j):
        """
        Description: Checks if a point is in the starting square from where the robot will start.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        if (start.i - 10 <= i <= start.i + 10) and (start.j - 10 <= j <= start.j + 10):
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
        a = 60+self.CLEARANCE
        b = 30+self.CLEARANCE
        h = 246
        k = 145
        if ((math.pow((x - h), 2) / math.pow(a, 2)) + (math.pow((y - k), 2) / math.pow(b, 2))) <= 1:
            return True
        else:
            return False

    def isAnObstacle(self, x, y):
        """
        Description: Checks if the point (x,y) is inside an obstacle or not.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        return self.isInEllipse(x, y) or self.isInBrokenRectangle(x, y) or self.isInCircle(x, y) or self.isInRectangle(
            x, y)

    def isOutsideArena(self, x, y):
        """
        Description: Checks if the point (x,y) is outside the areana or not.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """
        

        return True if x < self.CLEARANCE or y < self.CLEARANCE or x > 400-self.CLEARANCE or y > 300-self.CLEARANCE else False


x1 = int(input("Enter the x coordiante of the starting point: "))
y1 = int(input("Enter the y coordiante of the starting point: "))
thetaStart = int(input("Enter the start theta: "))
print("#############################################")

x2 = int(input("Enter the x coordiante of the ending point: "))
y2 = int(input("Enter the y coordiante of the ending point: "))
print("#############################################")

MAGNITUDE = int(input("Enter the step size of the robot:  "))
RADIUS = int(input("Enter the radius of the robot:  "))
CLEARANCE = int(input("Enter the clearance:  "))

#############################################
# Algorithm Driver
end = Node(x2, y2, x2, y2, 0)
start = Node(x1, y1, x2, y2, thetaStart)
start.costToCome = 0
robot = Graph(start, end, MAGNITUDE, RADIUS, CLEARANCE)
path = []

# Check if path can be found
if robot.performAStar(start, end):
    pass
    pygame.init()  # Setup Pygame
    gridDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("A* Algorithm - Rigid Robot")
    exiting = False
    clock = pygame.time.Clock()
    grid = [[0 for j in range(HEIGHT)] for i in range(WIDTH)]
    canvas = Graph(start, end, MAGNITUDE, RADIUS, CLEARANCE)  # Create Canvas
    canvas.generateGraph()
    robot.visualizeAStar(start, end)
    path.reverse()
else:
    # No Path Found
    exiting = True

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
pygame.quit()
#############################################
