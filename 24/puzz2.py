"""
--- Part Two ---
After careful analysis, one thing is certain: you have no idea where all these
bugs are coming from.

Then, you remember: Eris is an old Plutonian settlement! Clearly, the bugs are
coming from recursively-folded space.

This 5x5 grid is only one level in an infinite number of recursion levels. The
tile in the middle of the grid is actually another 5x5 grid, the grid in your
scan is contained as the middle tile of a larger 5x5 grid, and so on. Two levels
of grids look like this:

     |     |         |     |     
     |     |         |     |     
     |     |         |     |     
-----+-----+---------+-----+-----
     |     |         |     |     
     |     |         |     |     
     |     |         |     |     
-----+-----+---------+-----+-----
     |     | | | | | |     |     
     |     |-+-+-+-+-|     |     
     |     | | | | | |     |     
     |     |-+-+-+-+-|     |     
     |     | | |?| | |     |     
     |     |-+-+-+-+-|     |     
     |     | | | | | |     |     
     |     |-+-+-+-+-|     |     
     |     | | | | | |     |     
-----+-----+---------+-----+-----
     |     |         |     |     
     |     |         |     |     
     |     |         |     |     
-----+-----+---------+-----+-----
     |     |         |     |     
     |     |         |     |     
     |     |         |     |     

(To save space, some of the tiles are not drawn to scale.) Remember, this is
only a small part of the infinitely recursive grid; there is a 5x5 grid that
contains this diagram, and a 5x5 grid that contains that one, and so on. Also,
the ? in the diagram contains another 5x5 grid, which itself contains another
5x5 grid, and so on.

The scan you took (your puzzle input) shows where the bugs are on a single level
of this structure. The middle tile of your scan is empty to accommodate the
recursive grids within it. Initially, no other levels contain bugs.

Tiles still count as adjacent if they are directly up, down, left, or right of a
given tile. Some tiles have adjacent tiles at a recursion level above or below
its own level. For example:

     |     |         |     |     
  1  |  2  |    3    |  4  |  5  
     |     |         |     |     
-----+-----+---------+-----+-----
     |     |         |     |     
  6  |  7  |    8    |  9  |  10 
     |     |         |     |     
-----+-----+---------+-----+-----
     |     |A|B|C|D|E|     |     
     |     |-+-+-+-+-|     |     
     |     |F|G|H|I|J|     |     
     |     |-+-+-+-+-|     |     
 11  | 12  |K|L|?|N|O|  14 |  15 
     |     |-+-+-+-+-|     |     
     |     |P|Q|R|S|T|     |     
     |     |-+-+-+-+-|     |     
     |     |U|V|W|X|Y|     |     
-----+-----+---------+-----+-----
     |     |         |     |     
 16  | 17  |    18   |  19 |  20 
     |     |         |     |     
-----+-----+---------+-----+-----
     |     |         |     |     
 21  | 22  |    23   |  24 |  25 
     |     |         |     |     

- Tile 19 has four adjacent tiles: 14, 18, 20, and 24.
- Tile G has four adjacent tiles: B, F, H, and L.
- Tile D has four adjacent tiles: 8, C, E, and I.
- Tile E has four adjacent tiles: 8, D, 14, and J.
- Tile 14 has eight adjacent tiles: 9, E, J, O, T, Y, 15, and 19.
- Tile N has eight adjacent tiles: I, O, S, and five tiles within the sub-grid
  marked ?.

The rules about bugs living and dying are the same as before.

For example, consider the same initial state as above:

....#
#..#.
#.?##
..#..
#....

The center tile is drawn as ? to indicate the next recursive grid. Call this
level 0; the grid within this one is level 1, and the grid that contains this
one is level -1. Then, after ten minutes, the grid at each level would look like
this:

Depth -5:
..#..
.#.#.
..?.#
.#.#.
x..#..

Depth -4:
...#.
...##
..?..
...##
...#.

Depth -3:
#.#..
.#...
..?..
.#...
#.#..

Depth -2:
.#.##
....#
..?.#
...##
.###.

Depth -1:
#..##
...##
..?..
...#.
.####

Depth 0:
.#...
.#.##
.#?..
.....
.....

Depth 1:
.##..
#..##
..?.#
##.##
#####

Depth 2:
###..
##.#.
#.?..
.#.##
#.#..

Depth 3:
..###
.....
#.?..
#....
#...#

Depth 4:
.###.
#..#.
#.?..
##.#.
.....

Depth 5:
####.
#..#.
#.?#.
####.
.....

In this example, after 10 minutes, a total of 99 bugs are present.

Starting with your scan, how many bugs are present after 200 minutes?
"""
from tqdm import tqdm
import numpy as np
from copy import deepcopy

