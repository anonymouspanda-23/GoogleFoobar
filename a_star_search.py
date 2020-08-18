import time


class Node:
    def __init__(self, parent, position):
        self.g = 0
        self.h = 0
        self.f = 0

        self.parent = parent
        self.position = position

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
        end_pos = (len(maze) - 1, len(maze[n_rows - 1]) - 1)

    # print start and end coordinates to ensure calculations are working
    print(f"Start location: {start_pos}")
    print(f"End location: {end_pos}")

    # define the maximum number of iterations before exiting
    max_iter = (n_rows * n_cols) ** 2  # maybe max_iter can be reduced to (n_rows ** n_cols)
    current_iter = 0

    # declare the maximum allowable length if not break (number of tiles)
    max_path_len = n_cols * n_rows

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

    # while nodes available in open_list to expand
    while open_list:
        print(f"Open List: {[node.position for node in open_list]}")
        print(f"Closed List: {[node.position for node in closed_list]}")
        input("Press enter to continue.")
        
        # get 1 node from list
        # todo: add check that node is not in closed_list
        current_node = open_list[0]
        current_index = 0

        # check if current iteration has reached iteration limit
        if current_iter >= max_iter or max_path_len <= 0:
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

        # remove all nodes in open_list with f length greater than max_path_len
        to_remove = []
        
        for node in open_list:
            if node.f > max_path_len:
                to_remove.append(node)

        for node in to_remove:
            open_list.remove(node)
            closed_list.append(node)

        # update max_path_len
        # max_path_len -= 1

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

            # check if child_node exists in open_list and if it does, check if it is more efficient going this way
            if child_node in open_list:
                for index, node in enumerate(open_list):
                    if child_node == node and child_node.g < node.g:
                        open_list.pop(index)
            
            open_list.append(child_node)

    print("No more possible paths found. Exiting...")
    return return_path(False, current_node)


if __name__ == '__main__':

    main_start_time = time.time()

    test_maze_1 = [
        [0, 1, 1, 0],
        [0, 0, 0, 1],
        [1, 1, 0, 0],
        [1, 1, 1, 0]
    ]

    maze_1_start = time.time()
    solvable, path = a_star_search(test_maze_1)
    maze_1_end = time.time()
    print(f"Time to solve maze 1: {maze_1_end - maze_1_start}s")
    
    if solvable:
        print(f"Maze 1: {path}")
    else:
        print("Maze 1 is unsolvable")
        print(f"Partial path: {path}")

    print("")

    test_maze_2 = [
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0]
    ]

    maze_2_start = time.time()
    solvable, path = a_star_search(test_maze_2)
    maze_2_end = time.time()
    print(f"Time to solve maze 2: {maze_2_end - maze_2_start}s")
    
    if solvable:
        print(f"Maze 2: {path}")
    else:
        print("Maze 2 is unsolvable")
        print(f"Partial path: {path}")

    print("")

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

    maze_3_start = time.time()
    solvable, path = a_star_search(test_maze_3)
    maze_3_end = time.time()
    print(f"Time to solve maze 3: {maze_3_end - maze_3_start}s")
    
    if solvable:
        print(f"Maze 3: {path}")
    else:
        print("Maze 3 is unsolvable")
        print(f"Partial path: {path}")

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

    maze_4_start = time.time()
    solvable, path = a_star_search(test_maze_4)
    maze_4_end = time.time()
    print(f"Time to solve maze 4: {maze_4_end - maze_4_start}s")
    
    if solvable:
        print(f"Maze 4: {path}")
    else:
        print("Maze 4 is unsolvable")
        print(f"Partial path: {path}")

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

    maze_5_start = time.time()
    solvable, path = a_star_search(test_maze_5)
    maze_5_end = time.time()
    print(f"Time to solve maze 5: {maze_5_end - maze_5_start}s")
    
    if solvable:
        print(f"Maze 5: {path}")
    else:
        print("Maze 5 is unsolvable")
        print(f"Partial path: {path}")

    main_end_time = time.time()

    print(f"Total runtime: {main_end_time - main_start_time}s")

