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
from tqdm import tqdm

if __name__ == '__main__':

    is_test = False

    if is_test:
        inp = np.loadtxt('test_input', delimiter=',', dtype=int)
    else:
        inp = np.loadtxt('input', delimiter=',', dtype=int)

    dist_mat = np.zeros((inp[:, 0].max()+1, inp[:, 1].max()+1), dtype='|U2')
    res = dist_mat.copy()

    print(dist_mat.shape)

    if is_test:
        pos_list = [' {}'.format(a) for a in ascii_uppercase]
    else:
        pos_list = [' {}'.format(a) for a in ascii_uppercase]
        pos_list += ['{}{}'.format(a, a) for a in ascii_uppercase]

    it = np.nditer(dist_mat, flags=['multi_index'])
    print(dist_mat.size)
    t = tqdm(total=dist_mat.size)
    while not it.finished:
        this_point = it.multi_index[0], it.multi_index[1]
        t.set_description('{}, {}'.format(*this_point))

        # For each point, find the closest point in the input list:
        # print()
        # print(this_point)
        dist_list = []
        for pos in inp:
            dist = spd.cityblock(this_point, pos)
            # print(pos, 'distance is:', dist)
            dist_list.append(dist)
        # print('distance list:', dist_list)
        min_val = np.array(dist_list).min()
        min_pos = np.array(dist_list).argmin()
        # print('Min dist is {} at position {}'.format(min_val, min_pos))
        min_positions = np.where(np.array(dist_list) == min_val)[0]
        # print(min_positions)
        if len(min_positions) > 1:
            val = '..'
        else:
            if min_val == 0:
                val = pos_list[min_pos]
            else:
                val = pos_list[min_pos].lower()
        # print(val)
        res[this_point] = val
        t.update()
        it.iternext()
    t.close()
    res = res.T

    print(res)
    print()
    inf_values = np.unique(np.char.upper(np.hstack((res[0, :], res[-1, :],
                                                    res[:, 0], res[:, -1]))))
    print(inf_values)
    unique, counts = np.unique(np.char.upper(res), return_counts=True)
    counted_results = dict(zip(unique, counts))
    for v in inf_values:
        del counted_results[v]

    final_res = sorted(counted_results.items(), key=lambda k: k[1],
                       reverse=True)
    print()
    print("Largest section is{} with area of {}".format(final_res[0][0],
                                                         final_res[0][1]))
