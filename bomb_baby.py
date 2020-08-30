import unittest


def solution(x, y):
    x = int(x)
    y = int(y)

    count = 0

    while x > 0 and y > 0:
        if x > y:
            add = x / y - 1 if x / y > 1 else 1
            x = x - y * add
        elif y > x:
            add = y / x - 1 if y / x > 1 else 1
            y = y - x * add
        else:
            break

        count += add

    if x == 1 and y == 1:
        return str(count)
    else:
        return "impossible"


class Test(unittest.TestCase):
    def test_one(self):
        self.assertEqual(solution('4', '7'), '4')

    def test_two(self):
        self.assertEqual(solution('2', '1'), '1')

    def test_three(self):
        self.assertEqual(solution('2', '4'), "impossible")

    def test_four(self):
        self.assertEqual(solution('5432123456788', '5432123456789'), '5432123456788')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
