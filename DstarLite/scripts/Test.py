
#Node is a part of a map
#Node is a child of the map

#What is an object?
#Location - Memory addres - pointer

#static
class Map:
    static dirs
obj1 = Map()
obj1.dirs = 5

print(obj2.vairbale)

object1, object2
member


#Superclass
Class Map:
    #m*n
    nodes = {"00":Node, "01":Node}
    static dirs = [[0,1], [0, -1], [1,0], [0,1], [1,1,], [1,-1], [-1,1], [-1,-1]]

    def check4change():
        #Matplotlib updates a numpy array
        = numpy


        #Compare nodes(our old map) with numpy array(new map)

        for row in rows:
            for col in cols:
                #node ->u
               
                if( nodes[row][col] != numpy[row][col]) #there is a change
                    
                    #Update the vertex
                    node.isObstacle = True
                    
                    #Update the weights
                    #child ->v
                    for c in node.child:
                        #parent to child
                        node.child[c] = inf
                        updatevertex(node[row][col]) 

                        #Child to parent
                        #O(8)
                        #iterate thorugh childs children=parent
                            #if child has row and col == [row][col] it is a parent
                                #update weight to inf
                        updatevertex(c)

#Needed
Class Node(Map)(self, myconstant):
    posI = myconstant
    posJ = 0
    parent = Node()
    (0 1), (1,0), (1,1)
    child = {Node(): 5, Node(): 10, Node(): 15, Node(): 20}
    costToCome 
    isObstacle
    rhs

    #O(8) Number of directions
    def getChild():
        for dir in self.dirs:
        newPosI = dir[0] + posI[0]
        newPosJ = dir[1] + posI[1] 
        self.child.append(self.nodes[str(newPosI) + str(newPosJ)])



main():
    initlization()
    move the robot()

    check4change()
node1 = Node()
node1.dirs


int 
S
0 0 0 0 0 0
0 0 0 0 0 0 
0 0 0 0 0 0 
          G

currRow = 1
currCol = 6

child 

bfs():
queue = [(0,0)]
visited = set([])
dirs = [[0,1], [0, -1], [1,0], [0,1], [1,1,], [1,-1], [-1,1], [-1,-1]]

while queue.size() != 0:

    currPost = queue.pop()

    if ( currPOst == goalPos) return True

    #Get all child nodes
    for dir in dirs:
        newPosI = dir[0] + currPost[0]
        newPosJ = dir[1] + currPost[1]

        if ( newPosI >= 0 and newPosI < rows and newPosJ >=0 and newPosJ < cols ):
            queue.push([newPosI, newPosJ])





#Hash
Key, value

Key -> unique, determinstic, immutable


hashing function- Key


"10" "100"  num /0 = index
c++ : std::hash()
python: __qual

#not have collission
#ideally no colliosn:
