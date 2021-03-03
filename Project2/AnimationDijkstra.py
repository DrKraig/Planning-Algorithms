import pygame
import sys

HEIGHT = 300
WIDTH = 400
CELL_MARGIN = 0
CELL_WIDTH = 2
CELL_HEIGHT = 2

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
        print("-----------------------------------------------------")
        i, j = currentNode.i, currentNode.j
        neighbours ={}

        #Bottom
        if i > 0 and (not self.isAnObstacle(i-1, j)):
            #print("No Obstacle found at ", i-1, j)
            neighbours[tuple([i-1,j])] = 1
        
        #Left
        if j > 0 and (not self.isAnObstacle(i, j-1)):
            #print("No Obstacle found at ", i, j-1)
            neighbours[tuple([i,j-1])] = 1
        
        #Top
        if i < (HEIGHT -1) and (not self.isAnObstacle(i+1, j)):
            #print("No Obstacle found at ", i+1, j)
            neighbours[tuple([i+1,j])] = 1
        
        #Right
        if j < (WIDTH -1) and (not self.isAnObstacle(i, j+1)):
            #print("No Obstacle found at ", i, j+1)
            neighbours[tuple([i,j+1])] = 1
        
        #TopLeft 
        if j > 0 and i < (HEIGHT-1) and (not self.isAnObstacle(i+1, j-1)):
            #print("No Obstacle found at ", i+1, j-1)
            neighbours[tuple([i+1, j-1])] = 1.41
        
        #TopRight 
        if j < (WIDTH-1) and i < (HEIGHT-1)and (not self.isAnObstacle(i+1, j+1)):
            #print("No Obstacle found at ", i+1, j+1)
            neighbours[tuple([i+1, j+1])] = 1.41
        
        #BottomLeft
        if i > 0 and j > 0 and (not self.isAnObstacle(i-1, j-1)):
            #print("No Obstacle found at ", i-1, j-1)
            neighbours[tuple([i-1, j-1])] = 1.41

        #BottomRight 
        if i > 0 and j < (WIDTH -1) and (not self.isAnObstacle(i-1, j+1)):
            #print("No Obstacle found at ", i-1, j+1)
            neighbours[tuple([i-1, j+1])] = 1.41
        
        print(neighbours, "are the neighbours of",i,j)
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
                    pygame.draw.rect(gridDisplay,BLUE,[(CELL_MARGIN + CELL_WIDTH) * i + CELL_MARGIN,(CELL_MARGIN + CELL_HEIGHT) * (HEIGHT - j) + CELL_MARGIN,CELL_WIDTH, CELL_HEIGHT])
                    pygame.display.update()
                else:    
                    pygame.draw.rect(gridDisplay,CYAN,[(CELL_MARGIN + CELL_WIDTH) * i + CELL_MARGIN,(CELL_MARGIN + CELL_HEIGHT) * (HEIGHT - j) + CELL_MARGIN,CELL_WIDTH, CELL_HEIGHT])
                    pygame.display.update()
                neighbourNode.distanceToReach = currentDistance + newDistance
                neighbourNode.parent = currentNode
                priorityQueue.append(neighbourNode)

        print("Cannot find a path :(")

    def backTrack(self, child):
        while child != None:
            print(child.i, child.j)
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
        horizontalRadius = 60
        verticalRadius = 30
        centerX = 246
        centerY = 145
        if  (((x- centerX)**2)/horizontalRadius**2) + (((y- centerY)**2)/verticalRadius**2) - 1< 0:
            return True
        else:
            return False

    def isInPolygon(self, x,y):
        if (y + .99*x - 389.3) > 0  and (y - x + 181.6) < 0 and (y - 1.13*x - 260.75) < 0 and (y + 0.29*x - 240.6022) < 0 and (y + 250*x -95054) < 0 and (y - x + 266) > 0:
            return True
        else:
            return False


    def isAnObstacle(self,x,y):
        # return self.isInTestCircle(x,y) or self.isInTestCircleTwo(x,y)
        return self.isInEllipse(x,y) or self.isInBrokenRectangle(x,y) or self.isInCircle(x,y) or self.isInRectangle(x,y) or self.isInPolygon(x,y)