def get_spaces_to_check(grid, x, y, z):
    """
    Check 2D array for adjacent spaces
    Position 2 is the center space, which is recursive
    """
    to_check = []

    # check non-recursive spaces first
    # one left; make sure there's room to left
    if x-1 >= 0 and (y, x-1) != (2, 2):
        to_check.append((y, x-1, z))
    # one right; make sure x+1 doesn't overflow
    if x+1 < grid.shape[1] and (y, x+1) != (2, 2):
        to_check.append((y, x+1, z))
    # one above:
    if y-1 >= 0 and (y-1, x) != (2, 2):
        to_check.append((y-1, x, z))
    # one below:
    if y+1 < grid.shape[0] and (y+1, x) != (2,2):
        to_check.append((y+1, x, z))

    if z < grid.shape[2] - 1:
        # handle recursion into middle (z + 1)
        if y == 2 and x-1 == 2:        # left
            for i in range(5):
                to_check.append((i, 4, z+1))
        if y == 2 and x+1 == 2:        # right
            for i in range(5):
                to_check.append((i, 0, z+1))
        if x == 2 and y-1 == 2:        # up
            for i in range(5):
                to_check.append((4, i, z+1))
        if x == 2 and y+1 == 2:        # down
            for i in range(5):
                to_check.append((0, i, z+1))

    # handle recursion on outsides (z - 1)
    if z > 0:
        if x-1 < 0:                  # left
            to_check.append((2, 1, z-1))
        if x+1 >= grid.shape[1]:     # right
            to_check.append((2, 3, z-1))
        if y-1 < 0:                  # up
            to_check.append((1, 2, z-1))
        if y+1 >= grid.shape[0]:     # down
            to_check.append((3, 2, z-1))

    return to_check

def process_space(grid, x, y, z):
    grid = deepcopy(grid)
    # print(f'checking space x={x}, y={y}')
    to_check = get_spaces_to_check(grid, x, y, z)
    # for t in to_check:
    #     print(f'to_check: x={t[1]}, y={t[0]}')
    sum_around = sum([grid[t[0], t[1], t[2]] for t in to_check])
    # print(f'{sum_around} bugs around x={x}, y={y}')

    # process bug
    if grid[y,x,z] == 1:
        # A bug dies (becoming an empty space) unless there is exactly 
        # one bug adjacent to it (sum == 1).
        if sum_around == 1:
            grid[y, x, z] = 1
            # print(f'x={x}, y={y} stays bug')
        else:
            grid[y, x, z] = 0
            # print(f'x={x}, y={y} becomes space')
    
    # process space
    else:
        # An empty space becomes infested with a bug if exactly one or two bugs 
        # are adjacent to it.
        if sum_around == 1 or sum_around == 2:
            grid[y, x, z] = 1
            # print(f'x={x}, y={y} becomes bug')
        else:
            grid[y, x, z] = 0
            # print(f'x={x}, y={y} stays space')

    
    return grid[y, x, z]


def print_grid(grid):
    
    output_str = ''
    if len(grid.shape) == 2:
        for y in range(grid.shape[0]):
            for x in range(grid.shape[1]):
                if x == 2 and y == 2:
                    output_str += '?'
                    continue
                if grid[y, x]:
                    output_str += '#'
                else:
                    output_str += '.'
            output_str += '\n'
    
    elif len(grid.shape) == 3:
        for z in range(grid.shape[2]):
            print(f'Depth {z-grid.shape[2]//2}:')
            print_grid(grid[:,:,z])
        output_str += '\n'
    print(output_str)


def get_grid(fname, time_steps=0):
    with open(fname, 'r') as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
    
    grid = np.zeros((len(lines[0]), len(lines)), dtype=int)
    grid_2d_zeros = deepcopy(grid)

    # 1 is a bug, 0 is empty
    for j, l in enumerate(lines):
        for i, char in enumerate(l):
            grid[j, i] = 0 if char == '.' else 1

    for i in range(time_steps//2):
        grid = np.dstack((grid, grid_2d_zeros))
        grid = np.dstack((grid_2d_zeros, grid))

    return grid


def process_minute(grid):
    new_grid = np.zeros_like(grid)
    for y, x, z in np.ndindex(grid.shape):
        if x == 2 and y == 2:
            continue
        new_grid[y, x, z] = process_space(grid, x, y, z)
    return new_grid


def process_minutes(grid, minutes):
    for i in tqdm(range(minutes)):
        grid = process_minute(grid)
    return grid


if __name__ == '__main__':

    grid = get_grid('24/test_input', 10)
    grid = process_minutes(grid, 10)
    assert grid.sum() == 99

    grid = get_grid('24/input', 200)
    grid = process_minutes(grid, 200)
    print(grid.sum())

    # Answer is 32509983



    