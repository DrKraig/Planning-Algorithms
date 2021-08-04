import numpy as np
import cv2
import math
import heapq

CLEARANCE = 0

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

def isInCircle(x, y):
    """
    Description: Checks if a point is in the circle.
    Input: Point with co-ordinates (x,y)
    Output: True or False
    """
    r = 35 + CLEARANCE
    if (x - 90) ** 2 + (y - 70) ** 2 - r**2 >= 0:
        return False
    else:
        return True

def isInRectangle(x, y):
    """
    Description: Checks if a point is in the rotated rectangle.
    Input: Point with co-ordinates (x,y)
    Output: True or False
    """
    circ1 = (x-48)**2 + (y-108)**2 <= CLEARANCE**2
    circ2 = (x-170.876)**2 + (y-194.044)**2 <= CLEARANCE**2
    circ3 = (x-159.4)**2 + (y-210.432)**2 <= CLEARANCE**2
    circ4 = (x-36.524)**2 + (y-124.387)**2 <= CLEARANCE**2
    side1 = 0.7*x - y + 74.39 <= 0
    eside1 = 0.7*x - y + 74.39 - 1.22*CLEARANCE <= 0
    side2 = -1.43*x - y + 176.55 <= 0
    eside2 = -1.43*x - y + 176.55 - 1.74*CLEARANCE <= 0
    side3 = 0.7*x - y + 98.81 >= 0
    eside3 = 0.7*x - y + 98.81 + 1.22*CLEARANCE >= 0
    side4 = -1.43*x - y + 438.06 >= 0
    eside4 = -1.43*x - y + 438.06 + 1.74*CLEARANCE >= 0
    rect1 = eside1 and side2 and eside3 and side4
    rect2 = side1 and eside2 and side3 and eside4

    if rect1 or rect2 or circ1 or circ2 or circ3 or circ4:
        return True
    else:
        return False

def isInBrokenRectangle(x, y):
    """
    Description: Checks if a point is in the top rectangle.
    Input: Point with co-ordinates (x,y)
    Output: True or False
    """
    rect1 = (y <= 280 + CLEARANCE) and (y >= 270 - CLEARANCE) and (x <= 230) and (x >= 200)
    rect2 = (y <= 280) and (y >= 270) and (x <= 230 + CLEARANCE) and (x >= 200 - CLEARANCE)
    rect3 = (y <= 270) and (y >= 240) and (x <= 210 + CLEARANCE) and (x >= 200 - CLEARANCE)
    rect4 = (y <= 240 + CLEARANCE) and (y >= 230 - CLEARANCE) and (x <= 230) and (x >= 200)
    rect5 = (y <= 240) and (y >= 230) and (x <= 230 + CLEARANCE) and (x >= 200 - CLEARANCE)
    circ1 = (x - 230) ** 2 + (y - 280) ** 2 <= CLEARANCE ** 2
    circ2 = (x - 200) ** 2 + (y - 280) ** 2 <= CLEARANCE ** 2
    circ3 = (x - 230) ** 2 + (y - 270) ** 2 <= CLEARANCE ** 2
    circ4 = (x - 230) ** 2 + (y - 240) ** 2 <= CLEARANCE ** 2
    circ5 = (x - 230) ** 2 + (y - 230) ** 2 <= CLEARANCE ** 2
    circ6 = (x - 200) ** 2 + (y - 230) ** 2 <= CLEARANCE ** 2

    if rect1 or rect2 or rect3 or rect4 or rect5 or circ1 or circ2 or circ3 or circ4 or circ5 or circ6:
        return True
    else:
        return False

def isInEllipse(x, y):
    """
    Description: Checks if a point is in the Ellipse.
    Input: Point with co-ordinates (x,y)
    Output: True or False
    """
    a = 60+CLEARANCE
    b = 30+CLEARANCE
    h = 246
    k = 145
    if ((math.pow((x - h), 2) / math.pow(a, 2)) + (math.pow((y - k), 2) / math.pow(b, 2))) <= 1:
        return True
    else:
        return False

def isOutsideArena(x, y):
    """
    Description: Checks if the point (x,y) is outside the areana or not.
    Input: Point with co-ordinates (x,y)
    Output: True or False
    """
    return True if x < CLEARANCE or y < CLEARANCE or x > 400-CLEARANCE or y > 300-CLEARANCE else False

def obstacle_space(point):
    """
    Description: Checks if the point (x,y) is inside an obstacle or not.
    Input: point with co-ordinates (x,y)
    Output: True or False
    """
    [x, y] = np.array(point)

    return isInEllipse(x, y) or isInBrokenRectangle(x, y) or isInCircle(x, y) or isInRectangle(
        x, y) or isOutsideArena(x,y)

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
out = cv2.VideoWriter('./Output/visualisation.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 1000, (frame_width,frame_height),isColor=True)

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