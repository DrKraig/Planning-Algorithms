#!/usr/bin/env python
import rospy
import math
import heapq
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class Node:
    """
    Node class : This class is built to store the node information.
    A node is simply a location on a map. For each node, its neighbours, parents & distance to reach that node is stored.
    """

    def __init__(self, i, j, endI, endJ, theta):
        """
        Description: Defining all properties for each node - Neighbours, Parents, Distance.
        """
        self.i = i
        self.j = j
        self.theta = theta
        self.costToCome = 0.0
        self.costToGo = 2.5 * (math.sqrt((i - endI) ** 2 + (j - endJ) ** 2))
        self.cost = None
        self.neighbours = {}
        self.valid_actions = {}
        self.parent = None

    def __lt__(self, other):
        return self.cost < other.cost


class Graph:
    """
    Graph class : This class defines all methods to generate a graph and perform AStar Algorithm.
    """

    def __init__(self, start, end, RPM1, RPM2, RADIUS, CLEARANCE):
        self.visited = {}
        self.endI = end.i
        self.endJ = end.j
        self.RPM1 = RPM1
        self.RPM2 = RPM2
        self.RADIUS = RADIUS
        self.CLEARANCE = CLEARANCE + self.RADIUS

    def getNeighbours(self, currentNode):
        """
        Description: Returns neighbours for the currentNode.
        """
        i, j, theta = currentNode.i, currentNode.j, currentNode.theta
        neighbours = {}
        valid_actions = {}
        actions = [[0, self.RPM1], [self.RPM1, 0], [self.RPM1, self.RPM1], [0, self.RPM2], [self.RPM2, 0],
                   [self.RPM2, self.RPM2], [self.RPM1, self.RPM2], [self.RPM2, self.RPM1]]
        for UL, UR in actions:
            x, y, newTheta, distance, lin_vel, ang_vel = self.getNewCoordiantes(i, j, theta, UL, UR)
            if (not self.isOutsideArena(x, y)) and (not self.isAnObstacle(x, y)):
                newNode = Node(x, y, self.endI, self.endJ, newTheta)
                neighbours[newNode] = distance
                valid_actions[newNode] = [lin_vel, ang_vel]
        return neighbours, valid_actions

    def getNewCoordiantes(self, i, j, theta, UL, UR):
        t = 0
        r = 0.033
        L = 0.16
        dt = 0.01

        UL = 3.14 * (UL / 30)
        UR = 3.14 * (UR / 30)
        ang_vel = (r / L) * (UR - UL)
        lin_vel = 0.5 * r * (UL + UR)
        newI = i
        newJ = j
        newTheta = 3.14 * theta / 180
        D = 0

        while t < 1:
            t = t + dt
            Delta_Xn = 0.5 * r * (UL + UR) * math.cos(newTheta) * dt
            Delta_Yn = 0.5 * r * (UL + UR) * math.sin(newTheta) * dt
            newI += Delta_Xn
            newJ += Delta_Yn
            newTheta += (r / L) * (UR - UL) * dt
            D = D + math.sqrt(math.pow(Delta_Xn, 2) + math.pow(Delta_Yn, 2))
        newTheta = 180 * newTheta / 3.14

        if newTheta > 0:
            newTheta = newTheta % 360
        elif newTheta < 0:
            newTheta = (newTheta + 360) % 360

        newI = self.getRoundedNumber(newI)
        newJ = self.getRoundedNumber(newJ)

        return newI, newJ, newTheta, D, lin_vel, ang_vel


    def getRoundedNumber(self, i):
        i = 50 * i
        i = int(i)
        i = float(i) / 50.0
        return i

    def performAStar(self, start, end):
        """
        Description: Defining initial constants - Visited array, Rows, Cols, Target String.
        Input: Starting and ending node for the robot to browse.
        Output: Returns True or False to define if an optimal path can be found or not.
        """

        # Checking is start and end are in obstancle.
        if self.isAnObstacle(start.i, start.j) and self.isAnObstacle(end.i, end.j):
            rospy.loginfo("Starting and ending point are inside the obstacle! Check clearances!")
            return

        if self.isAnObstacle(start.i, start.j):
            rospy.loginfo("Starting point is inside the obstacle! Check clearances!")
            return

        if self.isAnObstacle(end.i, end.j):
            rospy.loginfo("Ending point is inside the obstacle! Check clearances!")
            return

        if self.isOutsideArena(start.i, start.j):
            rospy.loginfo("Starting point is outside the arena! Check clearances!")
            return

        if self.isOutsideArena(end.i, end.j):
            rospy.loginfo("Ending point is outside the arena! Check clearances!")
            return

        rospy.loginfo("Finding path...")
        priorityQueue = []
        visited_list = {}
        heapq.heappush(priorityQueue, (start.cost, start))
        while len(priorityQueue):
            currentNode = heapq.heappop(priorityQueue)
            currentNode = currentNode[1]
            if self.isInTargetArea(currentNode.i, currentNode.j):
                self.backTrack(currentNode)
                print("Found a path!")
                print("Distance Required to reach from start to end is:", currentNode.costToCome)
                return True

            if tuple([currentNode.i, currentNode.j]) in visited_list:
                continue
            visited_list[tuple([currentNode.i, currentNode.j])] = True

            currentDistance = currentNode.costToCome
            neighbours, valid_actions = self.getNeighbours(currentNode)
            currentNode.neighbours = neighbours
            currentNode.valid_actions = valid_actions
            for neighbourNode, newDistance in neighbours.items():
                neighbourNode.costToCome = currentDistance + newDistance
                neighbourNode.cost = neighbourNode.costToCome + neighbourNode.costToGo
                neighbourNode.parent = currentNode
                heapq.heappush(priorityQueue, (neighbourNode.cost, neighbourNode))
        print("Cannot find a path :(")
        return False

    def isInTargetArea(self, i, j):
        """
        Description: Checks if the currentnode is in target area to terminal the program
        Input: Current Node co-ordinates
        Output: Boolean
        """
        if (i - self.endI) ** 2 + (j - self.endJ) ** 2 - 1 <= 0:
            return True
        else:
            return False

    def backTrack(self, child):
        """
        Description: Backtracking from the finishing node to the start node.
        Input: Ending Node
        Output: A animation of the path generated.
        """
        while child != None:
            path.append(child)
            child = child.parent
        return True

    def isinStartingCircle(self, start, i, j):
        """
        Description: Checks if a point is in the starting circle from where the robot will start,
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        if (i - start.i) ** 2 + (j - start.j) ** 2 - 1 <= 0:
            return True
        else:
            return False

    def isInStartingSquare(self, start, i, j):
        """
        Description: Checks if a point is in the starting square from where the robot will start.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        if (start.i - 0.5 <= i <= start.i + 0.5) and (start.j - 0.5 <= j <= start.j + 0.5):
            return True
        else:
            return False

    def isInCircle1(self, x, y):
        """
        Description: Checks if a point is in the circle.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """
        r = 1 + self.CLEARANCE
        if (x - 2) ** 2 + (y - 2) ** 2 - r ** 2 >= 0:
            return False
        else:
            return True

    def isInCircle2(self, x, y):
        """
        Description: Checks if a point is in the circle.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """
        r = 1 + self.CLEARANCE
        if (x - 2) ** 2 + (y - 8) ** 2 - r ** 2 >= 0:
            return False
        else:
            return True

    def isInRectangle1(self, x, y):
        """
        Description: Checks if a point is in the rotated rectangle.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """
        circ1 = (x - 0.25) ** 2 + (y - 5.75) ** 2 <= self.CLEARANCE ** 2
        circ2 = (x - 1.75) ** 2 + (y - 5.75) ** 2 <= self.CLEARANCE ** 2
        circ3 = (x - 0.25) ** 2 + (y - 4.25) ** 2 <= self.CLEARANCE ** 2
        circ4 = (x - 1.75) ** 2 + (y - 4.25) ** 2 <= self.CLEARANCE ** 2
        side1 = x <= 1.75
        eside1 = x <= 1.75 + self.CLEARANCE
        side2 = y <= 5.75
        eside2 = y <= 5.75 + self.CLEARANCE
        side3 = x >= 0.25
        eside3 = x >= 0.25 - self.CLEARANCE
        side4 = y >= 4.25
        eside4 = y >= 4.25 - self.CLEARANCE
        rect1 = eside1 and side2 and eside3 and side4
        rect2 = side1 and eside2 and side3 and eside4

        if rect1 or rect2 or circ1 or circ2 or circ3 or circ4:
            return True
        else:
            return False

    def isInRectangle2(self, x, y):
        """
        Description: Checks if a point is in the rotated rectangle.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """
        circ1 = (x - 3.75) ** 2 + (y - 5.75) ** 2 <= self.CLEARANCE ** 2
        circ2 = (x - 6.25) ** 2 + (y - 5.75) ** 2 <= self.CLEARANCE ** 2
        circ3 = (x - 3.75) ** 2 + (y - 4.25) ** 2 <= self.CLEARANCE ** 2
        circ4 = (x - 6.25) ** 2 + (y - 4.25) ** 2 <= self.CLEARANCE ** 2
        side1 = x <= 6.25
        eside1 = x <= 6.25 + self.CLEARANCE
        side2 = y <= 5.75
        eside2 = y <= 5.75 + self.CLEARANCE
        side3 = x >= 3.75
        eside3 = x >= 3.75 - self.CLEARANCE
        side4 = y >= 4.25
        eside4 = y >= 4.25 - self.CLEARANCE
        rect1 = eside1 and side2 and eside3 and side4
        rect2 = side1 and eside2 and side3 and eside4

        if rect1 or rect2 or circ1 or circ2 or circ3 or circ4:
            return True
        else:
            return False

    def isInRectangle3(self, x, y):
        """
        Description: Checks if a point is in the rotated rectangle.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """
        circ1 = (x - 7.25) ** 2 + (y - 4) ** 2 <= self.CLEARANCE ** 2
        circ2 = (x - 8.75) ** 2 + (y - 4) ** 2 <= self.CLEARANCE ** 2
        circ3 = (x - 8.75) ** 2 + (y - 2) ** 2 <= self.CLEARANCE ** 2
        circ4 = (x - 7.25) ** 2 + (y - 2) ** 2 <= self.CLEARANCE ** 2
        side1 = x <= 8.75
        eside1 = x <= 8.75 + self.CLEARANCE
        side2 = y <= 4
        eside2 = y <= 4 + self.CLEARANCE
        side3 = x >= 7.25
        eside3 = x >= 7.25 - self.CLEARANCE
        side4 = y >= 2
        eside4 = y >= 2 - self.CLEARANCE
        rect1 = eside1 and side2 and eside3 and side4
        rect2 = side1 and eside2 and side3 and eside4

        if rect1 or rect2 or circ1 or circ2 or circ3 or circ4:
            return True
        else:
            return False

    def isAnObstacle(self, x, y):
        """
        Description: Checks if the point (x,y) is inside an obstacle or not.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        return self.isInCircle1(x, y) or self.isInCircle2(x, y) or self.isInRectangle1(x, y) or self.isInRectangle2(x, y) or self.isInRectangle3(x, y)

    def isOutsideArena(self, x, y):
        """
        Description: Checks if the point (x,y) is outside the arena or not.
        Input: Point with co-ordinates (x,y)
        Output: True or False
        """

        return True if x < self.CLEARANCE or y < self.CLEARANCE or x > 10 - self.CLEARANCE or y > 10 - self.CLEARANCE else False


def publisher(action):
    msg = Twist()
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.init_node('publisher', anonymous=True)
    if not rospy.is_shutdown():
        msg.linear.x = action[0]
        msg.angular.z = action[1]
        #rospy.loginfo(msg.linear.x)
        pub.publish(msg)
        rospy.sleep(1.0)
    return


if __name__ == '__main__':
    try:
        x1 = float(input("Enter the x coordiante of the starting point: "))
        y1 = float(input("Enter the y coordiante of the starting point: "))
        thetaStart = int(input("Enter the start theta: "))
        print("#############################################")

        x2 = float(input("Enter the x coordiante of the ending point: "))
        y2 = float(input("Enter the y coordiante of the ending point: "))
        print("#############################################")

        RPM1 = float(input("Enter one RPM of the robot:  "))
        RPM2 = float(input("Enter another RPM of the robot:  "))
        RADIUS = float(input("Enter the radius of the robot:  "))
        CLEARANCE = float(input("Enter the clearance:  "))

        end = Node(x2, y2, x2, y2, 0)
        start = Node(x1, y1, x2, y2, thetaStart)
        start.costToCome = 0
        robot = Graph(start, end, RPM1, RPM2, RADIUS, CLEARANCE)
        path = []

        if robot.performAStar(start, end):
            path.reverse()
            trail = 0
            while trail<5:
                publisher([0.0, 0.0])
                trail += 1
            for index in range(len(path) - 1):
                node = path[index]
                print((node.i,node.j))
                action = node.valid_actions[path[index + 1]]
                publisher(action)
            trail = 0
            while trail<5:
                publisher([0.0, 0.0])
                trail += 1
    except rospy.ROSInterruptException:
        pass

