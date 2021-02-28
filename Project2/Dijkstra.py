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

class Graph:
    def __init__(self):
        self.height= 5
        self.width = 5

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
        # print("-----------------------------------------------------")
        i, j = currentNode.i, currentNode.j
        neighbours ={}

        #Top
        if i > 0:
            neighbours[tuple([i-1,j])] = 1
        
        #Left
        if j > 0:
            neighbours[tuple([i,j-1])] = 1
        
        #Bottom
        if i < (self.height -1):
            neighbours[tuple([i+1,j])] = 1
        
        #Right
        if j < (self.width -1):
            neighbours[tuple([i,j+1])] = 1
        
        #BottomLeft 
        if j > 0 and i < (self.height-1):
            neighbours[tuple([i+1, j-1])] = 2
        
        #BottomRight 
        if j < (self.width-1) and i < (self.height-1):
            neighbours[tuple([i+1, j+1])] = 2
        
        #TopLeft 
        if i > 0 and j > 0:
            neighbours[tuple([i-1, j-1])] = 2

        #TopRight 
        if i > 0 and j < (self.width -1):
            neighbours[tuple([i-1, j+1])] = 2
        
        # print(neighbours, "are the neighbours of",i,j)
        return neighbours

    def performDijkstra(self, start, end):
        priorityQueue = [start]
        while len(priorityQueue):
            #Assuming this will work
            currentNode = heapq.heappop(priorityQueue)
            if currentNode.i == end.i and currentNode.j == end.j:
                print("Found it!")
                self.backTrack(currentNode)
                print("Distance Required to reach from start to end is:", currentNode.distanceToReach)
                return
                 
            currentDistance = currentNode.distanceToReach
            neighbours = self.getNeighbours(currentNode)
            for neighbour, newDistance in neighbours.items():
                
                #Add Wall condition
                neighbourNode = Node(neighbour[0], neighbour[1])
                neighbourNode.distanceToReach = currentDistance + newDistance

                neighbourNode.parent = currentNode
                heapq.heappush(priorityQueue, neighbourNode)

        print("Cannot find a path :(")


    def backTrack(self, child):
        while child != None:
            print(child.i, child.j)
            child = child.parent
        return True
        


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

grid = []
for row in range(5):
    grid.append([])
    for column in range(5):
        grid[row].append(0)

# pygame.init()
# gridDisplay = pygame.display.set_mode((100, 100))
# pygame.display.set_caption("First Game")

done = False
clock = pygame.time.Clock()

start = Node(0,0)
start.distanceToReach = 0
end = Node(1,1)
robot = Graph()
robot.performDijkstra(start, end)

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

