"""
--- Day 20: Donut Maze ---
You notice a strange pattern on the surface of Pluto and land nearby to get a
closer look. Upon closer inspection, you realize you've come across one of the
famous space-warping mazes of the long-lost Pluto civilization!

Because there isn't much space on Pluto, the civilization that used to live here
thrived by inventing a method for folding spacetime. Although the technology is
no longer understood, mazes like this one provide a small glimpse into the daily
life of an ancient Pluto citizen.

This maze is shaped like a donut. Portals along the inner and outer edge of the
donut can instantly teleport you from one side to the other. For example:

            A           
            A           
    #######.#########  
    #######.........#  
    #######.#######.#  
    #######.#######.#  
    #######.#######.#  
    #####  B    ###.#  
    BC...##  C    ###.#  
    ##.##       ###.#  
    ##...DE  F  ###.#  
    #####    G  ###.#  
    #########.#####.#  
    DE..#######...###.#  
    #.#########.###.#  
    FG..#########.....#  
    ###########.#####  
                Z       
                Z       

This map of the maze shows solid walls (#) and open passages (.). Every maze on
Pluto has a start (the open tile next to AA) and an end (the open tile next to
ZZ). Mazes on Pluto also have portals; this maze has three pairs of portals: BC,
DE, and FG. When on an open tile next to one of these labels, a single step can
take you to the other tile with the same label. (You can only walk on . tiles;
labels and empty space are not traversable.)

One path through the maze doesn't require any portals. Starting at AA, you could
go down 1, right 8, down 12, left 4, and down 1 to reach ZZ, a total of 26
steps.

However, there is a shorter path: You could walk from AA to the inner BC portal
(4 steps), warp to the outer BC portal (1 step), walk to the inner DE (6 steps),
warp to the outer DE (1 step), walk to the outer FG (4 steps), warp to the inner
FG (1 step), and finally walk to ZZ (6 steps). In total, this is only 23 steps.

Here is a larger example:

                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               

Here, AA has no direct path to ZZ, but it does connect to AS and CP. By passing
through AS, QG, BU, and JO, you can reach ZZ in 58 steps.

In your maze, how many steps does it take to get from the open tile marked AA to
the open tile marked ZZ? 
"""

import numpy as np
import networkx as nx
from collections import namedtuple, defaultdict
from colorama import Fore, Back, Style 
import matplotlib.pyplot as plt
import math
import string
import itertools

Point = namedtuple('P', 'x y')

def get_grid(fname, plot=False, render=True, part2=False):

    def _get_letter(arr, x, y):
        try:
            if arr[y, x] in string.ascii_uppercase:
                return arr[y, x]
        except IndexError as e:
            pass

        return None

    with open(fname, 'r') as f:
        lines = f.readlines()
        lines = [list(l.strip('\n')) for l in lines]

    grid = defaultdict(int)
    
    arr = np.array(lines)

    for y, x in np.ndindex(arr.shape):
        grid[(x,y)] = arr[y,x]

    G = nx.Graph()
    for y, x in np.argwhere(arr == '.'):
        p = Point(x, y)
        G.add_node(p) 
        for yp, xp in [(y+1, x  ), (y-1, x  ),
                       (y  , x+1), (y  , x-1)]: 
            try:
                if arr[yp, xp] == '.':
                    G.add_edge(Point(x, y), Point(xp, yp))
            except IndexError as e:
                pass

        down_letter = _get_letter(arr, x, y+1)
        up_letter = _get_letter(arr, x, y-1)
        left_letter = _get_letter(arr, x-1, y)
        right_letter = _get_letter(arr, x+1, y)
        
        if down_letter is not None:
            G.nodes[p]['val'] = _get_letter(arr, x, y+1) + _get_letter(arr, x, y+2)
        if up_letter is not None:
            G.nodes[p]['val'] = _get_letter(arr, x, y-2) + _get_letter(arr, x, y-1)
        if left_letter is not None:
            G.nodes[p]['val'] = _get_letter(arr, x-2, y) + _get_letter(arr, x-1, y)
        if right_letter is not None:
            G.nodes[p]['val'] = _get_letter(arr, x+1, y) + _get_letter(arr, x+2, y)

        if 'val' in G.nodes[p] and G.nodes[p]['val'] == 'AA':
            G.graph['starting_node'] = p
        if 'val' in G.nodes[p] and G.nodes[p]['val'] == 'ZZ':
            G.graph['ending_node'] = p

    for node_r in G.nodes(data=True):
        for node in G.nodes(data=True):
            if node != node_r and len(node[1]) > 0 and len(node_r[1]) > 0 and \
                node[1]['val'] == node_r[1]['val']:
                G.add_edge(node[0], node_r[0])

    labels = {n[0] : f'({n[0].x}, {n[0].y})' + (f'\n{n[1]["val"]}' 
                                             if 'val' in n[1] else '') 
                                             for n in G.nodes(data=True)}
    G.graph['labels'] = labels

    if plot:
        nx.draw_kamada_kawai(G, with_labels=True, labels=G.graph['labels']);
        plt.show()

    if render: render_graph(G)

    return G


def render_graph(G):

    # G is a networkx graph of positions
    x_max = max([n[0] for n in G.nodes()])
    y_max = max([n[1] for n in G.nodes()])

    backgrounds = [Back.RED, Back.YELLOW, Back.GREEN, 
                   Back.BLUE, Back.MAGENTA, Back.CYAN]
    def bg_cycle(n):
        return backgrounds[n % len(backgrounds)]
    
    portals = set()
    for n in G.nodes(data=True):
        if 'val' in n[1]:
            portals.add(n[1]['val'])
    portals = sorted(list(portals))
    p_dict = {}
    for i, p in enumerate(portals):
        p_dict[p] = bg_cycle(i)
    num_portals = len(portals)

    # add two to account for borders
    arr = np.zeros((y_max + 2, x_max + 2), dtype='|U10')
    # Set up numpy array for printing using graph
    arr[:] = '#'
    portal_num = 0
    for n, d in G.nodes(data=True):
        if 'val' in d:
            arr[n.y, n.x] = p_dict[d['val']] + '.' + Style.RESET_ALL
            portal_num += 1
        else:
            arr[n.y, n.x] = '.'

    output_string = '\n'
    out_dict = {'#': '█',
                '.': '.'}

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

if __name__ == '__main__':

    G = get_grid('20/test_input1', plot=False)
    assert nx.shortest_path_length(G, 
                                   source=G.graph['starting_node'], 
                                   target=G.graph['ending_node']) == 23

    G = get_grid('20/test_input2', plot=False)
    assert nx.shortest_path_length(G, 
                                   source=G.graph['starting_node'], 
                                   target=G.graph['ending_node']) == 58    

    G = get_grid('20/input')
    path_len = nx.shortest_path_length(G, 
                                       source=G.graph['starting_node'], 
                                       target=G.graph['ending_node'])
    print(f'Shortest path is {path_len}')
    
    # Answer is 516