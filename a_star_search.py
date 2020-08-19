import copy
import time


class Node:
    def __init__(self, parent, position):  # todo: add attribute of wall_broken
        self.g = 0
        self.h = 0
        self.f = 0

        self.parent = parent
        self.position = position
        # self.wall_broken = wall_broken

    def __eq__(self, other):
        return self.position == other.position


def return_path(solvable, current_node):
    path = []
    current = current_node

    while current is not None:
        path.append(current.position)
        current = current.parent

    path = path[::-1]

    return [solvable, path]


def a_star_search(maze, start_pos=tuple(), end_pos=tuple()):
    """
    a_star_search function attempts to look for a path, returns unsolvable as True if there is no possible path to end state
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
    start_node.g = start_node.h = start_node.f = 0

    end_node = Node(None, end_pos)
    end_node.g = end_node.h = end_node.f = 0

    # define open and closed lists
    open_list = []  # list of nodes to expand
    closed_list = []  # list of nodes expanded

    # add current node to open_list
    open_list.append(start_node)

    # define legal moves
    valid_moves = [
        [-1, 0],  # move up
        [1, 0],  # move down
        [0, -1],  # move left
        [0, 1]   # move right
    ]

    # initialise current_node
    current_node = None

    # while nodes available in open_list to expand
    while open_list:
        
        # get 1 node from list
        current_node = open_list[0]
        current_index = 0

        # check if current iteration has reached iteration limit
        if current_iter >= max_iter:
            return return_path(False, current_node)

        # increment current iteration
        current_iter += 1

        # use current node to get optimal node
        for index, node in enumerate(open_list):
            if node.f < current_node.f:
                current_node = node
                current_index = index

        if current_node == end_node:
            return return_path(True, current_node)

        # remove current node from open_list and add it to closed_list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # create list to store new valid nodes expanded from current node
        children = []

        # loop through valid_moves and add children nodes in valid positions to children list for expanding
        for move in valid_moves:

            # create child position
            child_position = (current_node.position[0] + move[0], current_node.position[1] + move[1])

            # check if child position is in maze
            if not 0 <= child_position[0] <= n_rows - 1 or not 0 <= child_position[1] <= n_cols - 1:
                continue

            # check if child position is not in wall
            if maze[child_position[0]][child_position[1]] != 0:
                continue

            # create child_node
            child_node = Node(current_node, child_position)

            # add child_node to list of child nodes
            children.append(child_node)

        for child_node in children:

            # check if child_node is in closed_list
            if child_node in closed_list:
                continue

            # calculate child_node g, h and f values
            child_node.g = current_node.g + 1
            child_node.h = abs((end_node.position[0] - child_node.position[0]) + (end_node.position[1] - child_node.position[1]))
            child_node.f = child_node.g + child_node.h

            for node in open_list:
                if child_node == node and child_node.g < node.g:
                    node.g = child_node.g
                    node.h = child_node.h
                    node.f = child_node.f

                    node.parent = child_node.parent

            if child_node not in open_list:
                open_list.append(child_node)

    return return_path(False, current_node)


def destroy_wall(maze):  # todo: try to optimize -> https://stackoverflow.com/questions/2489672/removing-the-obstacle-that-yields-the-best-path-from-a-map-after-a-traversal
    solvable, resultant_path = a_star_search(maze)
    maze_copy = copy.deepcopy(maze)
    path_length = len(resultant_path)

    for y, row in enumerate(maze_copy):
        for x, col in enumerate(row):

            if maze_copy[y][x] == 1:
                maze_copy[y][x] = 0
                new_solvable, new_resultant_path = a_star_search(maze_copy)
                new_path_length = len(new_resultant_path)
                maze_copy[y][x] = 1

                if solvable and new_solvable and new_path_length < path_length:
                    path_length = new_path_length
                    resultant_path = new_resultant_path

                elif not solvable and new_solvable:
                    path_length = new_path_length
                    resultant_path = new_resultant_path
                    solvable = new_solvable

                elif solvable and not new_solvable:
                    continue

                else:  # if maze is unsolvable with or without removing wall
                    continue

    return solvable, resultant_path


def test_algorithm(maze):
    n_rows = len(maze)
    n_cols = len(maze[n_rows - 1])

    start_pos = (0, 0)
    end_pos = (n_rows - 1, n_cols - 1)

    print(f"Start Point: {tuple(start_pos)}.")
    print(f"End Point: {tuple(end_pos)}.")

    start_time = time.time()
    # solvable, resultant_path = a_star_search(maze)  # function to search without removing a wall
    solvable, resultant_path = destroy_wall(maze)  # function to search with ability to remove 1 wall
    end_time = time.time()

    print(f"Time taken to execute: {end_time - start_time}s")

    print(f"Resulting path coordinates: {resultant_path}")

    print(f"Cost: {len(resultant_path)}")

    print("\n")

    print("Solved maze:") if solvable else print("Partially solved maze:")

    for y, row in enumerate(maze):
        print("")

        for x, column in enumerate(row):
            if (y, x) == tuple(start_pos):
                print('SS', end="")
            elif (y, x) == tuple(end_pos):
                print('EE', end="")
            elif (y, x) in resultant_path:
                print('MV', end="")
            elif maze[y][x] == 1:
                print(u"\u2588" * 2, end="")
            else:
                print("[]", end="")

    print("\n")


if __name__ == '__main__':

    main_start_time = time.time()

    test_maze_1 = [
        [0, 1, 1, 0],
        [0, 0, 0, 1],
        [1, 1, 0, 0],
        [1, 1, 1, 0]
    ]

    test_algorithm(test_maze_1)

    test_maze_2 = [
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0]
    ]

    test_algorithm(test_maze_2)

    test_maze_3 = [
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
    ]

    test_algorithm(test_maze_3)

    print("")

    test_maze_4 = [
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
    ]

    test_algorithm(test_maze_4)

    print("")

    test_maze_5 = [
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
    ]

    test_algorithm(test_maze_5)

    main_end_time = time.time()

    print(f"Total runtime: {main_end_time - main_start_time}s")
