import heapq
import pygame
import sys

class Node:

    def __init__(self, i ,j):
        self.i = i
        self.j = j
        self.distanceToReach = float('inf')
        self.neighbours = {}
        self.parent = None
        self.obstacle = False

    def addNeighbours(self, neighbours):
        self.neighbours = neighbours

class Graph:
    def __init__(self):
        self.height = 300
        self.width = 400

        self.CELL_MARGIN = .5
        self.CELL_WIDTH = 2
        self.CELL_HEIGHT = 2

    def generateGraph(self):

        for i in range(self.height):
            for j in range(self.width):
                currentNode = Node(i,j)
                pygame.draw.rect(gridDisplay,(255,255,255),[(self.CELL_MARGIN + self.CELL_WIDTH) * j + self.CELL_MARGIN,(self.CELL_MARGIN + self.CELL_HEIGHT) * i + self.CELL_MARGIN,self.CELL_WIDTH, self.CELL_HEIGHT])
                pygame.display.update()
                neighbours = self.getNeighbours(currentNode)

                #Add Neighbours to each node
                #Node(currentNode.addNeighbours)

    def getNeighbours(self, currentNode):
        i, j = currentNode.i, currentNode.j
        neighbours ={}

        #Top
        if i > 0:
            neighbours[Node(i-1,j)] = 1
        
        #Left
        if j > 0:
            neighbours[Node(i,j-1)] = 1
        
        #Bottom
        if i < (self.height -1):
            neighbours[Node(i+1,j)] = 1
        
        #Right
        if j < (self.width -1):
            neighbours[Node(i,j+1)] = 1
        
        #BottomLeft 
        if j > 0 and i < (self.height-1):
            neighbours[Node(i+1, j-1)] = 2
        
        #BottomRight 
        if j < (self.width-1) and i < (self.height-1):
            neighbours[Node(i+1, j-1)] = 2
        
        #TopLeft 
        if i > 0 and j > 0:
            neighbours[Node(i-1, j-1)] = 2

        #TopRight 
        if i > 0 and j < (self.width -1):
            neighbours[Node(i-1, j+1)] = 2
        
        print(neighbours)
        return neighbours

    def performDijkstra(self, start, end):
        priorityQueue = [start]
        while priorityQueue:

            #Assuming this will work
            currentNode = heapq.heappop(priorityQueue)
            
            if currentNode == end:
                print("TRUE")
                self.backTrack(end) 
            
            currentDistance = currentNode.distanceToReach

            #Key = Neighbour, Value = Distance
            for neighbour, distanceToReachNeighbour in currentNode.neighbours:
                
                #Add Wall condition
                #TODO

                neighbour.distanceToReach = currentDistance + distanceToReachNeighbour
                neighbour.parent = currentNode
                heapq.heappush(priorityQueue, neighbour)



    def backTrack(self, end):
        pass

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

grid = []
for row in range(300):
    grid.append([])
    for column in range(400):
        grid[row].append(0)

pygame.init()
gridDisplay = pygame.display.set_mode((1000, 750))
pygame.display.set_caption("First Game")

done = False
clock = pygame.time.Clock()

obj = Graph()
obj.generateGraph()
start = Node(0,0)
end = Node(50,50)
robot = Graph()
robot.performDijkstra(start, end)

while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     # User clicks the mouse. Get the position
        #     pos = pygame.mouse.get_pos()
        #     # Change the x/y screen coordinates to grid coordinates
        #     column = pos[0] // (WIDTH + MARGIN)
        #     row = pos[1] // (HEIGHT + MARGIN)
        #     # Set that location to one
        #     grid[row][column] = 1
        #     print("Click ", pos, "Grid coordinates: ", row, column)
 
    # Set the screen background 
    # Draw the grid
    # for row in range(10):
    #     for column in range(10):
    #         color = WHITE
    #         if grid[row][column] == 1:
    #             color = GREEN

 
    clock.tick(144)
 
    pygame.display.flip()
 
pygame.quit()




# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
    