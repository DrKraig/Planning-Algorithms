import pygame
import sys

class Node:

    def __init__(self, i ,j):
        self.i = i
        self.j = j
        self.distanceToReach = float('inf')
        self.neighbours = {}
        self.parent = None

class Graph:
    def __init__(self):
        self.height= 100
        self.width = 100

        self.CELL_MARGIN = .5
        self.CELL_WIDTH = 2
        self.CELL_HEIGHT = 2

    # def generateGraph(self):
    #     for i in range(self.height):
    #         for j in range(self.width):
    #             currentNode = Node(i,j)
    #             #pygame.draw.rect(gridDisplay,(255,255,255),[(self.CELL_MARGIN + self.CELL_WIDTH) * j + self.CELL_MARGIN,(self.CELL_MARGIN + self.CELL_HEIGHT) * i + self.CELL_MARGIN,self.CELL_WIDTH, self.CELL_HEIGHT])
    #             #pygame.display.update()
    #             neighbours = self.getNeighbours(currentNode)
    #             currentNode.neighbours = neighbours
    #             print("Stored the neighbours", currentNode.neighbours, "for the node", currentNode.i, currentNode.j)

    def getNeighbours(self, currentNode):
        print("-----------------------------------------------------")
        i, j = currentNode.i, currentNode.j
        neighbours ={}

        #Top
        if i > 0 and (not self.isAnObstacle(i-1, j)):
            #print("No Obstacle found at ", i-1, j)
            neighbours[tuple([i-1,j])] = 1
        
        #Left
        if j > 0 and (not self.isAnObstacle(i, j-1)):
            #print("No Obstacle found at ", i, j-1)
            neighbours[tuple([i,j-1])] = 1
        
        #Bottom
        if i < (self.height -1) and (not self.isAnObstacle(i+1, j)):
            #print("No Obstacle found at ", i+1, j)
            neighbours[tuple([i+1,j])] = 1
        
        #Right
        if j < (self.width -1) and (not self.isAnObstacle(i, j+1)):
            #print("No Obstacle found at ", i, j+1)
            neighbours[tuple([i,j+1])] = 1
        
        #BottomLeft 
        if j > 0 and i < (self.height-1) and (not self.isAnObstacle(i+1, j-1)):
            #print("No Obstacle found at ", i+1, j-1)
            neighbours[tuple([i+1, j-1])] = 1.41
        
        #BottomRight 
        if j < (self.width-1) and i < (self.height-1)and (not self.isAnObstacle(i+1, j+1)):
            #print("No Obstacle found at ", i+1, j+1)
            neighbours[tuple([i+1, j+1])] = 1.41
        
        #TopLeft 
        if i > 0 and j > 0 and (not self.isAnObstacle(i-1, j-1)):
            #print("No Obstacle found at ", i-1, j-1)
            neighbours[tuple([i-1, j-1])] = 1.41

        #TopRight 
        if i > 0 and j < (self.width -1) and (not self.isAnObstacle(i-1, j+1)):
            #print("No Obstacle found at ", i-1, j+1)
            neighbours[tuple([i-1, j+1])] = 1.41
        
        print(neighbours, "are the neighbours of",i,j)
        return neighbours

    def performDijkstra(self, start, end):
        priorityQueue = [start]
        while len(priorityQueue):
            priorityQueue.sort(key = lambda x: x.distanceToReach)
            currentNode = priorityQueue.pop(0)
            if currentNode.i == end.i and currentNode.j == end.j:
                print("Found it!")
                self.backTrack(currentNode)
                print("Distance Required to reach from start to end is:", currentNode.distanceToReach)
                return
                 
            currentDistance = currentNode.distanceToReach
            neighbours = self.getNeighbours(currentNode)
            for neighbour, newDistance in neighbours.items():
                neighbourNode = Node(neighbour[0], neighbour[1])
                neighbourNode.distanceToReach = currentDistance + newDistance
                neighbourNode.parent = currentNode
                priorityQueue.append(neighbourNode)

        print("Cannot find a path :(")

    def backTrack(self, child):
        while child != None:
            print(child.i, child.j)
            child = child.parent
        return True
    
    def isInCircle(self, x,y):
        if (x - 90) **2 + (y-70)**2 - 1225 > 0:
            return False
        else:
            return True

    def isInRectangle(self, x,y):
        if (y + 1.42*x - 176.55) > 0  and (y - 0.7*x - 74.39) > 0 and (y - 0.7*x - 98.81) < 0 and (y + 1.42*x - 438.06) < 0:
            return True
        else:
            return False

    def isInBrokenRectangle(self, x,y):
        if (x >= 200 and x <= 210 and y <= 280 and y >=230 ) or (x>= 210 and x <= 230 and y >=270 and y <= 280) or (y >= 230 and y <= 240 and x >= 210 and x <= 230):
            return True
        else:
            return False

    def isInEllipse(self, x,y):
        horizontalRadius = 60
        verticalRadius = 30
        centerX = 246
        centerY = 145
        if  ((x- centerX)**2)/horizontalRadius**2 + ((y- centerY)**2)/verticalRadius**2 - 1< 0:
            return True
        else:
            return False

    def isInPolygon(self, x,y):
        if (y + .99*x - 389.3) > 0  and (y - x + 181.6) < 0 and (y - 1.13*x - 260.75) < 0 and (y + 0.29*x - 240.6022) < 0 and (y + 250*x -95054) < 0 and (y - x + 266) > 0:
            return True
        else:
            return False

    # def isInTestCircle(self, x,y):
    #     if (x - 2) **2 + (y-2)**2 - 1 < 0:
    #         return True
    #     else:
    #         return False

    # def isInTestCircleTwo(self, x,y):
    #     if (x - 4) **2 + (y-1)**2 - 1 < 0:
    #         return True
    #     else:
    #         return False

    def isAnObstacle(self,x,y):
        # return self.isInTestCircle(x,y) or self.isInTestCircleTwo(x,y)
        return self.isInEllipse(x,y) or self.isInBrokenRectangle(x,y) or self.isInCircle(x,y) or self.isInRectangle(x,y) or self.isInPolygon(x,y)
        
start = Node(1,1)
start.distanceToReach = 0
end = Node(5,0)
robot = Graph()
robot.performDijkstra(start, end)

#PyGame Code
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# GREEN = (0, 255, 0)
# RED = (255, 0, 0)

# grid = []
# for row in range(300):
#     grid.append([])
#     for column in range(5):
#         grid[row].append(0)

# pygame.init()
# gridDisplay = pygame.display.set_mode((100, 100))
# pygame.display.set_caption("First Game")

# done = False
# clock = pygame.time.Clock()

# while not done:
#     for event in pygame.event.get():  # User did something
#         if event.type == pygame.QUIT:  # If user clicked close
#             done = True  # Flag that we are done so we exit this loop
#         # elif event.type == pygame.MOUSEBUTTONDOWN:
#         #     # User clicks the mouse. Get the position
#         #     pos = pygame.mouse.get_pos()
#         #     # Change the x/y screen coordinates to grid coordinates
#         #     column = pos[0] // (WIDTH + MARGIN)
#         #     row = pos[1] // (HEIGHT + MARGIN)
#         #     # Set that location to one
#         #     grid[row][column] = 1
#         #     print("Click ", pos, "Grid coordinates: ", row, column)
 
#     # Set the screen background 
#     # Draw the grid
#     # for row in range(10):
#     #     for column in range(10):
#     #         color = WHITE
#     #         if grid[row][column] == 1:
#     #             color = GREEN
#     clock.tick(144)
 
#     pygame.display.flip()
 
# pygame.quit()

