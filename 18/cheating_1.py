from collections import defaultdict, namedtuple, deque
import networkx as nx
from copy import deepcopy
from pprint import pprint
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt;

Point = namedtuple('P', 'x y')

class Path():
    """
    A class to hold objects representing a path along our grid

    Attributes
    ----------
    current : int
        a bit-masked list of points on this path
    collected_keys : int
        a bit-masked list of keys that we "hold" having traveled on this path
    length : int
        the length of the path
    """
    def __init__(self, current, collected_keys, length):
        self.current = current
        self.collected_keys = collected_keys
        self.length = length

    def get_state(self):
        """
        Get a 'hash' of this path's state by looking at what points we've 
        visited and what keys we currently hold
        """
        unique_state = (self.current, self.collected_keys)
        return unique_state

    def path_length(self):
        """
        Get the length (in keys) of the path by converting the list of 
        collected keys to binary, and counting the number of ones. This returns
        the number of keys that are on this path
        """
        return bin(self.collected_keys).count("1")

    def __repr__(self):
        """
        String representation of this is given by the list of current points 
        on this path, plus the list of collected keys converted to binary, plus
        the current length of the path
        """
        return str(self.current) + " " + str(bin(self.collected_keys)) + " : " + str(self.length)

def get_grid(part_b=False):
    """
    Parameters
    ----------
    part_b : bool
        flag for the second part of the problem, telling the program to
        quadruple the grid and put a robot in each corner

    Returns
    -------
    grid : defaultdict
        a dictionary (keys are Point objects) containing all valid positions on
        the grid as having a value of 1
    keys : dict
        a dictionary (keys are "key values" 1-N) containing the position of each
        key on the grid
    doors: dict
        a dictionary (keys are "key values" 1-N) containing the position of 
        each door that is unlocked by a given key
    start_points : list
        a list of the starting points (length 1 for part one)
    x : int
        max x index of the input grid
    y : int
        max y index of the input grid
    """
    grid = defaultdict(int)
    keys = {}
    doors = {}
    start_points = []

    with open("18/input") as f:

        lines = list(map(lambda x : list(x.strip()), f.readlines()))
        mid_y = (len(lines) - 1) // 2
        mid_x = (len(lines[0]) - 1) // 2
        if part_b:
            lines[mid_y-1][mid_x-1:mid_x+2] = "@#@"
            lines[mid_y][mid_x-1:mid_x+2] = "###"
            lines[mid_y+1][mid_x-1:mid_x+2] = "@#@"

        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c != '#':
                    p = Point(x,y)
                    grid[p] = 1
                    if c == '@':
                        start_points.append(p)
                    elif c != '.':
                        o = ord(c)
                        if o >= 97:
                            keys[o - 97] = p
                        else:
                            doors[o - 65] = p

    total_start_points = len(start_points)
    keys = {k + total_start_points : v for k, v in keys.items()}
    doors = {k + total_start_points : v for k, v in doors.items()}

    return grid, keys, doors, start_points, x, y

def get_surrounding_points(p):
    return set([
        Point(p.x, p.y-1),
        Point(p.x, p.y+1),
        Point(p.x-1, p.y),
        Point(p.x+1, p.y),
    ])

def build_graph(grid, max_x, max_y, plot=False):
    """
    Convert the input grid into a graph structure for easier processing

    Parameters
    ----------
    grid : defaultdict
        The input puzzle grid
    max_x : int
        the maximum x value of the grid
    max_y : int
        the maximum y value of the grid

    Returns
    -------
    G : nx.Graph
        a networkx graph containing edges connecting adjacent points on the
        input grid
    """

    edges = []
    for x in range(max_x+1):
        for y in range(max_y+1):
            p = Point(x,y)
            if grid[p]:
                for sp in get_surrounding_points(p):
                    if grid[sp]:
                        edges.append((p,sp))
    G = nx.Graph(edges)
    labels = {n : f'({n.x}, {n.y})' for n in G.nodes()}
    G.graph['labels'] = labels

    if plot:
        nx.draw_kamada_kawai(G, with_labels=True, labels=G.graph['labels']);
        plt.show()

    return G

