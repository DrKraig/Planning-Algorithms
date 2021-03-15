#https://github.com/SamPusegaonkar/ENPM661/tree/main/Project2
#Output Videos can be found in the 'Output Videos' folder.

import pygame
import math

#Defining Graph Constants
HEIGHT = 300
WIDTH = 400
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
MAGENTA = (255,0,255)

class Node:
    """
    Node class : This class is built to store the node information.
    A node is simply a location on a map. For each node, its neighbours, parents & distance to reach that node is stored.
    """
    def __init__(self, i ,j):
        """
        Description: Defining all properties for each node - Neighbours, Parents, Distance.
        """
        self.i = i
        self.j = j
        self.distanceToReach = float('inf')
        self.neighbours = {}
        self.parent = None

class Graph:
    """
    Graph class : This class defines all methods to generate a graph and perform Djikstra's Algorithm.
    """
    def __init__(self):
        self.visited = {}

    def getNeighbours(self, currentNode):
        """
        Description: Returns neighbours for the currentNode.
        """
        i, j = currentNode.i, currentNode.j
        neighbours ={}

        #Bottom Node
        if i > 0 and (not self.isAnObstacle(i-1, j)):
            newNode = Node(i-1,j)
            neighbours[newNode] = 1
        
        #Left Node
        if j > 0 and (not self.isAnObstacle(i, j-1)):
            newNode = Node(i,j-1)
            neighbours[newNode] = 1
        
        #Top Node
        if i < (HEIGHT -1) and (not self.isAnObstacle(i+1, j)):
            newNode = Node(i+1,j)
            neighbours[newNode] = 1
        
        #Right Node
        if j < (WIDTH -1) and (not self.isAnObstacle(i, j+1)):
            newNode = Node(i,j+1)
            neighbours[newNode] = 1
        
        #TopLeft Node
        if j > 0 and i < (HEIGHT-1) and (not self.isAnObstacle(i+1, j-1)):
            newNode = Node(i+1,j-1)
            neighbours[newNode] = 1.41
        
        #TopRight Node
        if j < (WIDTH-1) and i < (HEIGHT-1)and (not self.isAnObstacle(i+1, j+1)):
            newNode = Node(i+1,j+1)
            neighbours[newNode] = 1.41
        
        #BottomLeft Node
        if i > 0 and j > 0 and (not self.isAnObstacle(i-1, j-1)):
            newNode = Node(i-1,j-1)
            neighbours[newNode] = 1.41

        #BottomRight Node
        if i > 0 and j < (WIDTH -1) and (not self.isAnObstacle(i-1, j+1)):
            newNode = Node(i-1,j+1)
            neighbours[newNode] = 1.41
        
        return neighbours

    def generateGraph(self,):
        """
        Description: Checks if a point is in the Ellipse. 
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        #Make background White
        gridDisplay.fill(WHITE)

        #Circle
        pygame.draw.circle(gridDisplay, MAGENTA, [90,HEIGHT - 70], 35)
        
        #Ellipse
        pygame.draw.ellipse(gridDisplay, MAGENTA, [186, HEIGHT - 176, 120, 60], 0)

        #Polygon
        pygame.draw.polygon(gridDisplay, MAGENTA, [(285, HEIGHT - 105), (324, HEIGHT -144), (354, HEIGHT -138),(380,HEIGHT -171), (380,HEIGHT -116),(328,HEIGHT -63)])

        #Roatated Rect
        pygame.draw.polygon(gridDisplay, MAGENTA, [(36, HEIGHT - 124), (160, HEIGHT -210), (170, HEIGHT -194),(48,HEIGHT -108)])

        #Broken Rect
        pygame.draw.polygon(gridDisplay, MAGENTA, [(200, HEIGHT - 280), (230, HEIGHT -280), (230, HEIGHT -270),(200,HEIGHT -270)])
        pygame.draw.polygon(gridDisplay, MAGENTA, [(200, HEIGHT - 270), (210, HEIGHT -270), (210, HEIGHT -240),(200,HEIGHT -240)])
        pygame.draw.polygon(gridDisplay, MAGENTA, [(200, HEIGHT - 240), (230, HEIGHT -240), (230, HEIGHT -230),(200,HEIGHT -230)])

    def performDijkstra(self, start, end):
        """
        Description: Defining initial constants - Visited array, Rows, Cols, Target String.
        Input: Starting and ending node for the robot to browse.
        Output: Returns True or False to define if an optimal path can be found or not.
        """

        #Checking is start and end  are in obstancle.
        if self.isAnObstacle(start.i,start.j) and self.isAnObstacle(end.i, end.j):
            print("Starting and ending point are inside the obstacle!")
            return
        if self.isAnObstacle(start.i,start.j):
            print("Starting point is inside the obstacle!")
            return 
        if self.isAnObstacle(end.i, end.j):
            print("Ending point is inside the obstacle!")
            return 
        print("Finding path...")
        priorityQueue = [start]
        while len(priorityQueue):

            priorityQueue.sort(key = lambda x: x.distanceToReach)
            currentNode = priorityQueue.pop(0)

            if currentNode.i == end.i and currentNode.j == end.j:
                print("Found a path!")
                #self.backTrack(currentNode)
                #print("Distance Required to reach from start to end is:", currentNode.distanceToReach)
                return True
            
            if tuple([currentNode.i, currentNode.j]) in self.visited:
                continue
            self.visited[tuple([currentNode.i, currentNode.j])] = True

            currentDistance = currentNode.distanceToReach
            neighbours = self.getNeighbours(currentNode)
            currentNode.neighbours = neighbours
            for neighbourNode, newDistance in neighbours.items():

                neighbourNode.distanceToReach = currentDistance + newDistance
                neighbourNode.parent = currentNode
                priorityQueue.append(neighbourNode)

        print("Cannot find a path :(")
        return False

    def visualizeDijkstra(self, start, end):
        """
        Description: Visualization of the algorithm.
        Input: Starting and ending node for the robot to browse.
        Output: A animation of nodes which are browsed and the path generated.
        """

        self.visited = {}
        priorityQueue = [start]
        while len(priorityQueue):
            priorityQueue.sort(key = lambda x: x.distanceToReach)
            currentNode = priorityQueue.pop(0)

            if currentNode.i == end.i and currentNode.j == end.j:
                self.backTrack(currentNode)
                print("Distance Required to reach from start to end is:", currentNode.distanceToReach)
                return
            
            if tuple([currentNode.i, currentNode.j]) in self.visited:
                continue
            self.visited[tuple([currentNode.i, currentNode.j])] = True

            currentDistance = currentNode.distanceToReach
            for neighbourNode, newDistance in currentNode.neighbours.items():
                i = neighbourNode.i
                j = neighbourNode.j
                if (i-5 < start.i < i+5 and j-5 < start.j < j+5) or (i-5 < end.i < i+5 and j-5 < end.j < j+5):
                    pygame.draw.rect(gridDisplay, BLACK, [i, HEIGHT - j, 2,2])
                    pygame.display.update()         
                else:    
                    pygame.draw.rect(gridDisplay, CYAN, [i, HEIGHT - j, 2,2])
                    pygame.display.update()

                # neighbourNode.distanceToReach = currentDistance + newDistance
                # neighbourNode.parent = currentNode
                priorityQueue.append(neighbourNode)
        return 

    def backTrack(self, child):
        """
        Description: Backtracking from the finishing node to the start node.
        Input: Ending Node
        Output: A animation of the path generated.
        """

        while child != None:
            print(child.i, child.j, "Path")
            grid[child.i][child.j] = 1
            child = child.parent
        return True
    
    def isInCircle(self, x,y):
        """
        Description: Checks if a point is in the circle. 
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        if (x - 90) **2 + (y-70)**2 - 1225 > 0:
            return False
        else:
            return True

    def isInRectangle(self, x,y):
        """
        Description: Checks if a point is in the rotated rectangle. 
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        if (y + 1.42*x - 176.55) > 0  and (y - 0.7*x - 74.39) > 0 and (y - 0.7*x - 98.81) < 0 and (y + 1.42*x - 438.06) < 0:
            return True
        else:
            return False

    def isInBrokenRectangle(self, x,y):
        """
        Description: Checks if a point is in the top rectangle. 
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        if (x >= 200 and x <= 210 and y <= 280 and y >=230 ) or (x>= 210 and x <= 230 and y >=270 and y <= 280) or (y >= 230 and y <= 240 and x >= 210 and x <= 230):
            return True
        else:
            return False

    def isInEllipse(self, x,y):
        """
        Description: Checks if a point is in the Ellipse. 
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        a = 60
        b = 30
        h = 246
        k = 145
        if ((math.pow((x - h), 2) / math.pow(a, 2)) + (math.pow((y - k), 2) / math.pow(b, 2))) < 1:
            return True
        else:
            return False

    def isAnObstacle(self,x,y):
        """
        Description: Checks if the point (x,y) is inside an obstacle or not.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        return self.isInEllipse(x,y) or self.isInBrokenRectangle(x,y) or self.isInCircle(x,y) or self.isInRectangle(x,y)

