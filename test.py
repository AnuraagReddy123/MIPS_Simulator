def test(a):
    a[0] = 10

def test_1(b):
    global a
    a = 5

if __name__ == "__main__":
    a = 6
    b = 5
    test_1(b)
    print(a)