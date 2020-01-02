"""
"""
from colorama import Fore, Back, Style 
from copy import deepcopy
import networkx as nx
import numpy as np
from collections import defaultdict, namedtuple, deque
import matplotlib.pyplot as plt
import string
from itertools import combinations
import math

Point = namedtuple('P', 'x y')

def get_grid(fname, plot=False, render=True, part2=False):
    with open(fname, 'r') as f:
        lines = f.readlines()
        lines = [list(l.strip()) for l in lines]

    grid = defaultdict(int)
    
    arr = np.array(lines)

    for y, x in np.ndindex(arr.shape):
        grid[(x,y)] = arr[y,x]

    if part2:
        mid_y = (len(lines) - 1) // 2
        mid_x = (len(lines[0]) - 1) // 2
        replacement = np.array([['@','#','@'],
                                ['#','#','#'],
                                ['@','#','@']])
        arr[mid_y-1:mid_y+2,
            mid_x-1:mid_x+2] = replacement

    G = nx.Graph()
    G.graph['keys_held'] = set()
    G.graph['name'] = 'root'
    G.graph['keys'] = {}
    G.graph['doors'] = {}
    G.graph['cur_pos'] = None
    G.graph['starting_points'] = []

    for y, x in np.argwhere(arr != '#'):
        G.add_node(Point(x, y)) #, val=arr[y,x])
        for yp, xp in [(y+1, x  ), (y-1, x  ),
                       (y  , x+1), (y  , x-1)]: 
            try:
                if arr[yp, xp] != '#':
                    G.add_edge(Point(x, y), Point(xp, yp))
            except IndexError as e:
                pass

        if arr[y, x] in string.ascii_lowercase:
            G.graph['keys'][arr[y, x]] = Point(x, y)
        elif arr[y, x] in string.ascii_uppercase:
            G.graph['doors'][arr[y, x].lower()] = Point(x, y)
        
        if arr[y, x] == '@':
            G.graph['starting_points'].append(Point(x, y))
            G.graph['cur_pos'] = Point(x, y)

    labels = {n : f'({n.x}, {n.y})' for n in G.nodes()}
    G.graph['labels'] = labels

    if plot:
        nx.draw_kamada_kawai(G, with_labels=True, labels=G.graph['labels']);
        plt.show()

    if render: render_graph(G)

    G.graph['key_pos_to_letter'] = {}
    for k, v in G.graph['keys'].items():
        G.graph['key_pos_to_letter'][v] = k

    return G

def render_graph(G):

    # G is a networkx graph of positions
    x_max = max([n[0] for n in G.nodes()])
    y_max = max([n[1] for n in G.nodes()])
    
    # add two to account for borders
    arr = np.zeros((y_max + 2, x_max + 2), dtype=str)
    # Set up numpy array for printing using graph
    arr[:] = '#'
    for n in G.nodes():
        arr[n.y, n.x] = '.'
    for p in G.graph['starting_points']:
        arr[p.y, p.x] = '@'
    for k, p in G.graph['keys'].items():
        arr[p.y, p.x] = k
    for k, p in G.graph['doors'].items():
        arr[p.y, p.x] = k.upper()

    output_string = '\n'
    out_dict = {'#': '█',
                '@': Fore.YELLOW + '@',
                '.': ' '}
    for l in string.ascii_lowercase:
        out_dict[l] = Back.LIGHTGREEN_EX + Fore.BLACK + l
    for l in string.ascii_uppercase:
        out_dict[l] = Back.RED + l

    top_row =   ''.join([f'{i}         ' for i in range(math.ceil(x_max / 10))])
    second_row = '0123456789' * math.ceil(x_max / 10)
    output_string += '   ' + top_row + '\n'
    output_string += '   ' + second_row[:x_max + 2] + '\n'
    for y in range(arr.shape[0]):
        output_string += f'{y:02g} '
        for x in range(arr.shape[1]):
            c = arr[y, x]
            try:
                output_string += out_dict[c]
            except KeyError as e:
                output_string += c
            output_string += Style.RESET_ALL
        output_string += '\n'
    
    print(output_string, end='')
    # print(f"Keys held: {G.graph['keys_held']}")
    return(output_string)


