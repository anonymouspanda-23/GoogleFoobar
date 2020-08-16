"""
Sample Prison Layout:

| 11 17 24 32 41
| 7  12 18 25 33
| 4  8  13 19 26
| 2  5  9  14 20
| 1  3  6  10 15

"""

def formula_x(y_coords):
    return 2 * y_coords - 1


def formula_y(y_coords):
    return (y_coords * (y_coords - 1)) / 2


def cell_id(coordinates):
    x, y = coordinates
    id = (((x ** 2) + (formula_x(y) * x)) / 2) + formula_y(y - 1)

    print(f"ID of prisoner at {x}, {y} is {id}.")
    # print(f"X number is {formula_x(y)}.")
    # print(f"Added number is {formula_y(y - 1)}.")
    # print("\n")


if __name__ == '__main__':
    cell_id((1, 1))
    cell_id((2, 1))
    cell_id((2, 4))
    cell_id((5, 5))
