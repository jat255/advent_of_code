"""
--- Part Two ---
Once you give them the coordinates, the Elves quickly deploy an Instant
Monitoring Station to the location and discover the worst: there are simply too
many asteroids.

The only solution is complete vaporization by giant laser.

Fortunately, in addition to an asteroid scanner, the new monitoring station also
comes equipped with a giant rotating laser perfect for vaporizing asteroids. The
laser starts by pointing up and always rotates clockwise, vaporizing any
asteroid it hits.

If multiple asteroids are exactly in line with the station, the laser only has
enough power to vaporize one of them before continuing its rotation. In other
words, the same asteroids that can be detected can be vaporized, but if
vaporizing one asteroid makes another one detectable, the newly-detected
asteroid won't be vaporized until the laser has returned to the same position by
rotating a full 360 degrees.

For example, consider the following map, where the asteroid with the new
monitoring station (and laser) is marked X:

.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....X...###..
..#.#.....#....##

The first nine asteroids to get vaporized, in order, would be:

.#....###24...#..
##...##.13#67..9#
##...#...5.8####.
..#.....X...###..
..#.#.....#....##

Note that some asteroids (the ones behind the asteroids marked 1, 5, and 7)
won't have a chance to be vaporized until the next full rotation. The laser
continues rotating; the next nine to be vaporized are:

.#....###.....#..
##...##...#.....#
##...#......1234.
..#.....X...5##..
..#.9.....8....76

The next nine to be vaporized are then:

.8....###.....#..
56...9#...#.....#
34...7...........
..2.....X....##..
..1..............

Finally, the laser completes its first full rotation (1 through 3), a second
rotation (4 through 8), and vaporizes the last asteroid (9) partway through its
third rotation:

......234.....6..
......1...5.....7
.................
........X....89..
.................

In the large example above (the one with the best monitoring station location at
11,13):

- The 1st asteroid to be vaporized is at 11,12.
- The 2nd asteroid to be vaporized is at 12,1.
- The 3rd asteroid to be vaporized is at 12,2.
- The 10th asteroid to be vaporized is at 12,8.
- The 20th asteroid to be vaporized is at 16,0.
- The 50th asteroid to be vaporized is at 16,9.
- The 100th asteroid to be vaporized is at 10,16.
- The 199th asteroid to be vaporized is at 9,6.
- The 200th asteroid to be vaporized is at 8,2.
- The 201st asteroid to be vaporized is at 10,9.
- The 299th and final asteroid to be vaporized is at 11,1.

The Elves are placing bets on which will be the 200th asteroid to be vaporized.
Win the bet by determining which asteroid that will be; what do you get if you
multiply its X coordinate by 100 and then add its Y coordinate? (For example,
8,2 becomes 802.)

"""

import numpy as np
import math

def load_map(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()
    
    list_of_lines = [list(l.strip()) for l in lines]

    # return 
    return np.array(list_of_lines)

def gcd(vec):
    """
    Get greatest common denominator of a length two vector
    """
    x, y = vec
    return math.gcd(x, y)

def get_max_observable(fname):
    arr = load_map(fname)
    ast_locs = np.argwhere(arr == '#')
    max_loc = []
    max_visible = 0
    for i, loc in enumerate(ast_locs):
        other_asts = np.delete(ast_locs, i, axis=0)
        dxdy = [oa - loc for oa in other_asts]
        reduced_dxdy = [d//gcd(d) for d in dxdy]
        unique = []
        for r in reduced_dxdy:
            if tuple(r) not in unique: unique.append(tuple(r))
        if len(unique) > max_visible:
            max_loc = loc
            max_visible = len(unique)

    return max_loc

def vaporize(fname, loc):
    arr = load_map(fname)
    ast_locs = np.argwhere(arr == '#')
    this_ast_index = np.where(np.all(ast_locs == loc, axis=1))[0][0]
    
    other_asts = np.delete(ast_locs, this_ast_index, axis=0)
    dxdy = other_asts - loc
    dists = np.linalg.norm(dxdy, axis=1)

    # tan(theta) = dy/dx, so arctan(dy/dx) = theta
    angles = np.arctan2(dxdy[:,1], dxdy[:,0])
    
    sorted_indices = np.argsort(angles)[::-1]
    sorted_angles = np.rad2deg(angles[sorted_indices])
    sorted_dxdy = dxdy[sorted_indices]
    sorted_other_asts = other_asts[sorted_indices]
    sorted_dists = dists[sorted_indices]

    i = 0
    asts_vaporized = []
    while True:
        cur_angle = sorted_angles[i]
        max_ind_at_this_angle = np.where(sorted_angles == cur_angle)[0].max()  
        # get closest (by distance asteroid at this angle)
        closest_ast_ind = np.argmin(np.where(sorted_angles == cur_angle, 
                                            sorted_dists, 
                                            np.inf))

        asts_vaporized.append(sorted_other_asts[closest_ast_ind])

        sorted_dxdy = np.delete(sorted_dxdy, closest_ast_ind, axis=0)
        sorted_other_asts = np.delete(sorted_other_asts, closest_ast_ind, 
                                      axis=0)
        sorted_dists = np.delete(sorted_dists, closest_ast_ind, axis=0)
        sorted_angles = np.delete(sorted_angles, closest_ast_ind, axis=0)
        
        i = max_ind_at_this_angle

        if i >= len(sorted_angles):
            i = 0
        
        if len(sorted_angles) == 0:
            break

    return asts_vaporized

if __name__ == '__main__':

    loc = get_max_observable('10/test_input5')

    vapor_list = vaporize('10/test_input5', loc)
    assert tuple(vapor_list[0]) == (12, 11)
    assert tuple(vapor_list[1]) == (1, 12)
    assert tuple(vapor_list[2]) == (2, 12)
    assert tuple(vapor_list[9]) == (8, 12)
    assert tuple(vapor_list[19]) == (0, 16)
    assert tuple(vapor_list[49]) == (9, 16)
    assert tuple(vapor_list[99]) == (16, 10)
    assert tuple(vapor_list[198]) == (6, 9)
    assert tuple(vapor_list[199]) == (2, 8)
    assert tuple(vapor_list[200]) == (9, 10)
    assert tuple(vapor_list[298]) == (1, 11)
    
    loc = get_max_observable('10/input')
    vapor_list = vaporize('10/input', loc)

    print(tuple(vapor_list[199])[0] + tuple(vapor_list[199])[1] * 100)

    # Answer is 404
