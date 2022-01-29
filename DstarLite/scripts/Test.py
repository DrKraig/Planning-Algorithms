import numpy as np
import matplotlib.pyplot as plt
import threading
import time
import heapq
import copy

class Map:
    dirs1 = [[0,1], [0, -1], [1,0], [0,1]]
    dirs2 = [[1,1,], [1,-1], [-1,1], [-1,-1]]
    nodes = {}
    m = 30
    n = 30
    def __init__(self):
        for row in range(Map.m):
            for col in range(Map.n):
                hash_str = str(row) + "," + str(col) 
                self.nodes[hash_str]  = Node(row,col)
        for node in Map.nodes.values():
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
        self.k1 = 0
        self.k2 = 0
        self.deleted = True

    def __lt__(self,other):
        if self.k1 == other.k1:
            return self.k2 < other.k2
        else:
            return self.k1 < other.k1
    def __ne__(self,other):
        if self.posI != other.posI or self.posJ != other.posJ:
            return True
        else:
            return False

    #O(8) Number of directions
    def getChild(self):
        for dir in Map.dirs1:
            newPosI = dir[0] + self.posI
            newPosJ = dir[1] + self.posJ
            if newPosI >= 0 and newPosI < Map.m and newPosJ >= 0 and newPosJ < Map.n:
                hash_str = str(newPosI) + "," + str(newPosJ) 
                self.child[Map.nodes[hash_str]] = 1.0
        for dir in Map.dirs2:
            newPosI = dir[0] + self.posI
            newPosJ = dir[1] + self.posJ
            if newPosI >= 0 and newPosI < Map.m and newPosJ >= 0 and newPosJ < Map.n:
                hash_str = str(newPosI) + "," + str(newPosJ) 
                self.child[Map.nodes[hash_str]] = np.sqrt(2)

class plotter():
    U = []
    def __init__(self,fig,ax,m,n,Is,Js,Ig,Jg):
        self.fig = fig
        self.ax = ax
        self.map_img = np.zeros((m,n),dtype=np.int32)
        self.map = Map()
        self.km = 0
        self.goal = self.map.nodes[str(Ig)+','+str(Jg)]
        self.start = self.map.nodes[str(Is)+','+str(Js)]
        self.goal.rhs = 0
        self.insert_in_queue(self.goal,[self.heuristic(self.goal),0])    

    def update_plot(self):
        self.ax.clear()
        self.ax.imshow(self.map_img)
        self.ax.set_xlim(0, 30)
        self.ax.set_ylim(0, 30)
        vertices = self.fig.ginput(n=-1,timeout=30)
        for vertex in vertices:
            self.map_img[int(round(vertex[1])),int(round(vertex[0]))] = 255
        plt.pause(0.01)
    
    def heuristic(self,node):
        h = np.linalg.norm([node.posI-self.start.posI,node.posJ-self.start.posJ])
        return h

    def CalculateKey(self,node):
        return [min(node.g,node.rhs)+self.heuristic(node)+self.km, min(node.g,node.rhs)]

    def update_queue(self,node,key):
        node.k1 = key[0]
        node.k2 = key[1]
        topnode = heapq.heappop(plotter.U)
        heapq.heappush(plotter.U,topnode)
    
    def insert_in_queue(self,node,key):
        node.k1 = key[0]
        node.k2 = key[1]
        heapq.heappush(plotter.U,node)
        node.deleted = False

    def delete_from_queue(self,node):
        node.deleted = True

    def update_vertex(self,node):
        if node.g != node.rhs and not node.deleted:
            self.update_queue(node,self.CalculateKey(node))
        elif node.g != node.rhs and node.deleted:
            self.insert_in_queue(node,self.CalculateKey(node))
        elif node.g == node.rhs and not node.deleted:
            self.delete_from_queue(node)
    
    def check_map_changes(self):
        # run over all grid locations in the updated map image 
        for row in range(self.map_img.shape[0]):
            for col in range(self.map_img.shape[1]):
                hash_str = str(row) + ',' + str(col)
                node = Map.nodes[hash_str]
                # Check for grid location which changed 
                # according to the noself.map.nodes[hash_str]des map in Map class object
                # in map_img 0 is free and 1 is obstacle
                # in no.isObstacle False is free and True is obstacle
                if node.isObstacle != self.map_img[row][col]: 
                    print("changes detected here",row,col)
                    #Update the vertex status
                    node.isObstacle = not node.isObstacle
                    node.isChanged = True
                    for c in node.child:
                        # updating parents edge costs
                        if node.isObstacle:
                            node.child[c] = float('inf')
                        else:
                            node.child[c] = np.linalg.norm([node.posI-c.posI,node.posJ-c.posJ])
                        c.isChanged = True
                        # updating respective childs edge costs
                        for p in c.child:
                            if p.posI == node.posI and p.posJ == node.posJ:
                                if node.isObstacle:
                                    c.child[p] = float('inf')
                                else:
                                    c.child[p] = np.linalg.norm([p.posI-c.posI,p.posJ-c.posJ])                                 
        # run a loop over the nodes map to update all vertices which changed
        # create isChanged attribute for node for checking in this loop
        for node in Map.nodes.values():
            if node.isChanged:
                # self.update_vertex(node)
                node.isChanged = False
                    
    def compute_shortest_path(self):
        # need to check for nodes deleted in in U !!!!!!
        #
        #
        while [plotter.U[0].k1,plotter.U[0].k2] < self.CalculateKey(self.start) or self.start.rhs > self.start.g:
            u = plotter.U[0]
            k_old = [u.k1,u.k2]
            k_new = self.CalculateKey(u)
            if k_old < k_new:
                self.update_queue(u,k_new)
            elif u.g > u.rhs:
                u.g = u.rhs
                self.delete_from_queue(u)
                for s in u.child.keys():
                    if s != self.goal:
                        s.rhs = float("inf")
                        for sp,c in s.child:
                            new_rhs = c + sp.g 
                            if s.rhs < new_rhs:
                                s.rhs = new_rhs
                    self.update_vertex(s)
            else:
                g_old = u.g
                u.g = float("inf")
                union_dict = copy.deepcopy(u.child)
                union_dict[u] = 0
                for s,c in union_dict:
                    if s.rhs == c+g_old:
                        if s != self.goal:
                            s.rhs = float("inf")
                            for sp,cp in s.child:
                                new_rhs = cp + sp.g 
                                if s.rhs < new_rhs:
                                    s.rhs = new_rhs
                    self.update_vertex(s)

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
    drawing1 = plotter(fig,ax1,30,30)
    print(Map.nodes["2,2"].child[Map.nodes["2,1"]])
    drawing1.check_map_changes()
    drawing1.map_img[2:4,2:4] = 1
    drawing1.check_map_changes()
    print(Map.nodes["2,2"].child[Map.nodes["2,1"]])

if __name__ == '__main__':
    main()

