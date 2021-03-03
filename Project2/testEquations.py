import math
def isInCircle(x,y):
    if (x - 90) **2 + (y-70)**2 - 1225 > 0:
        return False
    else:
        return True

def isInRectangle(x,y):
    if (y + 1.42*x - 176.55) > 0  and (y - 0.7*x - 74.39) > 0 and (y - 0.7*x - 98.81) < 0 and (y + 1.42*x - 438.06) < 0:
        return True
    else:
        return False

def isInBrokenRectangle(x,y):
    if (x >= 200 and x <= 210 and y <= 280 and y >=230 ) or (x>= 210 and x <= 230 and y >=270 and y <= 280) or (y >= 230 and y <= 240 and x >= 210 and x <= 230):
        return True
    else:
        return False

def isInEllipse(x,y):

    horizontalRadius = a= 60
    verticalRadius = b=30
    centerX = h=246
    centerY = k = 145
    if ((math.pow((x - h), 2) / math.pow(a, 2)) + (math.pow((y - k), 2) / math.pow(b, 2))) < 1:
        return True
    else:
        return False
def isInPolygon(x,y):

    print(x,y)
    # if (y + 0.99*x - 389.3) > 0  and (y - x + 181.62) < 0 and (y - 1.13*x + 260.75) < 0 and (y + 0.29*x - 239.89) < 0 and (y + 250*x -95054) < 0 and (y - x + 266) > 0:
    if ((y - 1.01*x + 181.62) < 0 and (y + 0.29*x - 239.89) < 0 and (y + 249.20*x -95054.25) < 0 and (y - x + 266) > 0 and (y + 0.99*x - 389.3) > 0 ) or ( (y - 1.13*x + 260.75) < 0  and (y + 249.20*x - 95054.25) < 0 and (y + .29*x - 240.60) > 0):
        return True
    else:
        return False


def isAnObstacle(x,y):
    return True if (isInPolygon(x,y) and isInCircle(x, y) and isInRectangle(x, y) and isInBrokenRectangle(x, y) and isInEllipse(x, y)) else False

x = 385
y = 145

#print(isInCircle(x, y))
# print(isInRectangle(x, y))
# print(isInBrokenRectangle(x, y))
# print(isInEllipse(x, y))
print(isInPolygon(x,y))