def get_distance(G, p0, p1, doors):
    """
    Parameters
    ----------
    G : nx.Graph
        The graph representing the grid for this puzzle
    p0 : Point (namedtuple)
        the "starting point"
    p1 : Point (namedtuple)
        the "ending point"
    doors: dict
        a dictionary (keys are "key values" 1-N) containing the position of 
        each door that is unlocked by a given key

    Returns
    -------
    distance : int
        the shortest distance between the two points p0 and p1
    doors_in_way : int
        a list (expressed as a bitmask) of the doors between points p0 and p1
    """
    if not nx.has_path(G, p0, p1):
        return None
    # get the shortest path along this graph using networkX
    path = nx.shortest_path(G, p0, p1)
    # convert the path list to a set
    path_set = set(path)
    # assume there are zero doors in the way at first
    doors_in_way = 0
    # loop through the doors dict
    for k, p in doors.items():
        # if this door's Point object is in the path we found, add it (bitwise)
        # to the list of doors contained on this path
        if p in path_set:
            doors_in_way += (1 << k)
    # distance is actually one less than the length of the list of edges on the path
    distance = len(path) - 1

    # return the distance and which doors are on the path
    return distance, doors_in_way

def get_key_to_key(G, keys, doors, start_points, start_points_nums):
    """
    Parameters
    ----------
    G : nx.Graph
        graph representing this grid
    keys : dict
        a dictionary (keys are "key values" 1-N) containing the position of each
        key on the grid
    doors: dict
        a dictionary (keys are "key values" 1-N) containing the position of 
        each door that is unlocked by a given key
    start_points : list
        a list of the starting points (length 1 for part A, length 5 for part B)
    start_points_nums : list
        a list representing the starting point number (same length as 
        start_points)

    Returns
    -------
    key_to_key : dict
        A dictionary containing the distance along the graph for every key to 
        every other key. Keys of this dictionary are the "from" keys (represented in
        bit (key 2 is 2**2=4); each value is another dictionary, whose keys are 
        the "to" keys, and whose values are a tuple of distance between the two 
        keys and the doors in the way, represented by a bitmask)
    """
    key_to_key = defaultdict(dict)

    # convert key "indices" to bit values, so this dict looks like:
    # {1: 2, 2: 4, 3: 8, 4: 16, etc. for the number of total keys}
    key_to_bits = {k : 1 << k for k in keys.keys()}

    # loop through starting points (just one iteration for part A)
    for start_point, start_point_num in zip(start_points, start_points_nums):
        # calculate the "bit value" for this starting point
        start_point_bits = 1 << start_point_num
        # loop through the keys; k is a number from 1 to N; p is a Point with 
        # x and y values
        for k, p in keys.items():
            # get the bit value for this key (i.e. if k == 6, k_bits == 64)
            k_bits = key_to_bits[k]
            # get the distance on this grid from the starting point to this key,
            # accounting for the doors
            res = get_distance(G, start_point, p, doors)
            if res is not None:
                distance, doors_in_way = res
                key_to_key[start_point_bits][k_bits] = (distance, doors_in_way)

    # at this point, key_to_key has the distance from each starting point (just 
    # one if we're on part A) to all the keys in the puzzle

    # in this loop, find the distances between all the keys
    for k0, k1 in combinations(keys.keys(), 2):
        k0_bits = key_to_bits[k0]
        k1_bits = key_to_bits[k1]

        res = get_distance(G, keys[k0], keys[k1], doors)
        if res is not None:
            distance, doors_in_way = res
            key_to_key[k0_bits][k1_bits] = (distance, doors_in_way)
            key_to_key[k1_bits][k0_bits] = (distance, doors_in_way)

    # at this point, key_to_key contains the distance from each starting point 
    # to all the keys, as well as from each key to all the other keys
    # (assuming there's a path between them, which there likeley isn't for a
    # number of the keys in part B)
    return dict(key_to_key)

def find_next_possible_paths(key_to_key, path):
    """
    Generator to find the next possible path for a given path using the 
    key_to_key inter-key distance dictionary
    """
    current_positions = path.current
    # print(f'{path.current} : {path.collected_keys} : {path.length}')
    # loop through the keys and values in key_to_key (the "from" positions)
    for k0, v0 in key_to_key.items():
        # bitwise AND between k0 and the current position
        if k0 & current_positions:
            # loop through the keys and values in the "to" positions of key_to_key
            for k1, v1 in v0.items():
                # if k1 is not one of the collected keys:
                if not k1 & path.collected_keys:
                    dist, doors_in_way = v1
                    # check to see if we have keys for each of the doors currently in the way
                    if doors_in_way & path.collected_keys == doors_in_way:
                        # set the new position (not really sure how this works)
                        # ^ essentially clears the bit representing the robot that is going to move
                        # (for Part A, this clears the whole list)
                        # | combines two sets to form one containing items in either
                        #  so it adds the k1 position as the new robot position
                        new_position = current_positions ^ k0 | k1
                        # yield a Path object with the new position, this "to" key added to 
                        # the collected keys and the distance added to the path length
                        # this appears to only do something on the part B solution; 
                        # otherwise the new_position is just k1
                        # print(f'NEW: {new_position} : {path.collected_keys + k1} : {path.length + dist}')
                        yield Path(new_position, path.collected_keys + k1, path.length + dist)

