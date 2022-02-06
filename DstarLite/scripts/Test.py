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
        print("Inside this!")
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
        self.map_img[int(round(Is)),int(round(Js))] = 150
        self.map_img[int(round(Ig)),int(round(Jg))] = 25
        self.map_img_test = np.zeros((m,n))
        self.map = Map()
        self.km = 0
        self.goal = self.map.nodes[str(Ig)+','+str(Jg)]
        self.start = self.map.nodes[str(Is)+','+str(Js)]
        self.last = copy.copy(self.start)
        self.goal.rhs = 0
        self.insert_in_queue(self.goal,[self.heuristic(self.goal),0])    

    def update_plot(self):
        self.ax.clear()
        self.ax.imshow(self.map_img)
        self.ax.set_xlim(0, 30)
        self.ax.set_ylim(0, 30)
        plt.pause(0.01)
        vertices = self.fig.ginput(n=-1,timeout=5)
        for vertex in vertices:
            self.map_img[int(round(vertex[1])),int(round(vertex[0]))] = 255
        plt.pause(0.01)
    
    def update_test_map(self):
        for node in self.map.nodes.values():
            if node.g == float('inf'):
                self.map_img_test[int(node.posI)][int(node.posJ)] = 30
            else:
                self.map_img_test[int(node.posI)][int(node.posJ)] = node.g

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
        heapq.heappush(plotter.U, node)
        node.deleted = False

    def delete_from_queue(self,node):
        node.deleted = True

    def update_vertex(self,node):
        # print("Inside update vertex")
        # print(node.g, "G value")
        # print(node.rhs, "RHS")

        if node.g != node.rhs and not node.deleted:
            # print("Updating!")
            self.update_queue(node,self.CalculateKey(node))
        elif node.g != node.rhs and node.deleted:
            # print("Inserting!")
            self.insert_in_queue(node,self.CalculateKey(node))
        elif node.g == node.rhs and not node.deleted:
            # print("Deleting!")
            self.delete_from_queue(node)

    def topnode(self):
        while plotter.U[0].deleted:
            heapq.heappop(plotter.U)
        return plotter.U[0]

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
                if (node.isObstacle == True and self.map_img[row][col] == 0) or \
                   (node.isObstacle == False and self.map_img[row][col] == 255): 
                    # print("changes detected here",row,col)
                    #Update the vertex status
                    node.isObstacle = not node.isObstacle
                    node.isChanged = True
                    ## To do!!! optimisation over edge costs!!!
                    for c in node.child.keys():
                        # updating parents edge costs
                        if node.isObstacle:
                            node.child[c] = float('inf')
                        else:
                            node.child[c] = np.linalg.norm([node.posI-c.posI,node.posJ-c.posJ])
                        c.isChanged = True
                        # updating respective childs edge costs
                        for p in c.child.keys():
                            if p.posI == node.posI and p.posJ == node.posJ:
                                if node.isObstacle:
                                    c.child[p] = float('inf')
                                else:
                                    c.child[p] = np.linalg.norm([p.posI-c.posI,p.posJ-c.posJ])                                 
        # run a loop over the nodes map to update all vertices which changed
        # create isChanged attribute for node for checking in this loop
        change_flag = True
        for node in Map.nodes.values():
            if node.isChanged:
                if change_flag:
                    self.km += self.heuristic(self.last)
                    self.last = copy.copy(self.start)
                    change_flag = False
                self.update_vertex(node)
                node.isChanged = False
                    
    def compute_shortest_path(self):

        # print("in here!")
        while [self.topnode().k1,self.topnode().k2] < self.CalculateKey(self.start) or self.start.rhs > self.start.g:
            # print("looping")
            u = plotter.U[0]
            # print(u.deleted)
            k_old = [u.k1,u.k2]
            k_new = self.CalculateKey(u)
            if k_old < k_new:
                print("0th statement")
                self.update_queue(u,k_new)
            elif u.g > u.rhs:
                print("1st statement")
                u.g = u.rhs
                print(u.g, u.rhs)
                self.delete_from_queue(u)

                for s, c in u.child.items():
                    if s != self.goal:
                        s.rhs = min(s.rhs, c + u.g)
                    # print("First update vertex")
                    self.update_vertex(s)
            else:
                # print("Node:", u.posI, u.posJ, u.g, u.rhs)
                g_old = u.g
                u.g = float("inf")
                union_dict = copy.copy(u.child)
                union_dict[u] = 0
                for s,c in union_dict.items():
                    if s.rhs == c+g_old:
                        if s != self.goal:
                            s.rhs = float("inf")
                            for sp,cp in s.child.items():
                                new_rhs = cp + sp.g 
                                if s.rhs < new_rhs:
                                    s.rhs = new_rhs
                    print("Second update vertex")
                    self.update_vertex(s)

    def thread_function(self):
        print("started the thread")
        self.compute_shortest_path()
        print("startinh the loop")
        counter = 0
        while self.start != self.goal:
            print("beginning of the loop", counter)
            if self.start.rhs == float("inf"):
                print("No feasible Path")
                break
            # time.sleep(5)
            min_child_cost = float("inf")
            min_child = None
            for sp,c in self.start.child.items():
                if min_child_cost > c + sp.g:
                    min_child_cost = c + sp.g
                    min_child = sp
            self.start = min_child
            print("Current Pos: ", self.start.posI, " ", self.start.posJ)
            print("moved start", counter)
            self.map_img[int(round(self.start.posI)),int(round(self.start.posJ))] = 150
            
            time.sleep(1)
            self.check_map_changes()
            print("computing shortest path",  counter)
            self.compute_shortest_path()
            print("Computed shortest path", counter)
            self.update_test_map()
            counter += 1
        print("Goal Reached!")
def main():
    fig,ax1 = plt.subplots()
    fig.set_size_inches(6, 12)
    ax1.set_xlim(0, 30)
    ax1.set_ylim(0, 30)
    ax1.axes.xaxis.set_visible(False)
    ax1.axes.yaxis.set_visible(False)
    fig2,ax2 = plt.subplots()
    fig2.set_size_inches(6, 12)
    ax2.set_xlim(0, 30)
    ax2.set_ylim(0, 30)
    ax2.axes.xaxis.set_visible(False)
    ax2.axes.yaxis.set_visible(False)
    drawing1 = plotter(fig,ax1,30,30,2,2,15,15)
    x = threading.Thread(target=drawing1.thread_function, args=())
    x.start()
    while True:
        drawing1.update_plot()
        ax2.clear()
        ax2.imshow(drawing1.map_img_test)
        ax2.set_xlim(0, 30)
        ax2.set_ylim(0, 30)
        
        plt.pause(0.01)        
    # print(Map.nodes["2,2"].child[Map.nodes["2,1"]])
    # drawing1.check_map_changes()
    # drawing1.map_img[2:4,2:4] = 1
    # drawing1.check_map_changes()
    # print(Map.nodes["2,2"].child[Map.nodes["2,1"]])

if __name__ == '__main__':
    main()

