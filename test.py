from math import sqrt, ceil
import time


class Node:
    '''
    Class for nodes
    '''
    def __init__(self, parent = None, position= None):
        '''
        initialize the object
        '''
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
        self.wall_broken = False
    
    def __eq__(self, other):
        '''
        works for equality chacks
        '''
        return ((self.position == other.position) and (self.wall_broken == other.wall_broken))
    
    def __repr__(self):
        '''
        for printing the object
        '''
        return 'Position: {} Wall_Broken: {}'.format(self.position, self.wall_broken)
    
def astar(maze):
    '''
    A* algorithm
    takes a maze
    return the shortest path
    '''
    # The starting and ending position is always left top and right bottom respectively
    start_pos = (0,0)
    end_pos = (len(maze)-1, len(maze[0])-1)

    # Create the start and end node
    start = Node(parent=None, position=start_pos)
    end = Node(parent=None, position=end_pos)

    # Yet to visit and Visited list
    yet_to_visit = []
    visited = []

    # Keep start in yet to visit
    yet_to_visit.append(start)

    while(len(yet_to_visit)):
        # Loop untill we completely search all nodes

        # We need the lowest f in current node
        current_node = yet_to_visit[0]
        # current_index = 0
        for node in yet_to_visit:
            if current_node.f > node.f:
                current_node = node
                # current_index = idx
        
        # Remove the current node from yet_to_visit
        yet_to_visit.remove(current_node)
        # Add the current node to the visited
        visited.append(current_node)

        # Check if current node is goal or not
        if current_node.position == end.position:
            temp = current_node
            path = []
            while temp:
                path.append(temp.position)
                temp = temp.parent
            return path[::-1]

        # Generate children
        children = []
        for position in [(0,1), (0,-1), (1,0), (-1,0)]:
            new_position = (current_node.position[0] + position[0], current_node.position[1] + position[1])
            # Check the validity of borders
            if new_position[0] < 0 or new_position[0] >= len(maze) or new_position[1] < 0 or new_position[1] >= len(maze[0]):
                continue

            # Check if wall
            if maze[new_position[0]][new_position[1]] == 1:
                # Check if path has wall broken
                if current_node.wall_broken:
                    # Wall has been broken
                    continue
                else:
                    # Wall has not been broken
                    # check if visited
                    check = Node(current_node, new_position)
                    check.wall_broken = True
                    flag = 0
                    for visited_nodes in visited:
                        if check == visited_nodes:
                            flag = 1
                            break
                    if flag == 0:
                        children.append(check)
                    continue
            
            # Check if already visited
            flag = 0
            check = Node(current_node, new_position)
            check.wall_broken = current_node.wall_broken
            for visited_nodes in visited:
                if check == visited_nodes:
                    flag = 1
                    break
            if flag == 1:
                continue
            
            # If all the above things are not True
            children.append(check)
        
        # Iterate over children to consider the yet_to_visit
        for child in children:
            # Heuristics
            child.g = current_node.g + 1
            child.h = ceil(sqrt((end.position[0] - child.position[0])**2 + (end.position[1] - child.position[1])**2))
            child.f = child.g + child.h

            # Check if child in open list
            for open_node in yet_to_visit:
                if open_node == child:
                    # check for the path measure
                    if open_node.g > child.g:
                        idx = yet_to_visit.index(open_node)
                        yet_to_visit[idx] = child
                        continue
                    else:
                        continue
            
            # Add the node to yet_to_visit
            yet_to_visit.append(child)


def test_algorithm(maze):
    n_rows = len(maze)
    n_cols = len(maze[n_rows - 1])

    start_pos = (0, 0)
    end_pos = (n_rows - 1, n_cols - 1)

    print(f"Start Point: {tuple(start_pos)}.")
    print(f"End Point: {tuple(end_pos)}.")

    start_time = time.time()
    resultant_path = astar(maze)  # function to search without removing a wall
    # solvable, resultant_path = destroy_wall(maze)  # function to search with ability to remove 1 wall
    end_time = time.time()

    print(f"Time taken to execute: {end_time - start_time}s")

    print(f"Resulting path coordinates: {resultant_path}")

    print(f"Cost: {len(resultant_path)}")

    print("\n")

    print("Solved maze:")

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
