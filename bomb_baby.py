import unittest


def solution(x, y):
    x = int(x)
    y = int(y)

    count = 0

    while x > 1 and y > 1:
        if x > y:
            x = x - y
        if y > x:
            y = y - x

        count += 1

    if x == 1 and y == 1:
        return count
    else:
        return "impossible"


class Test(unittest.TestCase):
    def test(self):
        self.assertEqual(solution('4', '7'), 4)
        self.assertEqual(solution('2', '1'), 1)


if __name__ == '__main__':
    test = Test()
    test.test()
