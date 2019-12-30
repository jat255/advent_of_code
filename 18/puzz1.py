"""
"""
from colorama import Fore, Back, Style 
from copy import deepcopy
import networkx as nx
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import string
from itertools import combinations
import math

def get_grid(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()
        lines = [list(l.strip()) for l in lines]

    grid = defaultdict(lambda: '.')
    
    arr = np.array(lines)

    for y, x in np.ndindex(arr.shape):
        grid[(x,y)] = arr[y,x]

    G = nx.Graph()
    G.graph['keys_held'] = set()
    G.graph['name'] = 'root'

    for y, x in np.argwhere(arr != '#'):
        G.add_node((x, y), val=arr[y,x])
        for yp, xp in [(y+1, x  ), (y-1, x  ),
                       (y  , x+1), (y  , x-1)]: 
            try:
                if arr[yp, xp] != '#':
                    G.add_edge((x, y), (xp, yp))
            except IndexError as e:
                pass
   
    keys = set([i for i in np.unique(arr) if i in string.ascii_lowercase])
    doors = set([i for i in np.unique(arr) if i in string.ascii_uppercase])

    return G, keys, doors

def render_graph(G):

    # G is a networkx graph of positions
    x_max = max([n[0] for n in G.nodes()])
    y_max = max([n[1] for n in G.nodes()])
    
    # add two to account for borders
    arr = np.zeros((y_max + 2, x_max + 2), dtype=str)
    arr[:] = '#'

    for n, d in G.nodes(data=True):
        arr[n[1], n[0]] = d['val']
    
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
    
    # print(output_string, end='')
    # print(f"Keys held: {G.graph['keys_held']}")
    return(output_string)


def tuple_to_string(tup):
    if isinstance(tup, str):
        return tup
    else:
        return f'({tup[0]}, {tup[1]})'

def get_accessible_keys(cur_pos, G):
    for node, (_, doors, keys) in dist_mat[cur_pos].items():
        # doors is a set containing doors in the way, 
        # so compare to G.graph['keys_held']
        if len(doors) == 0 or doors.issubset(G.graph['keys_held']):
            if node == G.graph['starting_node']: pass
            else: 
                if G.graph['key_letter_by_pos'][node].upper() in G.graph['keys_held']: pass
                else:
                    G.graph['accessible_keys'].add(G.graph['key_letter_by_pos'][node])
    return G

# Rather than full-on recursion, what about a while active_searches > 0
# each time a branch occurs, start a new search with a copy of the graph
# (this should likely be OOP designed); collect the results when each branch
# reaches the end, and then find the shortest one

def key_search(cur_pos, G, next_key=None):
    # starting from the starting node, find keys we have access to 
    if 'accessible_keys' not in G.graph:
        G.graph['accessible_keys'] = set()
    if 'total_dist' not in G.graph:
        G.graph['total_dist'] = 0
        G.graph['path'] = [cur_pos]

    global active_searches
    global paths

    # print('Current position:', cur_pos, 
    #       '@' if cur_pos == starting_node else 
    #               G.graph['key_letter_by_pos'][cur_pos])
    
    G = get_accessible_keys(cur_pos, G)
    # print('Accessible keys at start:', G.graph['accessible_keys'])
    if next_key in G.graph['accessible_keys']:
        G.graph['accessible_keys'].discard(next_key)
    # if we have access to more than one, we need to branch
    if len(G.graph['accessible_keys']) > 1:
        render_graph(G)
        # print('More than one key accessible')
        # We don't have a next key to try, so let's pick one and fire it off
        if next_key is None:
            next_key = G.graph['accessible_keys'].pop()
            G.graph['accessible_keys'].add(next_key)
            Gnew = deepcopy(G)
            Gnew.graph['name'] = Gnew.graph['name'] + f'_{next_key}'
            active_searches += 1
            # print(f'Added one to active_searches; now {active_searches}')
            key_search(cur_pos, Gnew, next_key=next_key)
    if len(G.graph['accessible_keys']) < 2 or next_key is not None:
        # when we find a new key, we need to add it to our set of keys_held
        # and update our position
        if len(G.graph['accessible_keys']) == 0:
            G = get_accessible_keys(cur_pos, G)
        if len(G.graph['keys_held']) == len(G.graph['key_letter_by_pos']):
            # print('We\'ve finished since we have all the keys')
            render_graph(G)
            # print('****', G.graph['total_dist'], G.graph['path'])
            # print('****', G.graph['total_dist'], [G.graph['all_letter_by_pos'][p] for p in G.graph['path']])
            if (G.graph['total_dist'], G.graph['path']) not in paths:
                paths.append((G.graph['total_dist'], G.graph['path']))
            active_searches -= 1
            # print(f'Removed one from active_searches; now {active_searches}')
            return cur_pos, G
        else:
            this_key = next_key if next_key else G.graph['accessible_keys'].pop()
            next_pos = G.graph['key_pos_by_letter'][this_key]
            
            G.graph['keys_held'].add(this_key.upper())
            # add any keys to our list that we cross "on the way" to the next key
            keys_to_process = []
            if cur_pos == next_pos:
                pass
            else:
                for k in dist_mat[cur_pos][next_pos][2]:
                    # we want to sort this list of keys by distance from our current
                    # so we add them in the right order
                    k_node = G.graph['key_pos_by_letter'][k]
                    if k_node != cur_pos:  # TODO: put in check for if k is already held
                        if k.upper() not in G.graph['keys_held']:
                            keys_to_process.append((k, dist_mat[cur_pos][k_node][0]))
                    else:
                        pass

            keys_to_process = sorted(keys_to_process, key=lambda x: x[1])

            for k, k_dist in keys_to_process:
                G.graph['keys_held'].add(k.upper())
                k_node = G.graph['key_pos_by_letter'][k]
                G.nodes[k_node]['val'] = '.'
                if k_node not in G.graph['path']:
                    G.graph['path'].append(k_node)

                try:
                    G.nodes[G.graph['door_pos_by_letter'][k.upper()]]['val'] = '.'
                except KeyError as _:
                    pass
            # print('Keys held:', G.graph['keys_held'])
            G.nodes[cur_pos]['val'] = '.'
            if cur_pos == next_pos:
                pass
            else:
                G.graph['total_dist'] += dist_mat[cur_pos][next_pos][0]
            cur_pos = next_pos
            G.graph['path'].append(next_pos)
            G.nodes[cur_pos]['val'] = '@'
            try:
                door_pos = G.graph['door_pos_by_letter'][this_key.upper()]
                G.nodes[door_pos]['val'] = '.'
                render_graph(G)

            except KeyError as _:
                # there is no door for this key, which means we've got them all
                pass
                # return
        
        # if len(G.graph['accessible_keys']) > 0:
        #     return key_search(cur_pos, G, next_key=G.graph['accessible_keys'].pop())
        # else:
        # return key_search(cur_pos, G)
    # print('escaped condition')
    return key_search(cur_pos, G)


if __name__ == '__main__':

    G, keys_needed, doors = get_grid('18/test_input4')
    # print(G.nodes(data=True))
    # render_graph(G)
        
    key_pos_by_letter, door_pos_by_letter = {}, {}
    starting_node = [x for x,y in G.nodes(data=True) if y['val']=='@'][0]
    for k in keys_needed:
        key_pos_by_letter[k] = [x for x,y in 
                                G.nodes(data=True) if y['val']==k][0]
    
    for k in doors:
        door_pos_by_letter[k] = [x for x,y in 
                                 G.nodes(data=True) if y['val']==k][0]
        
    # Invert the door and key dicts so we can lookup by position or letter
    G.graph['door_letter_by_pos'] = dict([[v,k] for k,v in door_pos_by_letter.items()])
    G.graph['key_letter_by_pos'] = dict([[v,k] for k,v in key_pos_by_letter.items()])

    G.graph['door_pos_by_letter'] = door_pos_by_letter
    G.graph['key_pos_by_letter'] = key_pos_by_letter
    del door_pos_by_letter; del key_pos_by_letter
    
    G.graph['all_letter_by_pos'] = deepcopy(G.graph['key_letter_by_pos'])
    G.graph['all_letter_by_pos'][starting_node] = '@'

    # print(key_pos)
    # print(list(nx.bfs_tree(G, starting_node)))

    # dist_mat[from][to] = distance
    # from and to are tuples (node definitions)
    # we want to pre-compute the distance from the starting point and all keys
    # to all other keys (and the starting point)
    # Also includes doors that need to be crossed as second item of tuple
    # and additional keys that are crossed as third item of tuple
    dist_mat = defaultdict(dict)
    froms = [starting_node] + [v for k,v in G.graph['key_pos_by_letter'].items()]
    for _from in froms:
        tos = froms.copy()
        tos.pop(tos.index(_from))
        for _to in tos:
            doors, keys = set(), set()
            path = nx.shortest_path(G, source=_from, target=_to)
            # for each position on the path, check to see if it is a door
            # if it is, add it to our doors set
            for pos in path:
                if pos in G.graph['door_letter_by_pos']:
                    doors.add(G.graph['door_letter_by_pos'][pos])
                if pos in G.graph['key_letter_by_pos']:
                    keys.add(G.graph['key_letter_by_pos'][pos])
            
            # distance is the length of the path node list minus 1
            dist_mat[_from][_to] = (len(path) - 1, doors, keys) 

    paths = []
    # print(dist_mat[starting_node])
    cur_pos = starting_node
    G.graph['starting_node'] = starting_node
    
    active_searches = 1
    key_search(cur_pos, G)
    
    paths = sorted(paths, key=lambda x:x[0])[::-1]

    for p in paths:
        print(p)