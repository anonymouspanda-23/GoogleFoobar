import copy
import time


class Node:
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def search(maze):
    open_list = list()  # list to store nodes to be expanded
    closed_list = list()  # list to store nodes which had been expanded

    n_rows = len(maze)
    n_cols = len(maze[0])

    start = [0, 0]
    end = [n_rows - 1, n_cols - 1]

    remaining_iterations = (len(maze) // 2) ** 10

    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0

    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0

    open_list.append(start_node)

    moves = [
        [0, -1],  # move left
        [0, 1],   # move right
        [-1, 0],  # move up
        [1, 0]    # move down
    ]

    while open_list:
        current_node = open_list[0]
        current_index = 0

        remaining_iterations -= 1

        for index, new_node in enumerate(open_list):
            if new_node.f < current_node.f:
                current_node = new_node
                current_index = index

        if remaining_iterations == 0:
            break  # return current path or 0 and None

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = list()
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent

            return path[::-1], len(path[::-1])

        children = list()

        for move in moves:
            # check if move is valid
            new_position = (current_node.position[0] + move[0], current_node.position[1] + move[1])
            # print(f"X Pos: {new_position[1]}, Y Pos: {new_position[0]}.")

            if not 0 <= new_position[0] <= n_rows - 1 or not 0 <= new_position[1] <= n_cols - 1:
                continue

            if maze[new_position[0]][new_position[1]] != 0:
                continue

            # if move valid in maze and  not wall, create node
            child_node = Node(current_node, new_position)

            # add to children
            children.append(child_node)

        for child_node in children:
            if child_node in closed_list:
                continue

            child_node.g = current_node.g + 1
            child_node.h = ((child_node.position[0] - end_node.position[0]) ** 2) + ((child_node.position[1] - end_node.position[1]) ** 2)
            child_node.f = child_node.g + child_node.h

            for node in open_list:
                if child_node == node and child_node.g > node.g:
                    continue

            open_list.append(child_node)


def destroy_wall(maze):
    path, path_length = search(maze)
    new_map = copy.deepcopy(maze)
    # print(f"New Map: {new_map}\n")

    for y, row in enumerate(new_map):
        for x, col in enumerate(row):
            if new_map[y][x] == 1:
                new_map[y][x] = 0
                # print(f"X = {x}, Y = {y}, New Map:      {new_map}")
                updated_path, updated_path_length = search(new_map)
                new_map[y][x] = 1
                # print(f"X = {x}, Y = {y}, Reverted Map: {new_map}\n")

                if updated_path_length < path_length:
                    path_length = updated_path_length
                    path = updated_path

    return path, path_length


def test_algorithm(maze, start, end):
    print(f"Start Point: {tuple(start)}.")
    print(f"End Point: {tuple(end)}.")
    print(f"Maze: {maze}")

    start_time = time.time()
    resultant_path, path_length = destroy_wall(maze)
    end_time = time.time()

    print(f"Time taken to execute: {end_time - start_time}s")

    print(f"Resulting path coordinates: {resultant_path}")

    print(f"Cost: {path_length}")

    print(f"Type: {type(path_length)}")

    for y, row in enumerate(maze):
        print("")

        for x, column in enumerate(row):
            if (y, x) == tuple(start):
                print('SS', end="")
            elif (y, x) == tuple(end):
                print('EE', end="")
            elif (y, x) in resultant_path:
                print('MV', end="")
            elif maze[y][x] == 1:
                print(u"\u2588" * 2, end="")
            else:
                print("[]", end="")

    print("\n")


if __name__ == '__main__':

    test_maze_2 = [
        [0, 1, 1, 0],
        [0, 0, 0, 1],
        [1, 1, 0, 0],
        [1, 1, 1, 0]
    ]

    start_point = [0, 0]
    end_point = [len(test_maze_2) - 1, len(test_maze_2[0]) - 1]

    test_algorithm(test_maze_2, start_point, end_point)

    test_maze_3 = [
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0]
    ]

    start_point = [0, 0]
    end_point = [len(test_maze_3) - 1, len(test_maze_3[0]) - 1]

    test_algorithm(test_maze_3, start_point, end_point)

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

    start_point = [0, 0]
    end_point = [len(test_maze_4) - 1, len(test_maze_4[0]) - 1]

    test_algorithm(test_maze_4, start_point, end_point)

    test_maze_5 = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]

    start_point = [0, 0]
    end_point = [len(test_maze_5) - 1, len(test_maze_5[0]) - 1]

    test_algorithm(test_maze_5, start_point, end_point)
