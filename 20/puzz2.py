"""
--- Part Two ---

Strangely, the exit isn't open when you reach it. Then, you remember: the
ancient Plutonians were famous for building recursive spaces.

The marked connections in the maze aren't portals: they physically connect to a
larger or smaller copy of the maze. Specifically, the labeled tiles around the
inside edge actually connect to a smaller copy of the same maze, and the smaller
copy's inner labeled tiles connect to yet a smaller copy, and so on.

When you enter the maze, you are at the outermost level; when at the outermost
level, only the outer labels AA and ZZ function (as the start and end,
respectively); all other outer labeled tiles are effectively walls. At any other
level, AA and ZZ count as walls, but the other outer labeled tiles bring you one
level outward.

Your goal is to find a path through the maze that brings you back to ZZ at the
outermost level of the maze.

In the first example above, the shortest path is now the loop around the right
side. If the starting level is 0, then taking the previously-shortest path would
pass through BC (to level 1), DE (to level 2), and FG (back to level 1). Because
this is not the outermost level, ZZ is a wall, and the only option is to go back
around to BC, which would only send you even deeper into the recursive maze.

In the second example above, there is no path that brings you to ZZ at the
outermost level.

Here is a more interesting example:

             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     

One shortest path through the maze is the following:

- Walk from AA to XF (16 steps)
- Recurse into level 1 through XF (1 step)
- Walk from XF to CK (10 steps)
- Recurse into level 2 through CK (1 step)
- Walk from CK to ZH (14 steps)
- Recurse into level 3 through ZH (1 step)
- Walk from ZH to WB (10 steps)
- Recurse into level 4 through WB (1 step)
- Walk from WB to IC (10 steps)
- Recurse into level 5 through IC (1 step)
- Walk from IC to RF (10 steps)
- Recurse into level 6 through RF (1 step)
- Walk from RF to NM (8 steps)
- Recurse into level 7 through NM (1 step)
- Walk from NM to LP (12 steps)
- Recurse into level 8 through LP (1 step)
- Walk from LP to FD (24 steps)
- Recurse into level 9 through FD (1 step)
- Walk from FD to XQ (8 steps)
- Recurse into level 10 through XQ (1 step)
- Walk from XQ to WB (4 steps)
- Return to level 9 through WB (1 step)
- Walk from WB to ZH (10 steps)
- Return to level 8 through ZH (1 step)
- Walk from ZH to CK (14 steps)
- Return to level 7 through CK (1 step)
- Walk from CK to XF (10 steps)
- Return to level 6 through XF (1 step)
- Walk from XF to OA (14 steps)
- Return to level 5 through OA (1 step)
- Walk from OA to CJ (8 steps)
- Return to level 4 through CJ (1 step)
- Walk from CJ to RE (8 steps)
- Return to level 3 through RE (1 step)
- Walk from RE to IC (4 steps)
- Recurse into level 4 through IC (1 step)
- Walk from IC to RF (10 steps)
- Recurse into level 5 through RF (1 step)
- Walk from RF to NM (8 steps)
- Recurse into level 6 through NM (1 step)
- Walk from NM to LP (12 steps)
- Recurse into level 7 through LP (1 step)
- Walk from LP to FD (24 steps)
- Recurse into level 8 through FD (1 step)
- Walk from FD to XQ (8 steps)
- Recurse into level 9 through XQ (1 step)
- Walk from XQ to WB (4 steps)
- Return to level 8 through WB (1 step)
- Walk from WB to ZH (10 steps)
- Return to level 7 through ZH (1 step)
- Walk from ZH to CK (14 steps)
- Return to level 6 through CK (1 step)
- Walk from CK to XF (10 steps)
- Return to level 5 through XF (1 step)
- Walk from XF to OA (14 steps)
- Return to level 4 through OA (1 step)
- Walk from OA to CJ (8 steps)
- Return to level 3 through CJ (1 step)
- Walk from CJ to RE (8 steps)
- Return to level 2 through RE (1 step)
- Walk from RE to XQ (14 steps)
- Return to level 1 through XQ (1 step)
- Walk from XQ to FD (8 steps)
- Return to level 0 through FD (1 step)
- Walk from FD to ZZ (18 steps)

This path takes a total of 396 steps to move from AA at the outermost layer to
ZZ at the outermost layer.

In your maze, when accounting for recursion, how many steps does it take to get
from the open tile marked AA to the open tile marked ZZ, both at the outermost
layer?

"""

import numpy as np
import networkx as nx
from collections import namedtuple, defaultdict
from colorama import Fore, Back, Style 
from copy import deepcopy
import matplotlib.pyplot as plt
import math
import string
import itertools
from tqdm import tqdm

Point = namedtuple('P', 'x y level')

