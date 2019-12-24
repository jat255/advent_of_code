"""
--- Part Two ---
All this drifting around in space makes you wonder about the nature of the
universe. Does history really repeat itself? You're curious whether the moons
will ever return to a previous state.

Determine the number of steps that must occur before all of the moons' positions
and velocities exactly match a previous point in time.

For example, the first example above takes 2772 steps before they exactly match
a previous point in time; it eventually returns to the initial state:

After 0 steps:
pos=<x= -1, y=  0, z=  2>, vel=<x=  0, y=  0, z=  0>
pos=<x=  2, y=-10, z= -7>, vel=<x=  0, y=  0, z=  0>
pos=<x=  4, y= -8, z=  8>, vel=<x=  0, y=  0, z=  0>
pos=<x=  3, y=  5, z= -1>, vel=<x=  0, y=  0, z=  0>

After 2770 steps:
pos=<x=  2, y= -1, z=  1>, vel=<x= -3, y=  2, z=  2>
pos=<x=  3, y= -7, z= -4>, vel=<x=  2, y= -5, z= -6>
pos=<x=  1, y= -7, z=  5>, vel=<x=  0, y= -3, z=  6>
pos=<x=  2, y=  2, z=  0>, vel=<x=  1, y=  6, z= -2>

After 2771 steps:
pos=<x= -1, y=  0, z=  2>, vel=<x= -3, y=  1, z=  1>
pos=<x=  2, y=-10, z= -7>, vel=<x= -1, y= -3, z= -3>
pos=<x=  4, y= -8, z=  8>, vel=<x=  3, y= -1, z=  3>
pos=<x=  3, y=  5, z= -1>, vel=<x=  1, y=  3, z= -1>

After 2772 steps:
pos=<x= -1, y=  0, z=  2>, vel=<x=  0, y=  0, z=  0>
pos=<x=  2, y=-10, z= -7>, vel=<x=  0, y=  0, z=  0>
pos=<x=  4, y= -8, z=  8>, vel=<x=  0, y=  0, z=  0>
pos=<x=  3, y=  5, z= -1>, vel=<x=  0, y=  0, z=  0>

Of course, the universe might last for a very long time before repeating. Here's
a copy of the second example from above:

<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>

This set of initial positions takes 4686774924 steps before it repeats a
previous state! Clearly, you might need to find a more efficient way to simulate
the universe.

How many steps does it take to reach the first state that exactly matches a
previous state?

"""

import itertools
import math

class Moon:
    def __init__(self, name, x, y, z, vel_x=0, vel_y=0, vel_z=0):
        self.name = name

        self.pos = {}
        self.pos['x'] = x
        self.pos['y'] = y
        self.pos['z'] = z

        self.vel = {}
        self.vel['x'] = vel_x
        self.vel['y'] = vel_y
        self.vel['z'] = vel_z

    def update_position(self):
        for ax in ['x', 'y', 'z']:
            self.pos[ax] += self.vel[ax]
    
    def get_potential_energy(self):
        return sum([abs(self.pos[ax]) for ax in ['x', 'y', 'z']])

    def get_kinetic_energy(self):
        return sum([abs(self.vel[ax]) for ax in ['x', 'y', 'z']])

    def __repr__(self):
        return f'{self.name}: pos=<{self.pos["x"]}, ' + \
               f'{self.pos["y"]}, {self.pos["z"]}> ' + \
               f'vel=<{self.vel["x"]}, ' + \
               f'{self.vel["y"]}, {self.vel["z"]}>'


def apply_gravity(moon_1, moon_2):
    # Update the velocities for this pair of moons
    for ax in ['x', 'y', 'z']:
        if moon_1.pos[ax] == moon_2.pos[ax]:
            # velocity does not change if they have same position
            pass
        elif moon_1.pos[ax] < moon_2.pos[ax]:
            # moon_1 is less than moon_2, so add 1 to moon_1 and subtract
            # 1 from moon_2
            moon_1.vel[ax] += 1
            moon_2.vel[ax] -= 1
        elif moon_1.pos[ax] > moon_2.pos[ax]:
            # moon_1 is greater than moon_2, so subtract 1 from moon_1 
            # and add 1 from moon_2
            moon_1.vel[ax] -= 1
            moon_2.vel[ax] += 1


