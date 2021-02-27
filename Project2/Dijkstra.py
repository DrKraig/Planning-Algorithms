import heapq
import pygame

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
        self.gridDisplay = pygame.display.set_mode((400, 300))

    def generateGraph(self):

        for i in range(self.height):
            for j in range(self.width):
                currentNode = Node(i,j)
                pygame.draw.rect(self.gridDisplay, color, [i, j, 10, 10 ])
                neighbours = self.getNeighbours(currentNode)
                #Add Neighbours to each node
                #Node(currentNode.addNeighbours)
        pygame.display.update()

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


obj = Graph()
obj.generateGraph()

start = Node(0,0)
end = Node(300,400)
robot = Graph()
# robot.performDijkstra(start, end)

