import unittest


def solution(x, y):
    x = int(x)
    y = int(y)

    count = 0

    while x > 0 and y > 0:
        count += 1
        if x == 1 and y == 1:
            break
        
        if x > y:
            x = x - y
        if y > x:
            y = y - x
        
        print("X: " + str(x))
        print("Y: " + str(y))

    print("Count: " + str(count))

    if x == 1 and y == 1:
        return count
    else:
        return "impossible"


class Test(unittest.TestCase):
    def test_one(self):
        self.assertEqual(solution('4', '7'), 4)

    def test_two(self):
        self.assertEqual(solution('2', '1'), 1)


if __name__ == '__main__':
    # suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    # unittest.TextTestRunner(verbosity=2).run(suite)
    print(solution('4', '7'))
    print(solution('2', '1'))
