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