def get_distance(G, point1, point2):
    """
    Get the shortest distance between two points along a Graph

    Parameters
    ----------
    G : nx.Graph
        The graph representing the grid for this puzzle
        Must have a graph attribute named "doors" containing the position of
        each door that is unlocked by a given key
    point1 : Point (namedtuple)
        the "starting point"
    point2 : Point (namedtuple)
        the "ending point"
    
    Returns
    -------
    distance : int
        the shortest distance between the two points point1 and point2
    doors_in_way : set
        a set of the doors between points point1 and point2
    """
    if not nx.has_path(G, point1, point2):
        return None
    # get the shortest path along this graph using networkX
    path = nx.shortest_path(G, point1, point2)

    # convert the path list to a set
    path_set = set(path)

    # assume there are zero doors in the way at first
    doors_in_way = set()

    # loop through the doors dict
    for k, p in G.graph['doors'].items():
        # if this door's Point object is in the path we found, add it (bitwise)
        # to the list of doors contained on this path
        if p in path_set:
            doors_in_way.add(k)
    # distance is actually one less than the length of the list of edges on the path
    distance = len(path) - 1

    # return the distance and which doors are on the path
    return distance, doors_in_way


def find_next_possible_paths(dist_mat, path):
    """
    Generator to find the next possible path for a given path using the 
    dist_mat inter-key distance dictionary
    """
    # current_positions is a tuple of current positions (length 1 for part A) 
    # where the position is given by a letter 'a-z'
    current_positions = path.current
    print('', end='')
    # loop through the keys and values in dist_mat (the "from" positions)
    for k0, v0 in dist_mat.items():
        # check to see if this key from dist_mat is one of our current positions
        if k0 in current_positions:
            # if it is, loop through the keys and values in the "to" positions 
            # of dist_mat
            for k1, v1 in v0.items():
                # if k1 is not one of the collected keys (i.e. we want to go there):
                if k1 not in path.collected_keys:
                    # doors_in_way is set of letters
                    dist, doors_in_way = v1

                    # convert path.collected_keys to set of letters:
                    collected_keys_as_letter = \
                        {path.G.graph['key_pos_to_letter'][k] 
                        for k in path.collected_keys}

                    # check to see if we have keys required for each of the 
                    # doors currently between our current position (k0) and 
                    # where we want to go (k1)
                    # path.collected_keys is set of Points
                    if doors_in_way.issubset(collected_keys_as_letter):
                        # set the new position for this robot by generating a 
                        # new tuple with this robot's position changed
                        index = current_positions.index(k0)
                        new_position = current_positions[:index] + (k1,) + current_positions[index+1:]
                        # yield a Path object with the new position, this "to" key added to 
                        # the collected keys and the distance added to the path length
                        # this appears to only do something on the part B solution; 
                        # otherwise the new_position is just k1
                        yield Path(new_position, 
                                   path.collected_keys.union({k1}), 
                                   path.length + dist,
                                   path.G)


def get_dist_mat(G):
    """
    Parameters
    ----------
    G : nx.Graph
        graph representing this grid

    Attributes of G.graph:
        keys : dict
            a dictionary (keys are "key values" a-z) containing the 
            position of each key on the grid as a Point (namedtuple)
        doors: dict
            a dictionary (keys are "key values" a-z) containing the position of 
            each door that is unlocked by a given key as a Point (namedtuple)
        starting_points : list
            a list of the starting points (length 1 for part A, length 5 for 
            part B)

    Returns
    -------
    dist_mat : dict
        A dictionary containing the distance along the graph for every key to 
        every other key. Keys of this dictionary are the "from" keys 
        (represented as a string 'a-z'; each value is another dictionary, 
        whose keys are  the "to" keys, and whose values are a tuple of distance
        between the two keys and the doors in the way, as a set)
    """
    # dist_mat[from][to] = distance
    # from and to are tuples (node definitions)
    # we want to pre-compute the distance from the starting point and all keys
    # to all other keys (and the starting point)
    # Also includes doors that need to be crossed as second item of tuple
    # and additional keys that are crossed as third item of tuple
    dist_mat = defaultdict(dict)
    for start_point in G.graph['starting_points']:
        for _to_key, _to_point in G.graph['keys'].items():
            res = get_distance(G, start_point, _to_point)
            if res is not None:
                distance, doors_in_way = res
                dist_mat[start_point][_to_point] = (distance, doors_in_way)

    froms = [v for k,v in G.graph['keys'].items()]
    for _from in froms:
        tos = froms.copy()
        tos.pop(tos.index(_from))
        for _to in tos:
            res = get_distance(G, _from, _to)
            if res is not None:
                distance, doors_in_way = res
                dist_mat[_from][_to] = (distance, doors_in_way)
    
    return dict(dist_mat)