# i1 = int(input("Enter the ith coordiante of the starting point: "))
# j1 = int(input("Enter the jth coordiante of the starting point: "))

# i2 = int(input("Enter the ith coordiante of the ending point: "))
# j2 = int(input("Enter the jth coordiante of the ending point: "))

i1 = 0
j1 = 0

i2 = 20
j2 = 20

pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
gridDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dijkstra's Algorithm")
done = False
clock = pygame.time.Clock()

#PyGame Code
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
MAGENTA =(255,0,255)
#Create Grid
grid = []
print(HEIGHT)
print(WIDTH)
for row in range(HEIGHT):
    grid.append([])
    for column in range(WIDTH):
        grid[row].append(0)

obj = Graph()
#Make background White
print(HEIGHT)
print(WIDTH)

for row in range(HEIGHT):
    for column in range(WIDTH):
        pygame.draw.rect(gridDisplay, WHITE,[(CELL_MARGIN + CELL_WIDTH) * column + CELL_MARGIN, (CELL_MARGIN + CELL_HEIGHT ) * (  row) + CELL_MARGIN, CELL_WIDTH,CELL_HEIGHT ])

for row in range(HEIGHT):
    for column in range(WIDTH):
        # if obj.isInEllipse(row, column):    
        #     pygame.draw.rect(gridDisplay, MAGENTA,[(CELL_MARGIN + CELL_WIDTH) * row + CELL_MARGIN, (CELL_MARGIN + CELL_HEIGHT ) * (HEIGHT - column) + CELL_MARGIN, CELL_WIDTH,CELL_HEIGHT ])
        if obj.isInCircle(row, column):
            pygame.draw.rect(gridDisplay, MAGENTA,[(CELL_MARGIN + CELL_WIDTH) * row + CELL_MARGIN, (CELL_MARGIN + CELL_HEIGHT ) * (HEIGHT - column) + CELL_MARGIN, CELL_WIDTH,CELL_HEIGHT ])
        if obj.isInRectangle(row, column):
            pygame.draw.rect(gridDisplay, MAGENTA,[(CELL_MARGIN + CELL_WIDTH) * row + CELL_MARGIN, (CELL_MARGIN + CELL_HEIGHT ) * (HEIGHT - column) + CELL_MARGIN, CELL_WIDTH,CELL_HEIGHT ])
        if obj.isInBrokenRectangle(row, column):
            pygame.draw.rect(gridDisplay, MAGENTA,[(CELL_MARGIN + CELL_WIDTH) * row + CELL_MARGIN, (CELL_MARGIN + CELL_HEIGHT ) * (HEIGHT - column) + CELL_MARGIN, CELL_WIDTH,CELL_HEIGHT ])
        if obj.isInPolygon(row, column):    
            pygame.draw.rect(gridDisplay, MAGENTA,[(CELL_MARGIN + CELL_WIDTH) * row + CELL_MARGIN, (CELL_MARGIN + CELL_HEIGHT ) * (HEIGHT - column) + CELL_MARGIN, CELL_WIDTH,CELL_HEIGHT ])

pygame.draw.ellipse(gridDisplay, MAGENTA, [WIDTH - 186, WIDTH - 176, 120, 60], 0)

            
#Algorithm Driver   
start = Node(i1,j1)
start.distanceToReach = 0
end = Node(i2,j2)
robot = Graph()
robot.performDijkstra(start, end)


while not done:
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            done = True  

    for row in range(HEIGHT):
        for column in range(WIDTH):
            if grid[row][column] == 1:
                pygame.draw.rect(gridDisplay, BLACK,[(CELL_MARGIN + CELL_WIDTH) * row + CELL_MARGIN, (CELL_MARGIN + CELL_HEIGHT) * (HEIGHT - column) + CELL_MARGIN, CELL_WIDTH,CELL_HEIGHT ])
    
    clock.tick(60)
    pygame.display.flip()
 
pygame.quit()

