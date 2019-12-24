"""
--- Day 12: The N-Body Problem ---
The space near Jupiter is not a very safe place; you need to be careful of a big
distracting red spot, extreme radiation, and a whole lot of moons swirling
around. You decide to start by tracking the four largest moons: Io, Europa,
Ganymede, and Callisto.

After a brief scan, you calculate the position of each moon (your puzzle input).
You just need to simulate their motion so you can avoid them.

Each moon has a 3-dimensional position (x, y, and z) and a 3-dimensional
velocity. The position of each moon is given in your scan; the x, y, and z
velocity of each moon starts at 0.

Simulate the motion of the moons in time steps. Within each time step, first
update the velocity of every moon by applying gravity. Then, once all moons'
velocities have been updated, update the position of every moon by applying
velocity. Time progresses by one step once all of the positions are updated.

To apply gravity, consider every pair of moons. On each axis (x, y, and z), the
velocity of each moon changes by exactly +1 or -1 to pull the moons together.
For example, if Ganymede has an x position of 3, and Callisto has a x position
of 5, then Ganymede's x velocity changes by +1 (because 5 > 3) and Callisto's x
velocity changes by -1 (because 3 < 5). However, if the positions on a given
axis are the same, the velocity on that axis does not change for that pair of
moons.

Once all gravity has been applied, apply velocity: simply add the velocity of
each moon to its own position. For example, if Europa has a position of x=1,
y=2, z=3 and a velocity of x=-2, y=0,z=3, then its new position would be x=-1,
y=2, z=6. This process does not modify the velocity of any moon.

For example, suppose your scan reveals the following positions:

<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>

Simulating the motion of these moons would produce the following:

After 0 steps:
pos=<x=-1, y=  0, z= 2>, vel=<x= 0, y= 0, z= 0>
pos=<x= 2, y=-10, z=-7>, vel=<x= 0, y= 0, z= 0>
pos=<x= 4, y= -8, z= 8>, vel=<x= 0, y= 0, z= 0>
pos=<x= 3, y=  5, z=-1>, vel=<x= 0, y= 0, z= 0>

After 1 step:
pos=<x= 2, y=-1, z= 1>, vel=<x= 3, y=-1, z=-1>
pos=<x= 3, y=-7, z=-4>, vel=<x= 1, y= 3, z= 3>
pos=<x= 1, y=-7, z= 5>, vel=<x=-3, y= 1, z=-3>
pos=<x= 2, y= 2, z= 0>, vel=<x=-1, y=-3, z= 1>

After 2 steps:
pos=<x= 5, y=-3, z=-1>, vel=<x= 3, y=-2, z=-2>
pos=<x= 1, y=-2, z= 2>, vel=<x=-2, y= 5, z= 6>
pos=<x= 1, y=-4, z=-1>, vel=<x= 0, y= 3, z=-6>
pos=<x= 1, y=-4, z= 2>, vel=<x=-1, y=-6, z= 2>

After 3 steps:
pos=<x= 5, y=-6, z=-1>, vel=<x= 0, y=-3, z= 0>
pos=<x= 0, y= 0, z= 6>, vel=<x=-1, y= 2, z= 4>
pos=<x= 2, y= 1, z=-5>, vel=<x= 1, y= 5, z=-4>
pos=<x= 1, y=-8, z= 2>, vel=<x= 0, y=-4, z= 0>

After 4 steps:
pos=<x= 2, y=-8, z= 0>, vel=<x=-3, y=-2, z= 1>
pos=<x= 2, y= 1, z= 7>, vel=<x= 2, y= 1, z= 1>
pos=<x= 2, y= 3, z=-6>, vel=<x= 0, y= 2, z=-1>
pos=<x= 2, y=-9, z= 1>, vel=<x= 1, y=-1, z=-1>

After 5 steps:
pos=<x=-1, y=-9, z= 2>, vel=<x=-3, y=-1, z= 2>
pos=<x= 4, y= 1, z= 5>, vel=<x= 2, y= 0, z=-2>
pos=<x= 2, y= 2, z=-4>, vel=<x= 0, y=-1, z= 2>
pos=<x= 3, y=-7, z=-1>, vel=<x= 1, y= 2, z=-2>

After 6 steps:
pos=<x=-1, y=-7, z= 3>, vel=<x= 0, y= 2, z= 1>
pos=<x= 3, y= 0, z= 0>, vel=<x=-1, y=-1, z=-5>
pos=<x= 3, y=-2, z= 1>, vel=<x= 1, y=-4, z= 5>
pos=<x= 3, y=-4, z=-2>, vel=<x= 0, y= 3, z=-1>

After 7 steps:
pos=<x= 2, y=-2, z= 1>, vel=<x= 3, y= 5, z=-2>
pos=<x= 1, y=-4, z=-4>, vel=<x=-2, y=-4, z=-4>
pos=<x= 3, y=-7, z= 5>, vel=<x= 0, y=-5, z= 4>
pos=<x= 2, y= 0, z= 0>, vel=<x=-1, y= 4, z= 2>

After 8 steps:
pos=<x= 5, y= 2, z=-2>, vel=<x= 3, y= 4, z=-3>
pos=<x= 2, y=-7, z=-5>, vel=<x= 1, y=-3, z=-1>
pos=<x= 0, y=-9, z= 6>, vel=<x=-3, y=-2, z= 1>
pos=<x= 1, y= 1, z= 3>, vel=<x=-1, y= 1, z= 3>

After 9 steps:
pos=<x= 5, y= 3, z=-4>, vel=<x= 0, y= 1, z=-2>
pos=<x= 2, y=-9, z=-3>, vel=<x= 0, y=-2, z= 2>
pos=<x= 0, y=-8, z= 4>, vel=<x= 0, y= 1, z=-2>
pos=<x= 1, y= 1, z= 5>, vel=<x= 0, y= 0, z= 2>

After 10 steps:
pos=<x= 2, y= 1, z=-3>, vel=<x=-3, y=-2, z= 1>
pos=<x= 1, y=-8, z= 0>, vel=<x=-1, y= 1, z= 3>
pos=<x= 3, y=-6, z= 1>, vel=<x= 3, y= 2, z=-3>
pos=<x= 2, y= 0, z= 4>, vel=<x= 1, y=-1, z=-1>

Then, it might help to calculate the total energy in the system. The total
energy for a single moon is its potential energy multiplied by its kinetic
energy. A moon's potential energy is the sum of the absolute values of its x, y,
and z position coordinates. A moon's kinetic energy is the sum of the absolute
values of its velocity coordinates. Below, each line shows the calculations for
a moon's potential energy (pot), kinetic energy (kin), and total energy:

Energy after 10 steps:

pot: 2 + 1 + 3 =  6;   kin: 3 + 2 + 1 = 6;   total:  6 * 6 = 36
pot: 1 + 8 + 0 =  9;   kin: 1 + 1 + 3 = 5;   total:  9 * 5 = 45
pot: 3 + 6 + 1 = 10;   kin: 3 + 2 + 3 = 8;   total: 10 * 8 = 80
pot: 2 + 0 + 4 =  6;   kin: 1 + 1 + 1 = 3;   total:  6 * 3 = 18

Sum of total energy: 36 + 45 + 80 + 18 = 179

In the above example, adding together the total energy for all moons after 10
steps produces the total energy in the system, 179.

Here's a second example:

<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>

Every ten steps of simulation for 100 steps produces:

After 0 steps:

pos=<x= -8, y=-10, z=  0>, vel=<x=  0, y=  0, z=  0>
pos=<x=  5, y=  5, z= 10>, vel=<x=  0, y=  0, z=  0>
pos=<x=  2, y= -7, z=  3>, vel=<x=  0, y=  0, z=  0>
pos=<x=  9, y= -8, z= -3>, vel=<x=  0, y=  0, z=  0>

After 10 steps:

pos=<x= -9, y=-10, z=  1>, vel=<x= -2, y= -2, z= -1>
pos=<x=  4, y= 10, z=  9>, vel=<x= -3, y=  7, z= -2>
pos=<x=  8, y=-10, z= -3>, vel=<x=  5, y= -1, z= -2>
pos=<x=  5, y=-10, z=  3>, vel=<x=  0, y= -4, z=  5>

After 20 steps:

pos=<x=-10, y=  3, z= -4>, vel=<x= -5, y=  2, z=  0>
pos=<x=  5, y=-25, z=  6>, vel=<x=  1, y=  1, z= -4>
pos=<x= 13, y=  1, z=  1>, vel=<x=  5, y= -2, z=  2>
pos=<x=  0, y=  1, z=  7>, vel=<x= -1, y= -1, z=  2>

After 30 steps:

pos=<x= 15, y= -6, z= -9>, vel=<x= -5, y=  4, z=  0>
pos=<x= -4, y=-11, z=  3>, vel=<x= -3, y=-10, z=  0>
pos=<x=  0, y= -1, z= 11>, vel=<x=  7, y=  4, z=  3>
pos=<x= -3, y= -2, z=  5>, vel=<x=  1, y=  2, z= -3>

After 40 steps:

pos=<x= 14, y=-12, z= -4>, vel=<x= 11, y=  3, z=  0>
pos=<x= -1, y= 18, z=  8>, vel=<x= -5, y=  2, z=  3>
pos=<x= -5, y=-14, z=  8>, vel=<x=  1, y= -2, z=  0>
pos=<x=  0, y=-12, z= -2>, vel=<x= -7, y= -3, z= -3>

After 50 steps:

pos=<x=-23, y=  4, z=  1>, vel=<x= -7, y= -1, z=  2>
pos=<x= 20, y=-31, z= 13>, vel=<x=  5, y=  3, z=  4>
pos=<x= -4, y=  6, z=  1>, vel=<x= -1, y=  1, z= -3>
pos=<x= 15, y=  1, z= -5>, vel=<x=  3, y= -3, z= -3>

After 60 steps:

pos=<x= 36, y=-10, z=  6>, vel=<x=  5, y=  0, z=  3>
pos=<x=-18, y= 10, z=  9>, vel=<x= -3, y= -7, z=  5>
pos=<x=  8, y=-12, z= -3>, vel=<x= -2, y=  1, z= -7>
pos=<x=-18, y= -8, z= -2>, vel=<x=  0, y=  6, z= -1>

After 70 steps:

pos=<x=-33, y= -6, z=  5>, vel=<x= -5, y= -4, z=  7>
pos=<x= 13, y= -9, z=  2>, vel=<x= -2, y= 11, z=  3>
pos=<x= 11, y= -8, z=  2>, vel=<x=  8, y= -6, z= -7>
pos=<x= 17, y=  3, z=  1>, vel=<x= -1, y= -1, z= -3>

After 80 steps:

pos=<x= 30, y= -8, z=  3>, vel=<x=  3, y=  3, z=  0>
pos=<x= -2, y= -4, z=  0>, vel=<x=  4, y=-13, z=  2>
pos=<x=-18, y= -7, z= 15>, vel=<x= -8, y=  2, z= -2>
pos=<x= -2, y= -1, z= -8>, vel=<x=  1, y=  8, z=  0>

After 90 steps:

pos=<x=-25, y= -1, z=  4>, vel=<x=  1, y= -3, z=  4>
pos=<x=  2, y= -9, z=  0>, vel=<x= -3, y= 13, z= -1>
pos=<x= 32, y= -8, z= 14>, vel=<x=  5, y= -4, z=  6>
pos=<x= -1, y= -2, z= -8>, vel=<x= -3, y= -6, z= -9>

After 100 steps:

pos=<x=  8, y=-12, z= -9>, vel=<x= -7, y=  3, z=  0>
pos=<x= 13, y= 16, z= -3>, vel=<x=  3, y=-11, z= -5>
pos=<x=-29, y=-11, z= -1>, vel=<x= -3, y=  7, z=  4>
pos=<x= 16, y=-13, z= 23>, vel=<x=  7, y=  1, z=  1>

Energy after 100 steps:

pot:  8 + 12 +  9 = 29;   kin: 7 +  3 + 0 = 10;   total: 29 * 10 = 290
pot: 13 + 16 +  3 = 32;   kin: 3 + 11 + 5 = 19;   total: 32 * 19 = 608
pot: 29 + 11 +  1 = 41;   kin: 3 +  7 + 4 = 14;   total: 41 * 14 = 574
pot: 16 + 13 + 23 = 52;   kin: 7 +  1 + 1 =  9;   total: 52 *  9 = 468
Sum of total energy: 290 + 608 + 574 + 468 = 1940

What is the total energy in the system after simulating the moons given in your
scan for 1000 steps?

"""

