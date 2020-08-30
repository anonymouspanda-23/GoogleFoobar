import unittest


class Node:
    def __init__(self, parent, position):
        self.g = 0
        self.h = 0
        self.f = 0

        self.parent = parent
        self.position = position
        self.wall_broken = False

    def __eq__(self, other):
        return self.position == other.position and self.wall_broken == other.wall_broken


def return_path(solvable, current_node):
    path = []
    current = current_node

    while current is not None:
        path.append(current.position)
        current = current.parent

    path = path[::-1]

    return solvable, len(path)


def search(maze, start_pos=tuple(), end_pos=tuple()):
    """
    search function attempts to look for a path, returns solvable as False if there is no possible path to end state
    :param maze:
    :param start_pos:
    :param end_pos:
    :return:
    """

    # calculate the number of rows and columns in the maze
    n_rows = len(maze)
    n_cols = len(maze[n_rows - 1])

    # calculating start and end if not set by user
    if not start_pos:
        start_pos = (0, 0)

    if not end_pos:
        end_pos = (n_rows - 1, n_cols - 1)

    # define the maximum number of iterations before exiting
    max_iter = (n_rows * n_cols) ** 2  # maybe max_iter can be reduced to (n_rows ** n_cols)
    current_iter = 0

    # initialize start and end nodes
    start_node = Node(None, start_pos)
    end_node = Node(None, end_pos)

    # define open and closed lists
    open_list = []  # list of nodes to expand
    closed_list = []  # list of nodes expanded

    # add current node to open_list
    open_list.append(start_node)

    # define legal moves
    valid_moves = [
        (-1, 0),  # move up
        (1, 0),  # move down
        (0, -1),  # move left
        (0, 1)   # move right
    ]

    # initialise current_node
    current_node = None

    # while nodes available in open_list to expand
    while open_list:
        # get 1 node from list
        current_node = open_list[0]

        # check if current iteration has reached iteration limit
        if current_iter >= max_iter:
            return return_path(False, current_node)

        # increment current iteration
        current_iter += 1

        # use current node to get optimal node
        for node in open_list:
            if current_node.f > node.f:
                current_node = node

        # remove current node from open_list and add it to closed_list
        open_list.remove(current_node)
        closed_list.append(current_node)

        if current_node.position == end_node.position:
            return return_path(True, current_node)

        # create list to store new valid nodes expanded from current node
        children = []

        # loop through valid_moves and add children nodes in valid positions to children list for expanding
        for move in valid_moves:  # check section
            # create child position
            child_position = (current_node.position[0] + move[0], current_node.position[1] + move[1])

            # create child_node
            child_node = Node(current_node, child_position)
            child_node.wall_broken = current_node.wall_broken

            # check if child position is not in maze
            if not 0 <= child_position[0] < n_rows or not 0 <= child_position[1] < n_cols:
                continue

            # check if child position is not in wall
            if maze[child_position[0]][child_position[1]] != 0:
                if current_node.wall_broken:
                    continue
                else:
                    child_node.wall_broken = True

            # add child_node to list of child nodes
            if child_node not in closed_list:
                children.append(child_node)

        for child_node in children:  # section clear
            # calculate child_node g, h and f values
            child_node.g = current_node.g + 1
            child_node.h = (end_node.position[0] - child_node.position[0]) + (end_node.position[1] - child_node.position[1])
            child_node.f = child_node.g + child_node.h

            # adding child_node to open_list (version 2)
            for node in open_list:
                if child_node == node and child_node.g < node.g:
                    index = open_list.index(node)
                    open_list[index] = child_node

            if child_node not in open_list:
                open_list.append(child_node)

    return return_path(False, current_node)


class Test(unittest.TestCase):
    def test_one(self):
        self.assertEqual(search([
            [0, 1, 1, 0],
            [0, 0, 0, 1],
            [1, 1, 0, 0],
            [1, 1, 1, 0]
        ]), (True, 7))

    def test_two(self):
        self.assertEqual(search([
            [0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0]
        ]), (True, 11))

    def test_three(self):
        self.assertEqual(search([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]), (True, 31))

    def test_four(self):
        self.assertEqual(search([
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
        ]), (True, 66))

    def test_five(self):
        self.assertEqual(search([
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1],
            [0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0],
            [1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
            [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        ]), (True, 47))

    def test_six(self):
        self.assertEqual(search([
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 0, 0, 0]
        ]), (False, 6))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    results = unittest.TextTestRunner(verbosity=2).run(suite)
