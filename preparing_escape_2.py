class Node:
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0


    def __eq__(self, other):
        return self.position == other.position


def search(maze, cost, start, end):
    open_list = list()  # list to store nodes to be expanded
    closed_list = list()  # list to store nodes which had been expanded

    n_rows = len(maze)
    n_cols = len(maze[0])

    # todo: add check to prevent infinite loop

    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0

    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0

    open_list.append(start_node)

    moves = [
        [0, 1],   # move up
        [0, -1],  # move down
        [-1, 0],  # move left
        [1, 0]    # move right
    ]

    while open_list:
        current_node = open_list[0]
        current_index = 0

        for index, new_node in enumerate(open_list):
            if new_node.f < current_node.f:
                current_node = new_node
                current_index = index

        open_list.pop(index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = list()
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent

            return path[::-1]

        children = list()

        for move in moves:
            # check if move is valid
            new_position = (current_node.position[0] + move[0], current_node.position[1] + move[1])

            if maze[new_position[0]][new_position[1]] != 0:
                continue

            if not 0 < new_position[0] <= n_rows or not 0 < new_position[1] <= n_cols:
                continue

            # if move valid (in maze and  not wall, create node
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
                if child_node == node and child_node.g < node.g:
                    node.g = child_node.g
                    node.h = child_node.h
                    node.f = child_node.f

                    node.parent = child_node.parent

            if not child_node in open_list:
                open_list.append(child_node)


if __name__ == '__main__':
    test_maze = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]

    start_point = [3, 1]
    end_point = [4, 5]

    resultant_path = search(test_maze, 1, start_point, end_point)

    print(resultant_path)
