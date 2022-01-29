import numpy as np
import matplotlib.pyplot as plt
import threading
import time


class Map:
    dirs = [[0,1], [0, -1], [1,0], [0,1], [1,1,], [1,-1], [-1,1], [-1,-1]]
    def __init__(self,m,n):
        self.nodes = {}
        self.m = m
        self.n = n
        for row in range(m):
            for col in range(n):
                hash_str = str(row) + "," + str(col) 
                self.nodes[hash_str]  = Node(row,col)
        for node in self.nodes.values():
            node.getChild()

    
class Node(Map):
    def __init__(self,row,col):
        self.posI = row
        self.posJ = col
        self.back_ptr = None
        self.child = {}
        self.isObstacle = False
        self.isChanged = False
        self.g = float("inf")
        self.rhs = float("inf")

    #O(8) Number of directions
    def getChild(self):
        for dir in Map.dirs:
            newPosI = dir[0] + self.posI
            newPosJ = dir[1] + self.posJ
            if newPosI >= 0 and newPosI < self.m and newPosJ >= 0 and newPosJ < self.n:
                hash_str = str(newPosI) + "," + str(newPosJ) 
                self.child[self.nodes[hash_str]] = 1


class plotter():
    def __init__(self,fig,ax,m,n):
        self.fig = fig
        self.ax = ax
        self.map_img = np.zeros((m,n),dtype=np.int32)
        self.map = Map(m,n)

    def update_plot(self):
        self.ax.clear()
        self.ax.imshow(self.map_img)
        self.ax.set_xlim(0, 30)
        self.ax.set_ylim(0, 30)
        vertices = self.fig.ginput(n=-1,timeout=30)
        for vertex in vertices:
            self.map_img[int(round(vertex[1])),int(round(vertex[0]))] = 255
        plt.pause(0.01)
    
    def check_map_changes(self):
        # run over all grid locations in the updated map image 
        for row in range(self.map_img.shape[0]):
            for col in range(self.map_img.shape[1]):
                hash_str = str(row) + ',' + str(col)
                node = self.map.nodes[hash_str]
                # Check for grid location which changed 
                # according to the noself.map.nodes[hash_str]des map in Map class object
                # in map_img 0 is free and 1 is obstacle
                # in no.isObstacle False is free and True is obstacle                
                if node.isObstacle != self.map_img[row][col]: 
                    #Update the vertex status
                    node.isObstacle = not node.isObstacle
                    node.isChanged = True
                    for c in node.child:
                        # updating parents edge costs
                        if node.isObstacle:
                            node.child[c] = float('inf')
                        else:
                            node.child[c] = 1
                        c.isChanged = True
                        # updating respective childs edge costs
                        for p in c.child:
                            if p.PosI == node.PosI and p.PosJ == node.PosJ:
                                if node.isObstacle:
                                    c.child[p] = float('inf')
                                else:
                                    c.child[p] = 1                                 
        # run a loop over the nodes map to update all vertices which changed
        # create isChanged attribute for node for checking in this loop
        for node in self.map.nodes.values():
            if node.isChanged:
                self.update_vertex(node)
                node.isChanged = False
                    
                   
    
    def compute_shortest_path(self):
        return

    def thread_function(self):
        while True:
            print("hey")
            #vertices = self.fig2.ginput(n=1,timeout=30)
            # print(vertices)
            # self.data[] = 
            time.sleep(5)


def main():
    fig,ax1 = plt.subplots()
    fig.set_size_inches(6, 12)
    ax1.set_xlim(0, 30)
    ax1.set_ylim(0, 30)
    ax1.axes.xaxis.set_visible(False)
    ax1.axes.yaxis.set_visible(False)
    drawing1 = plotter(fig,ax1)
    # This will enable the script to run even after plt.show()
    plt.ion()
    plt.axis('equal')
    plt.suptitle("Map",fontsize=22,y=0.94)
    
    # This will display the plot
    drawing1.update_plot()
    plt.pause(0.01)
    x = threading.Thread(target=drawing1.thread_function, args=())
    x.start()
    while True:
        drawing1.update_plot()


if __name__ == '__main__':
    main()

