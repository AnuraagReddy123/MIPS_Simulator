import sys
class Hello:
    def __init__(self):
        self.name = "anuraag"
        self.surname = "reddy"


class People:
    def __init__(self):
        self.number = 5
        self.person = []
        for i in range(5):
            self.person.append(Hello())
    
    def wave(self):
        print(self.person[0].name)

a = People()
a.wave()
print(sys.maxsize)


for i in range(5):
    b = 5

c = '101'
d = '123'
e = c + d + '0'*5
print(e)
print(b)