"""
--- Day 24: Planet of Discord ---
You land on Eris, your last stop before reaching Santa. As soon as you do, your
sensors start picking up strange life forms moving around: Eris is infested with
bugs! With an over 24-hour roundtrip for messages between you and Earth, you'll
have to deal with this problem on your own.

Eris isn't a very large place; a scan of the entire area fits into a 5x5 grid
(your puzzle input). The scan shows bugs (#) and empty spaces (.).

Each minute, The bugs live and die based on the number of bugs in the four
adjacent tiles:

A bug dies (becoming an empty space) unless there is exactly one bug adjacent to
it.

An empty space becomes infested with a bug if exactly one or two bugs are
adjacent to it.

Otherwise, a bug or empty space remains the same. (Tiles on the edges of the
grid have fewer than four adjacent tiles; the missing tiles count as empty
space.) This process happens in every location simultaneously; that is, within
the same minute, the number of adjacent bugs is counted for every tile first,
and then the tiles are updated.

Here are the first few minutes of an example scenario:

Initial state:
....#
#..#.
#..##
..#..
#....

After 1 minute:
#..#.
####.
###.#
##.##
.##..

After 2 minutes:
#####
....#
....#
...#.
#.###

After 3 minutes:
#....
####.
...##
#.##.
.##.#

After 4 minutes:
####.
....#
##..#
.....
##...

To understand the nature of the bugs, watch for the first time a layout of bugs
and empty spaces matches any previous layout. In the example above, the first
layout to appear twice is:

.....
.....
.....
#....
.#...

To calculate the biodiversity rating for this layout, consider each tile
left-to-right in the top row, then left-to-right in the second row, and so on.
Each of these tiles is worth biodiversity points equal to increasing powers of
two: 1, 2, 4, 8, 16, 32, and so on. Add up the biodiversity points for tiles
with bugs; in this example, the 16th tile (32768 points) and 22nd tile (2097152
points) have bugs, a total biodiversity rating of 2129920.

What is the biodiversity rating for the first layout that appears twice?

"""
import numpy as np
from copy import deepcopy

def get_spaces_to_check(grid, x, y):
    """Check 2D array for adjacent spaces"""
    to_check = []

    # one left; make sure there's room to left
    if x-1 >= 0:
        to_check.append((y, x-1))
    # one right; make sure x+1 doesn't overflow
    if x+1 < grid.shape[1]:
        to_check.append((y, x+1))
    # one above:
    if y-1 >= 0:
        to_check.append((y-1, x))
    # one below:
    if y+1 < grid.shape[0]:
        to_check.append((y+1, x))

    return to_check

def process_space(grid, x, y):
    grid = deepcopy(grid)
    # print(f'checking space x={x}, y={y}')
    to_check = get_spaces_to_check(grid, x, y)
    # for t in to_check:
    #     print(f'to_check: x={t[1]}, y={t[0]}')
    sum_around = sum([grid[t[0], t[1]] for t in to_check])
    # print(f'{sum_around} bugs around x={x}, y={y}')

    # process bug
    if grid[y,x] == 1:
        # A bug dies (becoming an empty space) unless there is exactly 
        # one bug adjacent to it (sum == 1).
        if sum_around == 1:
            grid[y, x] = 1
            # print(f'x={x}, y={y} stays bug')
        else:
            grid[y, x] = 0
            # print(f'x={x}, y={y} becomes space')
    
    # process space
    else:
        # An empty space becomes infested with a bug if exactly one or two bugs 
        # are adjacent to it.
        if sum_around == 1 or sum_around == 2:
            grid[y, x] = 1
            # print(f'x={x}, y={y} becomes bug')
        else:
            grid[y, x] = 0
            # print(f'x={x}, y={y} stays space')

    
    return grid[y, x]


def print_grid(grid):
    output_str = ''
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x]:
                output_str += '#'
            else:
                output_str += '.'
        output_str += '\n'
    
    print(output_str)


def get_grid(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
    
    grid = np.zeros((len(lines[0]), len(lines)), dtype=int)

    # 1 is a bug, 0 is empty
    for j, l in enumerate(lines):
        for i, char in enumerate(l):
            grid[j, i] = 0 if char == '.' else 1

    return grid


def process_minute(grid):
    new_grid = np.zeros_like(grid)
    for y, x in np.ndindex(grid.shape):
        new_grid[y, x] = process_space(grid, x, y)
    return new_grid

def get_duplicated_grid(fname):
    grid = get_grid(fname)
    grids_seen = set()
    grids_seen.add(hash(grid.tostring()))
    while True:
        grid = process_minute(grid)
        grid_hash = hash(grid.tostring())
        if grid_hash in grids_seen:
            print(f'Duplicate grid found ({len(grids_seen) + 1}):')
            print_grid(grid)
            return grid
        else:
            grids_seen.add(grid_hash)

def biodiversity_rating(grid):
    i = 0 
    biodiv = 0
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y,x]:
                biodiv += 2**i
            i += 1
    
    return biodiv

if __name__ == '__main__':

    grid = get_duplicated_grid('24/test_input')
    assert biodiversity_rating(grid) == 2129920

    grid = get_duplicated_grid('24/input')
    print(biodiversity_rating(grid))

    # Answer is 32509983



    