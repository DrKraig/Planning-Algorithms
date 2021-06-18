import numpy as np

# defining a node class
class CreateNode:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.next = None
        return

# defining a queue class
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        return

    def EnQueue(self, item):
        if self.front == None:
            self.front = item
            self.rear = item
        else:
            self.rear.next = item
            self.rear = self.rear.next
        self.rear.next = None
        print("Enqueued!")
        return

    def DeQueue(self):
        if self.front is None:
            print("Trying to Dequeue an empty queue")
            return None
        else:
            ans = self.front
            self.front = self.front.next
            print("Dequeued!")
            return ans

# function for unrolling a matrix into a integer (represented in hexadecimal)
def unroll(matrix):
    k = 15
    b = 0
    for row in matrix:
        for ele in row:
            b = b + int(ele * pow(16, k))
            k = k - 1
    return b

# function for rolling an integer (represented in hexadecimal) into a matrix
def roll(b):
    matrix = np.zeros((4, 4))
    strb = '0x%0*x' % (16,b)
    for i in range(0, 4):
        for j in range(0, 4):
            matrix[i][j] = int(strb[4*i+j+2], 16)
    return matrix

# function for finding position of zero in a matrix
def find0(matrix):
    pos = np.array([4, 4])
    for i in range(0, 4):
        for j in range(0, 4):
            if matrix[i][j] == 0:
                pos = [i, j]
    print(pos)
    return pos

# function for moving position of zero to the right and returning a new child node for it
def MoveRight(node, mat, pos):
    [i, j] = pos
    matrix = np.array(mat)
    temp = matrix[i][j+1]
    matrix[i][j] = temp
    matrix[i][j+1] = 0
    child = CreateNode(unroll(matrix))
    child.parent = node
    print("created a right child")
    return child

# function for moving position of zero to the left and returning a new child node for it
def MoveLeft(node, mat, pos):
    [i, j] = pos
    matrix = np.array(mat)
    temp = matrix[i][j-1]
    matrix[i][j] = temp
    matrix[i][j-1] = 0
    child = CreateNode(unroll(matrix))
    child.parent = node
    print("created a left child")
    return child

# function for moving position of zero up and returning a new child node for it
def MoveUp(node, mat, pos):
    [i, j] = pos
    matrix = np.array(mat)
    temp = matrix[i-1][j]
    matrix[i][j] = temp
    matrix[i-1][j] = 0
    child = CreateNode(unroll(matrix))
    child.parent = node
    print("created a up child")
    return child

# function for moving position of zero down and returning a new child node for it
def MoveDown(node, mat, pos):
    [i, j] = pos
    matrix = np.array(mat)
    temp = matrix[i+1][j]
    matrix[i][j] = temp
    matrix[i+1][j] = 0
    child = CreateNode(unroll(matrix))
    child.parent = node
    print("created a down child")
    return child

queue = Queue() # creating an empty queue

#testcase = np.array([[1, 2, 3, 4], [5, 6, 0, 8], [9, 10, 7, 12], [13, 14, 11, 15]])  # Testcase 1
#testcase = np.array([[1, 0, 3, 4], [5, 2, 7, 8], [9, 6, 10, 11], [13, 14, 15, 12]])  # Testcase 2
#testcase = np.array([[0, 2, 3, 4], [1, 5, 7, 8], [9, 6, 11, 12], [13, 10, 14, 15]])  # Testcase 3
testcase = np.array([[5, 1, 2, 3], [0, 6, 7, 4], [9, 10, 11, 8], [13, 14, 15, 12]])  # Testcase 4
#testcase = np.array([[1, 6, 2, 3], [9, 5, 7, 4], [0, 10, 11, 8], [13, 14, 15, 12]])  # Testcase 5

solution = 0x123456789abcdef0  # solution for checking the child nodes
child = None
root_node = CreateNode(unroll(testcase))  # creating a node from our testcase

queue.EnQueue(root_node)  # adding the first node to queue

while True:
    new_node = queue.DeQueue()  # obtaining the next node from the queue

    reader = queue.front
    bul = True
    # check for repeation of the node in the queue
    if reader != None:
        while reader.next != None:
            if reader.data == new_node.data:
                bul = False
                break
            temp = reader.next
            reader = temp

    # if it is new find new nodes by performing actions
    if bul:
        current_state = roll(new_node.data)
        p = find0(current_state)
        # perform move up action if possible
        if p[0] > 0:
            child_node_u = MoveUp(new_node, current_state, p)
            if child_node_u.data == solution:  # exit if solution is found
                child = child_node_u
                break
            else:
                queue.EnQueue(child_node_u)  # if it's not the solution add to the queue
        # perform move down action if possible
        if p[0] < 3:
            child_node_d = MoveDown(new_node, current_state, p)
            if child_node_d.data == solution:  # exit if solution is found
                child = child_node_d
                break
            else:
                queue.EnQueue(child_node_d)  # if it's not the solution add to the queue
        # perform move right action if possible
        if p[1] < 3:
            child_node_r = MoveRight(new_node, current_state, p)
            if child_node_r.data == solution:  # exit if solution is found
                child = child_node_r
                break
            else:
                queue.EnQueue(child_node_r)  # if it's not the solution add to the queue
        # perform move left action if possible
        if p[1] > 0:
            child_node_l = MoveLeft(new_node, current_state, p)
            if child_node_l.data == solution:  # exit if solution is found
                child = child_node_l
                break
            else:
                queue.EnQueue(child_node_l)  # if it's not the solution add to the queue


count = -1
nodelist = []
while child != None:  # Storing the nodes values in an list for returning
    state = roll(child.data)
    state_string = '\n'.join('\t'.join('%d' % x for x in y) for y in state)
    nodelist.insert(0, state_string)
    child = child.parent
    count = count+1

# writing the output in text file
file1 = open("./Output/nodePath.txt", "w")
file1.write("Each node is represented in its matrix form \n")
file1.write("The order of states is from start to goal node \n")
file1.write("Number steps taken are - ",length(nodelist))
for ele in nodelist:
    file1.write("\n\n")
    file1.write(ele)