import numpy as np
import cv2
from math import pi
import heapq

# defining a node class
class CreateNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.cost = 0
        return

    def move(self,direction,field):
        action_set = np.array([[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1],[1,0],[1,1]])
        point = np.array([self.x+action_set[direction][0], self.y+action_set[direction][1]])
        if point[0] < 0 or point[0] > 300 or point[1] < 0 or point[1] > 400:
            child = None
        elif field[point[0]][point[1]] == 0:
            child = CreateNode(self.x+action_set[direction][0], self.y+action_set[direction][1])
            child.parent = self
            child.cost = self.cost + np.linalg.norm(action_set[direction])
        else:
            child = None
        return child

    def __lt__(self, other):
        return (self.x < other.x)

def hp(point,param):
    [x, y] = np.array(point)
    a = np.array(param)
    f = a[0] + a[1]*x + a[2]*y + a[3]*x**2 + a[4]*x*y + a[5]*y**2
    if a[7] == 1:
        if a[6]*f <= 0:
            return 1
        else:
            return 0
    else:
        if a[6]*f < 0:
            return 1
        else:
            return 0

def obstacle_space(point):
    para = np.zeros((5,8))

    m1 = np.tan((25/36)*pi)
    m2 = -1/m1
    para[0] = np.array([48-192*m1,m1,-1,0,0,0,-1,1])
    para[1] = np.array([48-192*m1-20*np.sqrt(1+m1**2),m1,-1,0,0,0,1,1])
    para[2] = np.array([48-192*m2,m2,-1,0,0,0,1,1])
    para[3] = np.array([48-192*m2+150*np.sqrt(1+m2**2),m2,-1,0,0,0,-1,1])
    rect1 = hp(point,para[0])
    for i in range(1,4):
        rect1 = rect1 & hp(point,para[i])

    para[0] = np.array([-20,1,0,0,0,0,-1,1])
    para[1] = np.array([-30,1,0,0,0,0,1,1])
    para[2] = np.array([-200,0,1,0,0,0,-1,1])
    para[3] = np.array([-230,0,1,0,0,0,1,1])
    rect2 = hp(point,para[0])
    for i in range(1,4):
        rect2 = rect2 & hp(point,para[i])

    para[0] = np.array([-30,1,0,0,0,0,-1,1])
    para[1] = np.array([-60,1,0,0,0,0,1,1])
    para[2] = np.array([-200,0,1,0,0,0,-1,1])
    para[3] = np.array([-210,0,1,0,0,0,1,1])
    rect3 = hp(point,para[0])
    for i in range(1,4):
        rect3 = rect3 & hp(point,para[i])

    para[0] = np.array([-60,1,0,0,0,0,-1,1])
    para[1] = np.array([-70,1,0,0,0,0,1,1])
    para[2] = np.array([-200,0,1,0,0,0,-1,1])
    para[3] = np.array([-230,0,1,0,0,0,1,1])
    rect4 = hp(point,para[0])
    for i in range(1,4):
        rect4 = rect4 & hp(point,para[i])

    para[0] = np.array([59775,-460,-180,1,0,1,1,1])
    circ = hp(point,para[0])

    para[0] = np.array([137714400,-1116000,-442800,3600,0,900,1,1])
    elip = hp(point,para[0])

    para[0] = np.array([0,0,1,0,0,0,1,0])
    para[1] = np.array([-400,0,1,0,0,0,-1,0])
    para[2] = np.array([0,1,0,0,0,0,1,0])
    para[3] = np.array([-300,1,0,0,0,0,-1,0])
    border = hp(point,para[0])
    for i in range(1,4):
        border = border | hp(point,para[i])

    return rect1 | rect2 | rect3 | rect4 | circ | elip | border

while True:
    inp = input("Please enter the start point as <your x> <your y> : ")
    val = inp.split()
    start = np.array([300 - int(val[1]), int(val[0])])
    if obstacle_space(start) == 0:
        print("your start point is ", np.array([int(val[0]), int(val[1])]))
        break
    else:
        print("The point you entered is in obstacle space please input another point\n")

while True:
    inp = input("Please enter the goal point as <your x> <your y> : ")
    val = inp.split()
    goal = np.array([300 - int(val[1]), int(val[0])])
    if obstacle_space(goal) == 0:
        print("your goal point is ", np.array([int(val[0]), int(val[1])]))
        break
    else:
        print("The point you entered is in obstacle space please input another point\n")

frame_width = 401
frame_height = 301
out = cv2.VideoWriter('visualisation.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 1000, (frame_width,frame_height),isColor=True)

frame = np.ones([frame_height, frame_width, 3],dtype=np.uint8)
space = np.zeros([frame_height, frame_width])
for i in range(0, 301):
    for j in range(0, 401):
        pixel = np.array([i, j])
        if obstacle_space(pixel) == 1:
            frame[i][j] = [200, 0, 0]
            space[i][j] = 1
        else:
            frame[i][j] = [0, 0, 0]
frame[start[0]][start[1]] = [0, 0, 200]
frame[goal[0]][goal[1]] = [0, 200, 0]
print("\n Computing the Path... \n")
cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
cv2.resizeWindow('frame',400,300)

queue = [] ## Creating an empty queue
start_node = CreateNode(start[0], start[1])
start_node.cost = 0.0
new_entry = str(start_node.x) + "," + str(start_node.y)
heapq.heappush(queue,(start_node.cost,start_node))
visited_list = {new_entry: start_node}
while len(queue):
    priorty_element = heapq.heappop(queue)
    new_node = priorty_element[1]
    if new_node.x == goal[0] and new_node.y == goal[1]:
        print("Solution Found!")
        break

    for i in range(0, 8):
        child_node = new_node.move(i,space)
        if child_node is not None:
            child_key = str(child_node.x) + "," + str(child_node.y)
            if not (child_key in visited_list):
                frame[child_node.x][child_node.y] = [255, 255, 255]
                cv2.imshow('frame',frame)
                k = cv2.waitKey(1)
                out.write(frame)
                visited_list[child_key] = child_node
                heapq.heappush(queue,(child_node.cost,child_node))
            else:
                existing_node = visited_list[child_key]
                if existing_node.cost > child_node.cost:
                    existing_node.cost = child_node.cost
                    existing_node.parent = child_node.parent

goal_key = str(goal[0]) + "," + str(goal[1])
backtrack_node = visited_list[goal_key]
while backtrack_node is not None:  # Storing the nodes values in an list for returning
    frame[backtrack_node.x][backtrack_node.y] = [0, 255, 0]
    backtrack_node = backtrack_node.parent
for i in range(0,1000):
    out.write(frame)
out.release()
cv2.destroyAllWindows()