def get_grid(fname, plot=False, render=True):

    def _get_letter(arr, x, y):
        if x < 0 or y < 0:
            return None
        try:
            if arr[y, x] in string.ascii_uppercase:
                return arr[y, x]
        except IndexError as e:
            return None

        return ' '

    with open(fname, 'r') as f:
        lines = f.readlines()
        lines = [list(l.strip('\n')) for l in lines]

    level = 0

    grid = defaultdict(int)
    
    arr = np.array(lines)

    for y, x in np.ndindex(arr.shape):
        grid[(x,y)] = arr[y,x]

    G = nx.Graph()
    for y, x in np.argwhere(arr == '.'):
        p = Point(x, y, level)
        G.add_node(p, val='') 
        for yp, xp in [(y+1, x  ), (y-1, x  ),
                       (y  , x+1), (y  , x-1)]: 
            try:
                if arr[yp, xp] == '.':
                    G.add_edge(Point(x, y, level), Point(xp, yp, level))
            except IndexError as e:
                pass

        down_letter = _get_letter(arr, x, y+1)
        up_letter = _get_letter(arr, x, y-1)
        left_letter = _get_letter(arr, x-1, y)
        right_letter = _get_letter(arr, x+1, y)
        
        if down_letter not in [None, ' ']:
            G.nodes[p]['val'] = _get_letter(arr, x, y+1) + _get_letter(arr, x, y+2)
            if _get_letter(arr, x, y+3) is None:
                G.nodes[p]['edge'] = 'outer'
            else:
                G.nodes[p]['edge'] = 'inner'
        if up_letter not in [None, ' ']:
            G.nodes[p]['val'] = _get_letter(arr, x, y-2) + _get_letter(arr, x, y-1)
            if _get_letter(arr, x, y-3) is None:
                G.nodes[p]['edge'] = 'outer'
            else:
                G.nodes[p]['edge'] = 'inner'
        if left_letter not in [None, ' ']:
            G.nodes[p]['val'] = _get_letter(arr, x-2, y) + _get_letter(arr, x-1, y)
            if _get_letter(arr, x-3, y) is None:
                G.nodes[p]['edge'] = 'outer'
            else:
                G.nodes[p]['edge'] = 'inner'
        if right_letter not in [None, ' ']:
            G.nodes[p]['val'] = _get_letter(arr, x+1, y) + _get_letter(arr, x+2, y)
            if _get_letter(arr, x+3, y) is None:
                G.nodes[p]['edge'] = 'outer'
            else:
                G.nodes[p]['edge'] = 'inner'

        if 'val' in G.nodes[p] and G.nodes[p]['val'] == 'AA':
            G.graph['starting_node'] = p
        if 'val' in G.nodes[p] and G.nodes[p]['val'] == 'ZZ':
            G.graph['ending_node'] = p

    labels = {n[0] : f'({n[0].x}, {n[0].y})' + (f'\n{n[1]["val"]}' 
                                             if 'val' in n[1] else '') 
                                             for n in G.nodes(data=True)}
    G.graph['labels'] = labels

    if plot:
        nx.draw_kamada_kawai(G, with_labels=True, labels=G.graph['labels']);
        plt.show()

    if render: render_graph(G)

    return G


def add_level(G, level):
    # first, we want to duplicate every node and inter-level
    # edge in the last level at this level:
    nodes_to_add = []
    for p, d in G.nodes(data=True):
        if p.level == level - 1:
            nodes_to_add.append((Point(p.x, p.y, level), d))
    G.add_nodes_from(nodes_to_add)

    for e in G.edges:
        p1, p2 = e
        if p1.level == level-1 and p2.level == level-1:
            # this is a within-level edge, so recreate it on this level
            G.add_edge(Point(p1.x, p1.y, level), 
                       Point(p2.x, p2.y, level))

    # we want to connect inner portals from the previous level
    # to the outer portals in this level

    # Get the previous level's inner portals:
    l0_portals = [(p,d) for p, d in G.nodes(data=True) 
                  if len(d['val']) == 2 and 
                     d['edge'] == 'inner' and 
                     p.level == level-1]
    
    # Get this level's outer portals:
    l1_portals = [(p,d) for p, d in G.nodes(data=True)
                  if len(d['val']) == 2 and
                     d['val'] not in ['AA', 'ZZ'] and
                     d['edge'] == 'outer' and
                     p.level == level]

    # loop through inner portals
    for p0, d0 in l0_portals:
        lett = d0['val']
        # p0 is inner portal from last level
        p_1 = [p1 for p1, d1 in l1_portals if d1['val'] == lett][0]
        # p_1 is outer portal from this level
        G.add_edge(p0, p_1)

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
        output_string += f'{y:03g} '
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

    G = get_grid('20/test_input1', render=False, plot=False)
    G = add_level(G, 1)

    path_length = nx.shortest_path_length(G, 
                                          source=G.graph['starting_node'], 
                                          target=G.graph['ending_node'])
    assert path_length == 26

    G = get_grid('20/test_input3', render=False, plot=False)
    for i in range(1,20):
        G = add_level(G, i)
    
    path_length = nx.shortest_path_length(G, 
                                          source=G.graph['starting_node'], 
                                          target=G.graph['ending_node'])
    assert path_length == 396
    
    G = get_grid('20/input', render=False, plot=False)
    for i in tqdm(range(1,100)):
        G = add_level(G, i)
    
    path_length = nx.shortest_path_length(G, 
                                          source=G.graph['starting_node'], 
                                          target=G.graph['ending_node'])
    print(path_length)

    # Answer is 5966