def apply_timestep(moons):
    """
    Apply one step of time by updating velocity and then position for each moon
    in the list provided,

    Parameters
    ----------
    moons : list
        list of moons to process
    """
    for moon_pair in itertools.combinations(moons, 2):
        apply_gravity(*moon_pair)

    for moon in moons:
        moon.update_position()


def get_universe_state(moon_list, ax):
    """
    Get a hashed state of the universe on a given axis, 
    calculated from the moons provided in moon_list

    Returns
    -------
    universe_hash : str
        A hash containing the position and velocity of each moon in the universe
    """
    universe_hash = ''
    for m in moon_list:
        universe_hash += str(m.pos[ax]) + str(m.vel[ax])
    return universe_hash


def apply_sim(moon_list, steps, debug=False):
    for i in range(steps):
        if debug: 
            print(f'After {i} steps:')
            for m in moon_list:
                print(m)
            print('')
        apply_timestep(moon_list)

    if debug:
        # print last step
        print(f'After {i+1} steps:')
        for m in moon_list:
            print(m)
        print('')

    total_en = 0
    for m in moon_list:
        this_pot = m.get_potential_energy()
        this_kin = m.get_kinetic_energy()
        this_tot = this_kin * this_pot
        total_en += this_tot
        if debug: print(f'Pot: {this_pot}, Kin: {this_kin} = Total: {this_tot}')
    if debug: print(f'Sum: {total_en}')

    return total_en


def apply_sim_2(moon_list, debug=False, print_interval=10000):
    iters = 0
    x_hashes = set()
    y_hashes = set()
    z_hashes = set()
    found_x, found_y, found_z = False, False, False

    while True:
        if not found_x: 
            this_x_hash = get_universe_state(moon_list, 'x')            
            if this_x_hash not in x_hashes:
                x_hashes.add(this_x_hash)
            else:
                print(f'x: {iters}')
                x_iters = iters
                found_x = True

        if not found_y: 
            this_y_hash = get_universe_state(moon_list, 'y')
            if this_y_hash not in y_hashes:
                y_hashes.add(this_y_hash)
            else:
                print(f'y: {iters}')
                y_iters = iters
                found_y = True

        if not found_z: 
            this_z_hash = get_universe_state(moon_list, 'z')
            if this_z_hash not in z_hashes:
                z_hashes.add(this_z_hash)
            else:
                print(f'z: {iters}')
                z_iters = iters
                found_z = True     

        if found_x and found_y and found_z:
            interval = lcm3(x_iters, y_iters, z_iters)
            print(str(interval) + '\n')
            return interval


        if debug:
            if iters % print_interval == 0:
                print(f'iters: {iters}')

        apply_timestep(moon_list)
        iters += 1


def lcm2(a, b):
    return int(a * b / math.gcd(int(a), int(b)))

def lcm3(a, b, c):
    return lcm2(a, lcm2(b, c))

if __name__ == '__main__':

    # First test case:
    io =        Moon('Io',      -1,   0,  2)
    europa =    Moon('Europa',   2, -10, -7)
    ganymede =  Moon('Ganymede', 4,  -8,  8)
    callisto =  Moon('Callisto', 3,   5, -1)
    
    moon_list = [io, europa, ganymede, callisto]

    assert apply_sim_2(moon_list, False) == 2772

    # Second test case:
    io = Moon('Io',             -8, -10,  0)
    europa = Moon('Europa',      5,   5, 10)
    ganymede = Moon('Ganymede',  2,  -7,  3)
    callisto = Moon('Callisto',  9,  -8, -3)
    moon_list = [io, europa, ganymede, callisto]

    assert apply_sim_2(moon_list, False) == 4686774924

    # # Actual input:
    io = Moon('Io',              -1,  -4,  0)
    europa = Moon('Europa',       4,   7, -1)
    ganymede = Moon('Ganymede', -14, -10,  9)
    callisto = Moon('Callisto',   1,   2, 17)
    moon_list = [io, europa, ganymede, callisto]

    apply_sim_2(moon_list, False)

    # <x=-1, y=-4, z=0>
    # <x=4, y=7, z=-1>
    # <x=-14, y=-10, z=9>
    # <x=1, y=2, z=17>

    # Answer is 337721412394184
