import time

"""
Sample Prison Layout:

| 11 17 24 32 41
| 7  12 18 25 33
| 4  8  13 19 26
| 2  5  9  14 20
| 1  3  6  10 15

Note: Prison is in triangle shape

"""


def solution(x, y):
    # Your code here
    def formula_x(y_coords):
        return 2 * y_coords - 1

    def formula_y(y_coords):
        return (y_coords * (y_coords - 1)) / 2

    prisoner_id = (((x ** 2) + (formula_x(y) * x)) / 2) + formula_y(y - 1)
    prisoner_id = int(prisoner_id)

    return str(prisoner_id)


if __name__ == '__main__':
    start_time = time.time()
    solution(3, 2)
    solution(5, 10)
    solution(2, 4)
    print(solution(13975013750179, 310470147037150))
    end_time = time.time()

    print(f"Time taken: {end_time - start_time}s.")
