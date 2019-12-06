"""
--- Part Two ---
Now, you just need to figure out how many orbital transfers you (YOU) need to
take to get to Santa (SAN).

You start at the object YOU are orbiting; your destination is the object SAN is
orbiting. An orbital transfer lets you move from any object to an object
orbiting or orbited by that object.

For example, suppose you have the following map:

COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN

Visually, the above map of orbits looks like this:

                          YOU
                         /
        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN

In this example, YOU are in orbit around K, and SAN is in orbit around I. To
move from K to I, a minimum of 4 orbital transfers are required:

K to J
J to E
E to D
D to I

Afterward, the map of orbits looks like this:

        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN
                 \
                  YOU

What is the minimum number of orbital transfers required to move from the object
YOU are orbiting to the object SAN is orbiting? (Between the objects they are
orbiting - not between YOU and SAN.) 
"""

import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt

if __name__ == '__main__':

    with open('06/input', 'r') as f:
        lines = f.readlines()

    graph_inp = [tuple(l.strip('\n').split(')')) for l in lines]
    
    G = nx.Graph(graph_inp)

    # subtract two, because the start and end orbits (edges) do not count as
    # jumps 
    ln = nx.shortest_path_length(G, source='YOU', target='SAN') - 2
    
    print(f'Shortest path to Santa is: {ln}')

    # plt.figure(figsize=(16,14))
    # pos =graphviz_layout(G, prog='dot', args="-Grankdir=LR")
    # nx.draw(G, pos, with_labels=True)
    # plt.show()

    # Answer is 313