import itertools

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


if __name__ == '__main__':

    # First test case:
    io = Moon('Io', -1, 0, 2)
    europa = Moon('Europa', 2, -10, -7)
    ganymede = Moon('Ganymede', 4, -8, 8)
    callisto = Moon('Callisto', 3, 5, -1)
    
    moon_list = [io, europa, ganymede, callisto]

    assert apply_sim(moon_list, 10, False) == 179

    # Second test case:
    io = Moon('Io',             -8, -10,  0)
    europa = Moon('Europa',      5,   5, 10)
    ganymede = Moon('Ganymede',  2,  -7,  3)
    callisto = Moon('Callisto',  9,  -8, -3)
    moon_list = [io, europa, ganymede, callisto]

    assert apply_sim(moon_list, 100, False) == 1940

    # Actual input:
    io = Moon('Io',              -1,  -4,  0)
    europa = Moon('Europa',       4,   7, -1)
    ganymede = Moon('Ganymede', -14, -10,  9)
    callisto = Moon('Callisto',   1,   2, 17)
    moon_list = [io, europa, ganymede, callisto]

    apply_sim(moon_list, 1000, True)

    # <x=-1, y=-4, z=0>
    # <x=4, y=7, z=-1>
    # <x=-14, y=-10, z=9>
    # <x=1, y=2, z=17>

    # Answer is 7988