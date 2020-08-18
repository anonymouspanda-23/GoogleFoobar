class Node:
    def __int__(self, parent, position):
        self.g = 0
        self.h = 0
        self.f = 0

        self.parent = parent
        self.position = position


def a_star_search(maze, start=tuple(), end=tuple()):
    """
    a_star_search function attempts to look for a path, returns unsolvable as True if there is no possible path to end state
    :param maze:
    :param start:
    :param end:
    :return:
    """

    # calculate the number of rows and columns in the maze
    n_rows = len(maze)
    n_cols = len(maze[n_rows - 1])

    # calculating start and end if not set by user
    if start == ():
        start = (0, 0)

    if end == ():
        end = (len(maze) - 1, len(maze[n_rows - 1]) - 1)

    # print start and end coordinates to ensure calculations are working
    print(start)
    print(end)

    # define the maximum number of iterations before exiting
    max_iter = (n_rows * n_cols) ** 2  # maybe max_iter can be reduced to (n_rows ** n_cols)
    current_iter = 0




if __name__ == '__main__':

    maze = [
        [0, 1, 1, 0],
        [0, 0, 0, 1],
        [1, 1, 0, 0],
        [0, 0, 0, 0]
    ]

    a_star_search(maze, start=(3, 0))
