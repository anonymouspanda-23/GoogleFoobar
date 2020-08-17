"""

Sample Maze:

0 - Clear path
1 - Wall

[[0, 1, 1, 0],
 [0, 0, 0, 1],
 [1, 1, 0, 0],
 [1, 1, 1, 0]]

Start Index: 0, 0
End Index: len(maze) - 1, len(maze[0]) - 1
"""


class Node:
    """
    A node class for A* pathfinding
    Parent refers to the parent of the current node
    Position refers to the current position of the node in the maze
    g is the cost from the start to the current node
    h is the heuristic based estimated cost from the current node to the end node
    f is the total cost of the current node i.e. f = g + h
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


# function returns the optimal path
def return_path(current_node, maze):
    path = []
    n_rows, n_columns = len(maze), len(maze[0])
    # initialize maze with -1 in every accessible position
    result = [[-1 for i in range(n_columns)] for j in range(n_rows)]
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    # return reversed path as we need to show from start to end
    path = path[::-1]
    start_value = 0
    # update the path of start to end found by A* search with every step incremented by 1
    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value += 1
    return result


def search(maze, cost, start, end):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param cost:
    :param start:
    :param end:
    :return:
    """

    # create start and end node with initialized values for g, h and f
    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0

    # initialize both yet_to_visit and visited list
    # in this list, we put all nodes that have not yet been visited for exploration
    # from here, we will find the lowest cost node to expand to next
    yet_to_visit_list = []
    # in this list, we put all nodes that have already been visited so we don't visit them again
    visited_list = []
    # add start node
    yet_to_visit_list.append(start_node)

    # set a stop condition to prevent an infinite loop or to stop execution after a reasonable number of steps
    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 10

    # define allowed movements
    moves = [
        [-1, 0],  # Move up
        [0, -1],  # Move left
        [1, 0],   # Move down
        [0, 1]    # Move right
    ]

    # find the number of rows and columns in the maze
    n_rows, n_columns = len(maze), len(maze[0])

    # loop until end point is reached
    while len(yet_to_visit_list) > 0:
        # every time a node is referred to from yet_to_visit list, increment number of operations
        outer_iterations += 1

        # get the current node
        current_node = yet_to_visit_list[0]
        current_index = 0
        for index, item in enumerate(yet_to_visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # if we hit this point, return path as computation cost is too high
        if outer_iterations > max_iterations:
            return return_path(current_node, maze)

        # pop current node from yet_to_visit list, add to visited list
        yet_to_visit_list.pop(current_index)
        visited_list.append(current_node)

        # test if goal is reached, if yes, return path
        if current_node == end_node:
            return return_path(current_node, maze)

        # generate children from all adjacent squares
        children = []

        for new_position in moves:
            # get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # make sure position is within map
            if node_position[0] > n_rows - 1 or node_position[0] < 0 or node_position[1] > n_columns - 1 or node_position[1] < 0:
                continue

            # make sure node is not in a wall
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # create new node
            new_node = Node(current_node, node_position)

            # append
            children.append(new_node)

            # loop through children
            for child in children:
                # if child is in visited list
                if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                    continue

                # create the g, h and f values
                child.g = current_node.g + cost

                # calculate heuristic cost using euclidean distance
                child.h = (((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))

                child.f = child.g + child.h

                # if child already in yet_to_visit list and the g cost is lower
                if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                    continue

                # add child to yet_to_visit_list
                yet_to_visit_list.append(child)


if __name__ == '__main__':
    maze = [
        [0, 1, 1, 0],
        [0, 0, 0, 1],
        [1, 1, 0, 0],
        [1, 1, 1, 0]
    ]

    start = [0, 0]
    end = [3, 3]
    cost = 1  # per movement

    path = search(maze, cost, start, end)

    print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) for row in path]))
