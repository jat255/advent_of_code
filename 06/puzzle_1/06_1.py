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
import scipy.spatial.distance as spd
from string import ascii_uppercase

if __name__ == '__main__':

    is_test = True

    if is_test:
        inp = np.loadtxt('test_input', delimiter=',', dtype=int)
    else:
        inp = np.loadtxt('input', delimiter=',', dtype=int)

    dist_mat = np.zeros((inp[:, 1].max() + 2, inp[:, 0].max() + 2,
                         len(inp)), dtype=int)

    print(dist_mat.shape)

    # print(inp)
    # print(inp.shape)
    # print()

    if is_test:
        pos_list = [' {}'.format(a) for a in ascii_uppercase]
    else:
        pos_list = [' {}'.format(a) for a in ascii_uppercase]
        pos_list += ['{}{}'.format(a, a) for a in ascii_uppercase]

    for i, pos in enumerate(inp):
        print(i, pos, pos_list[i])

        a = dist_mat[:, :, i]

        it = np.nditer(a, flags=['multi_index'])
        while not it.finished:
            this_point = it.multi_index[0], it.multi_index[1]
            a[this_point] = int(spd.cityblock(this_point, pos))
            it.iternext()

    res = np.zeros_like(dist_mat[:,:,0], dtype='|U2')
    a = dist_mat[:, :, 0]
    it = np.nditer(a, flags=['multi_index'])
    while not it.finished:
        this_point = it.multi_index[0], it.multi_index[1]
        dist_row = dist_mat[this_point]
        this_min = dist_row.min()
        this_argmin = dist_row.argmin()
        min_matches = np.where(dist_row == this_min)[0]
        # print(len(min_matches), min_matches)
        # Multiple points were at minimum distance
        if len(min_matches) > 1:
            res[this_point] = '..'
        else:
            res[this_point] = pos_list[this_argmin].lower()
        it.iternext()

    for i, pos in enumerate(inp):
        print(pos, pos_list[i])
        res[pos[0],pos[1]] = pos_list[i]

    print(res.T)
    unique, counts = np.unique(np.char.upper(res), return_counts=True)
    print(dict(zip(unique, counts)))
