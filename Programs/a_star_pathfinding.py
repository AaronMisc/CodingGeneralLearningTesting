import heapq
import numpy as np

class Node:
    def __init__(self, parent=None, position=None, g=0, h=0, f=0):
        self.parent = parent
        self.position = position

        self.g = g
        self.h = h
        self.f = f

    def __eq__(self, other):
        return isinstance(other, Node) and self.position == other.position
    
    def __hash__(self):
        return hash(self.position)
    
    def __repr__(self):
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    def __lt__(self, other):
        "Less than"
        return self.f < other.f
    
    def __gt__(self, other):
        "Greater than"
        return self.f > other.f

    def calculate_distance_to_node(self, other):
        return abs(self.position[0] - other.position[0]) + abs(self.position[1] - other.position[1])

class Maze:
    def __init__(self, maze_map:np.ndarray, is_walkable_function=lambda x: x == 0):
        self.maze_map = maze_map
        self.is_walkable_function = is_walkable_function

        self.height = self.maze_map.shape[0]
        self.width = self.maze_map.shape[1]

    def to_string(self):
        string_representation = ""
        for i in range(self.height):
            for j in range(self.width):
                string_representation += str(self.maze_map[i][j])
            string_representation += "\n"
        return string_representation

    def check_if_coordinate_is_inside_maze(self, position):
        return 0 <= position[0] < self.height and 0 <= position[1] < self.width
    
    def get_list(self):
        return self.maze_map.tolist()
    
    def check_if_walkable(self, position):
        return self.is_walkable_function(self.maze_map[position[0]][position[1]])
    
    def get_height(self):
        return self.height
    
    def get_width(self):
        return self.width

    def set_point_at_position(self, position, value):
        self.maze_map[position[0]][position[1]] = value

    def substitute_values(self, old_to_new_value:dict={0: " ", 1: "\u2588", 2: ".",}):
        return Maze(np.vectorize(old_to_new_value.get)(self.maze_map))

    def mark_path(self, path, path_value=2):
        for position in path:
            self.set_point_at_position(position, path_value)

def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]

isometric_adjacent_coordinates = ((0, -1), (0, 1), (-1, 0), (1, 0),)
orthogonal_adjacent_coordinates = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

def astar(maze, start:tuple[int], end:tuple[int], relative_adjacent_coordinates:tuple[tuple]=isometric_adjacent_coordinates, h_multiplier:int=1):
    start_node = Node(None, start)
    end_node = Node(None, end)

    nodes_to_check_list = []
    checked_nodes_set = set()

    heapq.heapify(nodes_to_check_list) 
    heapq.heappush(nodes_to_check_list, start_node)

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = maze.get_width() * maze.get_height() * 2

    # what squares do we search
    adjacent_squares = relative_adjacent_coordinates

    # Loop until you find the end
    while len(nodes_to_check_list) > 0:
        outer_iterations += 1

        if outer_iterations > max_iterations:
            raise Exception("Too many iterations for pathfinding.")
        
        # Get the current node
        current_node = heapq.heappop(nodes_to_check_list)
        checked_nodes_set.add(current_node)

        # Found the goal
        if current_node == end_node:
            return return_path(current_node)

        children = []
        
        for adjacent_position in adjacent_squares: # Adjacent squares
            node_position = (current_node.position[0] + adjacent_position[0], current_node.position[1] + adjacent_position[1])

            if not maze.check_if_coordinate_is_inside_maze(node_position):
                continue
            if not maze.check_if_walkable(node_position):
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        # Loop through children
        for child in children:
            # THREE IDENTICAL CODES FOR: If child is on the closed list, continue

            if child in checked_nodes_set:
                continue

            child.g = current_node.g + 1            
            child.h = child.calculate_distance_to_node(end_node)
            child.f = child.g + child.h * h_multiplier

            # Child is already in the nodes to check list
            if len([open_node for open_node in nodes_to_check_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                continue
            # for open_node in nodes_to_check_list:
            #     if child.position == open_node.position and child.g > open_node.g:
            #         continue

            # Add the child to the nodes to check list
            heapq.heappush(nodes_to_check_list, child)

    raise Exception("Couldn't get a path to destination")

def example(print_maze = True):

    maze = Maze(np.array(
        [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
        [0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
        [0,0,0,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,],
        [0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,],
        [0,0,0,1,0,1,1,1,1,0,1,1,0,0,1,1,1,0,0,0,1,1,1,1,1,1,1,0,0,0,],
        [0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,1,0,0,0,0,0,0,1,1,1,0,],
        [0,0,0,1,0,1,1,0,1,1,0,1,1,1,0,0,0,0,0,1,0,0,1,1,1,1,1,0,0,0,],
        [0,0,0,1,0,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,0,1,0,1,1,],
        [0,0,0,1,0,1,0,1,1,0,1,1,1,1,0,0,1,1,1,1,1,1,1,0,1,0,1,0,0,0,],
        [0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,1,0,],
        [0,0,0,1,0,1,1,1,1,0,1,0,0,1,1,1,0,1,1,1,1,0,1,1,1,0,1,0,0,0,],
        [0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,1,],
        [0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,],])
    )

    start = (0, 0)
    end = (maze.get_height()-1, maze.get_width()-1)

    path = astar(maze, start, end)

    if print_maze:
        maze.mark_path(path)
        print(maze.substitute_values().to_string())

    print(path)

example()