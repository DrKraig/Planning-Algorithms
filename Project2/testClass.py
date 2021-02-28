class CAR:
    def __init__(self, name):
        self.name = name
    

a = CAR("A")
b = CAR("A")
print(a)
print(b)
print(a==b)