import pygame
import math

HEIGHT = 300
WIDTH = 400
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
MAGENTA = (255,0,255)

class Node:

    def __init__(self, i ,j):
        self.i = i
        self.j = j
        self.distanceToReach = float('inf')
        self.neighbours = {}
        self.parent = None

class Graph:
    def __init__(self):
        self.visited = {}

    def getNeighbours(self, currentNode):
        i, j = currentNode.i, currentNode.j
        neighbours ={}

        #Bottom
        if i > 0 and (not self.isAnObstacle(i-1, j)):
            neighbours[tuple([i-1,j])] = 1
        
        #Left
        if j > 0 and (not self.isAnObstacle(i, j-1)):
            neighbours[tuple([i,j-1])] = 1
        
        #Top
        if i < (HEIGHT -1) and (not self.isAnObstacle(i+1, j)):
            neighbours[tuple([i+1,j])] = 1
        
        #Right
        if j < (WIDTH -1) and (not self.isAnObstacle(i, j+1)):
            neighbours[tuple([i,j+1])] = 1
        
        #TopLeft 
        if j > 0 and i < (HEIGHT-1) and (not self.isAnObstacle(i+1, j-1)):
            neighbours[tuple([i+1, j-1])] = 1.41
        
        #TopRight 
        if j < (WIDTH-1) and i < (HEIGHT-1)and (not self.isAnObstacle(i+1, j+1)):
            neighbours[tuple([i+1, j+1])] = 1.41
        
        #BottomLeft
        if i > 0 and j > 0 and (not self.isAnObstacle(i-1, j-1)):
            neighbours[tuple([i-1, j-1])] = 1.41

        #BottomRight 
        if i > 0 and j < (WIDTH -1) and (not self.isAnObstacle(i-1, j+1)):
            neighbours[tuple([i-1, j+1])] = 1.41
        
        return neighbours

    def performDijkstra(self, start, end):

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

        priorityQueue = [start]
        while len(priorityQueue):

            priorityQueue.sort(key = lambda x: x.distanceToReach)
            currentNode = priorityQueue.pop(0)

            if currentNode.i == end.i and currentNode.j == end.j:
                print("Found a path!")
                self.backTrack(currentNode)
                print("Distance Required to reach from start to end is:", currentNode.distanceToReach)
                return
            
            if tuple([currentNode.i, currentNode.j]) in self.visited:
                continue
            self.visited[tuple([currentNode.i, currentNode.j])] = True

            currentDistance = currentNode.distanceToReach
            neighbours = self.getNeighbours(currentNode)

            for neighbour, newDistance in neighbours.items():
                i = neighbour[0]
                j = neighbour[1]
                neighbourNode = Node(i,j)
                if (i == start.i and j == start.j) or (i == end.i and j == end.j):
                    pygame.draw.rect(gridDisplay, BLACK, [i, HEIGHT - j, 2,2])
                    pygame.display.update()
                else:    
                    pygame.draw.rect(gridDisplay, CYAN, [i, HEIGHT - j, 2,2])
                    pygame.display.update()

                neighbourNode.distanceToReach = currentDistance + newDistance
                neighbourNode.parent = currentNode
                priorityQueue.append(neighbourNode)

        print("Cannot find a path :(")

    def backTrack(self, child):
        while child != None:
            print(child.i, child.j, "GRID")
            grid[child.i][child.j] = 1
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
        horizontalRadius = a = 60
        verticalRadius = b = 30
        centerX = h = 246
        centerY = k = 145
        if ((math.pow((x - h), 2) / math.pow(a, 2)) + (math.pow((y - k), 2) / math.pow(b, 2))) < 1:
            return True
        else:
            return False

    def isInPolygon(self, x,y):
        if ((y - 1.01*x + 181.62) < 0 and (y + 0.29*x - 239.89) < 0 and (y + 249.20*x -95054.25) < 0 and (y - x + 266) > 0 and (y + 0.99*x - 389.3) > 0 ) or ( (y - 1.13*x + 260.75) < 0  and (y + 249.20*x - 95054.25) < 0 and (y + .29*x - 240.60) > 0):
            return True
        else:
            return False

    def isAnObstacle(self,x,y):
        return self.isInEllipse(x,y) or self.isInBrokenRectangle(x,y) or self.isInCircle(x,y) or self.isInRectangle(x,y) or self.isInPolygon(x,y)

# i1 = int(input("Enter the ith coordiante of the starting point: "))
# j1 = int(input("Enter the jth coordiante of the starting point: "))

# i2 = int(input("Enter the ith coordiante of the ending point: "))
# j2 = int(input("Enter the jth coordiante of the ending point: "))

x1 = 420
y1 = 120

x2 = 400
y2 = 0

pygame.init()
gridDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dijkstra's Algorithm")
done = False
clock = pygame.time.Clock()

#Create Grid
grid = [[0 for j in range(HEIGHT)] for i in range(WIDTH)]

#Make background White
gridDisplay.fill(WHITE)

pygame.draw.circle(gridDisplay, MAGENTA, [90,HEIGHT - 70], 35)
pygame.draw.ellipse(gridDisplay, MAGENTA, [186, HEIGHT - 176, 120, 60], 0)

#Weird Shape
pygame.draw.polygon(gridDisplay, MAGENTA, [(285, HEIGHT - 105), (324, HEIGHT -144), (354, HEIGHT -138),(380,HEIGHT -171), (380,HEIGHT -116),(328,HEIGHT -63)])

#Roatated Rect
pygame.draw.polygon(gridDisplay, MAGENTA, [(36, HEIGHT - 124), (160, HEIGHT -210), (170, HEIGHT -194),(48,HEIGHT -108)])

#Broken Rect
pygame.draw.polygon(gridDisplay, MAGENTA, [(200, HEIGHT - 280), (230, HEIGHT -280), (230, HEIGHT -270),(200,HEIGHT -270)])
pygame.draw.polygon(gridDisplay, MAGENTA, [(200, HEIGHT - 270), (210, HEIGHT -270), (210, HEIGHT -240),(200,HEIGHT -240)])
pygame.draw.polygon(gridDisplay, MAGENTA, [(200, HEIGHT - 240), (230, HEIGHT -240), (230, HEIGHT -230),(200,HEIGHT -230)])
            
#Algorithm Driver   
start = Node(x1,y1)
start.distanceToReach = 0
end = Node(x2,y2)
robot = Graph()
robot.performDijkstra(start, end)

while not done:
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            done = True  

    for row in range(WIDTH):
        for column in range(HEIGHT):
            if grid[row][column] == 1:
                pygame.draw.rect(gridDisplay, BLACK,[row, HEIGHT - column, 2,2])
    
    clock.tick(144)
    pygame.display.flip()
 
pygame.quit()

