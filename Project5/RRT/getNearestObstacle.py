
import math
import numpy as np
def getEuclidianDistance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def getAllPointsOnObstacle():

    points = []
    CLEARANCE = 0.1

    #Circle 1
    r = 1 + CLEARANCE
    for theta in np.arange(0,360):
        thetaInRadians = (math.pi * theta) /180
        x = 2 + r*math.cos(thetaInRadians)
        y = 2 + r*math.sin(thetaInRadians)
        points.append([x,y])

    #Circle 2
    r = 1 + CLEARANCE
    for theta in np.arange(0,360):
        thetaInRadians = (math.pi * theta) /180
        x = 2 + r*math.cos(thetaInRadians)
        y = 8 + r*math.sin(thetaInRadians)
        points.append([x,y])

    # #Rectangle 1
    r = CLEARANCE
    for theta in np.arange(0,360):
        thetaInRadians = (math.pi * theta) /180
        x = 0.25 + r*math.cos(thetaInRadians)
        y = 5.75 + r*math.sin(thetaInRadians)
        points.append([x,y])
    for theta in np.arange(0,360):
        thetaInRadians = (math.pi * theta) /180
        x = 1.75 + r*math.cos(thetaInRadians)
        y = 5.75 + r*math.sin(thetaInRadians)
        points.append([x,y])
    for theta in np.arange(0,360):
        thetaInRadians = (math.pi * theta) /180
        x = 0.25 + r*math.cos(thetaInRadians)
        y = 4.25 + r*math.sin(thetaInRadians)
        points.append([x,y])
    for theta in np.arange(0,360):
        thetaInRadians = (math.pi * theta) /180
        x = 1.75 + r*math.cos(thetaInRadians)
        y = 4.25 + r*math.sin(thetaInRadians)
        points.append([x,y])
    for x in np.arange(0.25 - CLEARANCE, 1.75 + CLEARANCE, 0.1):
        points.append([x,5.75]) 
    for x in np.arange(0.25 - CLEARANCE, 1.75 + CLEARANCE, 0.1):
        points.append([x,4.25])
    for y in np.arange(4.25 - CLEARANCE, 5.75 + CLEARANCE, 0.1):
        points.append([0.25,y])
    for y in np.arange(4.25- CLEARANCE, 5.75 + CLEARANCE, 0.1):
        points.append([1.75,y])

    
    #Rectangle 2
    r = CLEARANCE
    for theta in np.arange(0,360):
        thetaInRadians = (math.pi * theta) /180
        x = 3.75 + r*math.cos(thetaInRadians)
        y = 5.75 + r*math.sin(thetaInRadians)
        points.append([x,y])
    for theta in np.arange(0,360):
        thetaInRadians = (math.pi * theta) /180
        x = 6.25 + r*math.cos(thetaInRadians)
        y = 5.75 + r*math.sin(thetaInRadians)
        points.append([x,y])
    for theta in np.arange(0,360):
        thetaInRadians = (math.pi * theta) /180
        x = 3.75 + r*math.cos(thetaInRadians)
        y = 4.25 + r*math.sin(thetaInRadians)
        points.append([x,y])
    for theta in np.arange(0,360):
        thetaInRadians = (math.pi * theta) /180
        x = 6.25 + r*math.cos(thetaInRadians)
        y = 4.25 + r*math.sin(thetaInRadians)
        points.append([x,y])
    for x in np.arange(3.75 - - CLEARANCE, 6.25 + CLEARANCE, 0.1):
        points.append([x,5.75])
    for x in np.arange(3.75 - CLEARANCE, 6.25 + CLEARANCE, 0.1):
        points.append([x,3.75])
    for y in np.arange(4.25 - CLEARANCE, 5.75 + CLEARANCE, 0.1):
        points.append([3.75,y])
    for y in np.arange(4.25 - CLEARANCE, 5.75 + CLEARANCE, 0.1):
        points.append([6.25,y])

    
    #Rectangle 3
    r = CLEARANCE
    for theta in np.arange(0,360):
        thetaInRadians = (math.pi * theta) /180
        x = 7.25 + r*math.cos(thetaInRadians)
        y = 4 + r*math.sin(thetaInRadians)
        points.append([x,y])
    for theta in np.arange(0,360):
        thetaInRadians = (math.pi * theta) /180
        x = 8.75 + r*math.cos(thetaInRadians)
        y = 4 + r*math.sin(thetaInRadians)
        points.append([x,y])
    for theta in np.arange(0,360):
        thetaInRadians = (math.pi * theta) /180
        x = 8.75 + r*math.cos(thetaInRadians)
        y = 2 + r*math.sin(thetaInRadians)
        points.append([x,y])
    for theta in np.arange(0,360):
        thetaInRadians = (math.pi * theta) /180
        x = 7.25 + r*math.cos(thetaInRadians)
        y = 2 + r*math.sin(thetaInRadians)
        points.append([x,y])
    for x in np.arange(7.25 - CLEARANCE, 8.75 + CLEARANCE, 0.1):
        points.append([x,2])
    for x in np.arange(7.25 - CLEARANCE, 8.75 + CLEARANCE, 0.1):
        points.append([x,2])
    for y in np.arange(2 - CLEARANCE, 4 + CLEARANCE, 0.1):
        points.append([8.75,y])
    for y in np.arange(2 - CLEARANCE, 4+ CLEARANCE, 0.1):
        points.append([7.25, y])

    return points

def getNearestObstacle(x, y):
    pointsOnObstacle = getAllPointsOnObstacle()
    print(pointsOnObstacle)
    minDistance = float("inf")
    minPoint = None
    for point in pointsOnObstacle:
        distance = getEuclidianDistance(point[0], point[1], 1,1)
        if minDistance > distance:
            minDistance = distance
            minPoint = point
    return minDistance

print(getNearestObstacle(10,10))