def find_smallest_path(grid, keys, doors, start_points, max_x, max_y):
    """
    Parameters
    ----------
    grid : defaultdict
        a dictionary (keys are Point objects) containing all valid positions on
        the grid as having a value of 1
    keys : dict
        a dictionary (keys are "key values" 1-N) containing the position of each
        key on the grid
    doors: dict
        a dictionary (keys are "key values" 1-N) containing the position of 
        each door that is unlocked by a given key
    start_points : list
        a list of the starting points (length 1 for part one)
    x : int
        max x index of the input grid
    y : int
        max y index of the input grid

    Returns
    -------
    min_length : int
        The shortest path length found
    counter : int
        The number of iterations it took to process
    """

    # create a graph from the grid of nodes
    G = build_graph(grid, max_x, max_y, plot=False)

    # total_keys is an integer that tells us how many keys we need to find
    total_keys = len(keys)

    # start_points_nums is a list created by counting number of starting positions
    start_points_nums = list(range(len(start_points)))
    # start_points_bits is a single number representing the bitwise sum of all those positions
    # i.e. for [0, 1, 2, 3, 4], it is sum([2**0, 2**1, 2**2, 2**3, 2**4]) = 31
    start_points_bits = int(np.bitwise_or.reduce(list(map(lambda x : 1 << x, start_points_nums))))

    # get a dictionary with a lookup table of distances from each key and 
    # starting point to every other key, as well as what doors are in the way
    key_to_key = get_key_to_key(G, keys, doors, start_points, start_points_nums)

    full_paths = []
    start_path = Path(start_points_bits, 0, 0)

    min_full_path_length = 1000000000000

    # a dictionary with default values of zero
    min_path_lengths = defaultdict(int)

    counter = 0
    # possible_paths holds all the "options" for paths as we are branching
    # it is a dequeue object, which is like a list, but optimized for getting
    # objects either from the start or end (O(1) performance)
    possible_paths = deque([start_path])
    while possible_paths:
        counter += 1

        # get a path from the left side of possible_paths
        path = possible_paths.popleft()

        # check if min_path_lengths value for this path's state is less than
        # the length of this path; if it is, then skip this iteration of the 
        # loop, which will break if possible_paths is currently empty
        if min_path_lengths[path.get_state()] < path.length:
            continue

        possible_moves = []

        # loop through the generator that finds the next possible path for the
        # given path
        for new_path in find_next_possible_paths(key_to_key, path):
            # if this new path's length is less than the previously seen minimum
            # full path length
            if new_path.length < min_full_path_length:
                # store the unique state of this path
                unique_state = new_path.get_state()
                better_path = False
                # if this path has already been seen
                if unique_state in min_path_lengths:
                    # if it's length is less than that which was already seen
                    if new_path.length < min_path_lengths[unique_state]:
                        # store it as the new min path for this state and mark 
                        # that we're on a better version
                        old_length = min_path_lengths[unique_state]
                        min_path_lengths[unique_state] = new_path.length
                        better_path = True
                else:
                    # if we haven't seen it, then assume it's a new best bath 
                    # for this state
                    min_path_lengths[unique_state] = new_path.length
                    better_path = True

                # if we detected that this path is better than the previous
                # version in the above section
                if better_path:
                    # if the path length of this path is same as the total 
                    # number of keys we need to find (i.e. it's complete)
                    if new_path.path_length() == total_keys:
                        if new_path.length < min_full_path_length:
                            # if the length is less than the previous minimum
                            # "full path" length, set that value to this path's
                            # length
                            min_full_path_length = new_path.length
                        # append this path to the list of full paths
                        full_paths.append(new_path)
                    else:
                        # if this path is not a full path, append it to the 
                        # possible paths that we need to check
                        possible_paths.append(new_path)

    
    return min([p.length for p in full_paths]), counter

import time

# Part A
start = time.time()
grid, keys, doors, start_points, max_x, max_y = get_grid()
min_length, counter = find_smallest_path(grid, keys, doors, start_points, max_x, max_y)
end = time.time()

print("Part A")
print("Iterations:", counter)
print("Min path length:", min_length)
print(f"Time to complete: {end-start:.2f}s")

# Part B
start = time.time()
grid, keys, doors, start_points, max_x, max_y = get_grid(part_b=True)
min_length, counter = find_smallest_path(grid, keys, doors, start_points, max_x, max_y)
end = time.time()

print("Part B")
print("Iterations:", counter)
print("Min path length:", min_length)
print(f"Time to complete: {end-start:.2f}s")