x1 = int(input("Enter the x coordiante of the starting point: "))
y1 = int(input("Enter the y coordiante of the starting point: "))

x2 = int(input("Enter the x coordiante of the ending point: "))
y2 = int(input("Enter the y coordiante of the ending point: "))

#############################################           
#Algorithm Driver   
start = Node(x1,y1)
start.distanceToReach = 0
end = Node(x2,y2)
robot = Graph()

#Check if path can be found
if robot.performDijkstra(start, end):
    pass
    # pygame.init() #Setup Pygame
    # gridDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
    # pygame.display.set_caption("Dijkstra's Algorithm")
    # exiting = False
    # clock = pygame.time.Clock()
    # grid = [[0 for j in range(HEIGHT)] for i in range(WIDTH)]

    # canvas = Graph() #Create Canvas
    # canvas.generateGraph()
    # robot.visualizeDijkstra(start, end)
else:
    #No Path Found
    exiting = True

#############################################
#Running the simulation in loop

# while not exiting:
#     for event in pygame.event.get():  
#         if event.type == pygame.QUIT:
#             exiting = True  

#     for row in range(WIDTH):
#         for column in range(HEIGHT):
#             if grid[row][column] == 1:
#                 pygame.draw.rect(gridDisplay, BLACK,[row, HEIGHT - column, 2,2])
    
#     clock.tick(2000)
#     pygame.display.flip()
 
# pygame.quit()
#############################################
