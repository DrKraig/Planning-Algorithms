import math
def getEuclidianDistance():
    parentX = 10
    parentY = 10
    currentX = 20
    currentY = 20   
    return math.sqrt((parentX - currentX) ** 2 + (parentY - currentY) ** 2)
print(getEuclidianDistance())