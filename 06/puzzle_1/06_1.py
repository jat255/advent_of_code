"""
--- Day 6: Chronal Coordinates ---
The device on your wrist beeps several times, and once again you feel like
you're falling.

"Situation critical," the device announces. "Destination indeterminate.
Chronal interference detected. Please specify new target coordinates."

The device then produces a list of coordinates (your puzzle input). Are they
places it thinks are safe or dangerous? It recommends you check manual page
729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the
coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate
by counting the number of integer X,Y locations that are closest to that
coordinate (and aren't tied in distance to any other coordinate).

Your goal is to find the size of the largest area that isn't infinite. For
example, consider the following list of coordinates:

1, 1
1, 6
8, 3
3, 4
5, 5
8, 9

If we name these coordinates A through F, we can draw them on a grid, putting
0,0 at the top left:
..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.

This view is partial - the actual grid extends infinitely in all directions.
Using the Manhattan distance, each location's closest coordinate can be
determined, shown here in lowercase:

aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf

Locations shown as . are equally far from two or more coordinates, and so they
don't count as being closest to any.

In this example, the areas of coordinates A, B, C, and F are infinite - while
not shown here, their areas extend forever outside the visible grid.
However, the areas of coordinates D and E are finite: D is closest to 9
locations, and E is closest to 17 (both including the coordinate's location
itself). Therefore, in this example, the size of the largest area is 17.

What is the size of the largest area that isn't infinite?
"""

import numpy as np
import scipy as sp
from string import ascii_uppercase

if __name__ == '__main__':

    is_test = True

    if is_test:
        inp = np.loadtxt('test_input', delimiter=',', dtype=int)
    else:
        inp = np.loadtxt('input', delimiter=',', dtype=int)

    blank_cell = '  '
    dist_mat = np.full((inp[:, 1].max() + 2, inp[:, 0].max() + 2), blank_cell)

    # print(dist_mat)

    # print(inp)
    # print(inp.shape)
    # print()

    if is_test:
        pos_list = [' {}'.format(a) for a in ascii_uppercase]
    else:
        pos_list = [' {}'.format(a) for a in ascii_uppercase]
        pos_list += ['{}{}'.format(a, a) for a in ascii_uppercase]

    # print(pos_list)
    for i, (y, x) in enumerate(inp):
        # print(i, x, y, pos_list[i])
        dist_mat[x, y] = pos_list[i]
        # dist_mat[0, 0] = ' A'
        # dist_mat[5, 5] = ' B'
        # dist_mat[7, 7] = ' C'
        # dist_mat[3, 6] = ' C'

    dist = 1
    while blank_cell in dist_mat:
        for p in pos_list[:10]:
            print()
            print(p)

            locs = np.where(np.logical_or(dist_mat == p, dist_mat ==
                                          p.lower()))
            locs = np.vstack(locs).T

            for ii, (yi, xi) in enumerate(locs):
                to_change = [(yi + dist, xi),
                             (yi, xi + dist),
                             (yi - dist, xi),
                             (yi, xi - dist)]
                for p_to_change in to_change:
                    try:
                        current_val = dist_mat[p_to_change]
                        print('{}, value: "{}"'.format(
                            p_to_change,
                            current_val))
                        if p_to_change[0] < 0 or p_to_change[1] < 0:
                            # Don't set any negative values
                            continue
                        if current_val == blank_cell:
                            dist_mat[p_to_change] = p.lower()
                        elif current_val == p.lower() or current_val == p:
                            pass
                        else:
                            dist_mat[p_to_change] = '..'
                    except IndexError:
                        pass

    print(dist_mat)
