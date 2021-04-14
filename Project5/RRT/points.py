x1 = 10
y1 = 10
x2 = 10
y2 = 20

for x in range(min(x1,x2), max(x1,x2)+1):
    for y in range(min(y1,y2), max(y1,y2)+1):
        if y == int(((x - x1) * (y1 - y2))/(x1-x2) + y1):
            print(x,y)