def get_shortest_path(G):
    # get the distance matrix between keys (and starting points)
    # values are a tuple of distances and doors between the two points
    dist_mat = get_dist_mat(G)
    num_keys_to_find = len(G.graph['keys'])

    # list to hold the completed "full" paths
    full_paths = []
    start_path = Path(G.graph['starting_points'], set(), 0, G)
    min_full_path_length = 1000000000000  # set to something unreasonably high for the first iteration
    # a dictionary with default values of zero
    min_path_lengths = defaultdict(int)
    
    counter = 0
    # possible_paths holds all the "options" for paths as we are branching
    # it is a deque object, which is like a list, but optimized for getting
    # objects either from the start or end (O(1) performance)
    possible_paths = deque([start_path])
    
    while possible_paths:
        counter += 1

        path = possible_paths.popleft()

        # check the min_path_lengths dict for this particular state, if it's
        # less than the current path length, it's not worth calculating this 
        # path, so skip this iteration
        if min_path_lengths[path.get_state()] < path.length:
            continue

        for new_path in find_next_possible_paths(dist_mat, path):
            # check to see if the new path length is less than our current minimum
            # for any of the "full paths"
            if new_path.length < min_full_path_length:
                # store the unique state of this path
                unique_state = new_path.get_state()
                is_better_path = False
                # check to see if this path (position and keys held) has been seen 
                # before, if so, check to see if its length is less than what we had
                if unique_state in min_path_lengths:
                    # if this version of the new path has shorter length, store it
                    if new_path.length < min_path_lengths[unique_state]:
                        min_path_lengths[unique_state] = new_path.length
                        is_better_path = True
                else:
                    # if we haven't seenthis new path before, then we can assume
                    # it's the "best" path for this state
                    min_path_lengths[unique_state] = new_path.length
                    is_better_path = True
            
            # what to do if we detected this new_path is better than the old
            if is_better_path:
                # is this a "full" path (i.e. have we found all the keys)?
                if new_path.path_length_in_keys() == num_keys_to_find:
                    # set the minimum length for a new path to the smaller of this
                    # path's length and the previous minimum:
                    min_full_path_length = min(min_full_path_length, new_path.length)
                    full_paths.append(new_path)
                # it's not a full path, so add it to the possible paths to search
                else:
                    possible_paths.append(new_path)

    return min([p.length for p in full_paths])


class Path():
    """
    A class to instantiate objects representing a path along our grid

    Attributes
    ----------
    current : tuple
        a collection of the current Point for each robot (will be length 1 for 
        part A)
    collected_keys : set
        a set of keys that we "hold" from having traveled on this path
    length : int
        the length of the path
    G : nx.Graph
        the graph that holds information about this grid
    """
    def __init__(self, current, collected_keys, length, G):
        if isinstance(current, list):
            current = tuple(current)
        self.current = current
        self.collected_keys = collected_keys
        self.length = length
        self.G = G

    def get_state(self):
        """
        Get a 'hash' of this path's state by looking at what points we've 
        visited and what keys we currently hold
        """
        unique_state = (tuple(f'{p.x},{p.y}' for p in self.current), 
                        frozenset(self.collected_keys))
        return unique_state

    def path_length_in_keys(self):
        """
        Get the length (in keys) of the path by converting the list of 
        collected keys to binary, and counting the number of ones. This returns
        the number of keys that are on this path
        """
        return len(self.collected_keys)

    def __repr__(self):
        """
        String representation of this is given by the list of current points 
        on this path, plus the list of collected keys converted to binary, plus
        the current length of the path
        """
        return '-'.join([f'({p.x}, {p.y})' for p in self.current]) + " : " + \
               ''.join(sorted([G.graph['key_pos_to_letter'][i] for i in self.collected_keys])) + " : " + \
               str(self.length)


if __name__ == '__main__':
    
    import time

    testing = False

    if testing:
        # get the graph representing our puzzle
        G = get_grid('18/test_input2', plot=False)
        assert get_shortest_path(G) == 86

        G = get_grid('18/test_input3', plot=False)
        assert get_shortest_path(G) == 132

        G = get_grid('18/test_input4', plot=False)
        assert get_shortest_path(G) == 136

        G = get_grid('18/test_input5', plot=False)
        assert get_shortest_path(G) == 81

    G = get_grid('18/input', plot=False, render=True, part2=True)
    times = []
    for i in range(5):
        start = time.time()
        print(get_shortest_path(G))
        end = time.time()
        times.append(end-start)

    time_str = ', '.join([f'{t:.2f}s' for t in times])
    avg_time = sum(times)/5
    print(f"Times to complete part 2: {time_str}")
    print(f'Average computation time: {avg_time:.2f}s')

    # answer is 2136
    # Times to complete part 2: 61.80s, 64.90s, 63.79s, 70.48s, 67.11s
    # Average computation time: 65.61s