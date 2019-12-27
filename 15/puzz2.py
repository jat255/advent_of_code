"""
--- Part Two ---
You quickly repair the oxygen system; oxygen gradually fills the area.

Oxygen starts in the location containing the repaired oxygen system. It takes
one minute for oxygen to spread to all open locations that are adjacent to a
location that already contains oxygen. Diagonal locations are not adjacent.

In the example above, suppose you've used the droid to explore the area fully
and have the following map (where locations that currently contain oxygen are
marked O):

 ##   
#..## 
#.#..#
#.O.# 
 ###  

Initially, the only location which contains oxygen is the location of the
repaired oxygen system. However, after one minute, the oxygen spreads to all
open (.) locations that are adjacent to a location containing oxygen:

 ##   
#..## 
#.#..#
#OOO# 
 ###  

After a total of two minutes, the map looks like this:

 ##   
#..## 
#O#O.#
#OOO# 
 ###  

After a total of three minutes:

 ##   
#O.## 
#O#OO#
#OOO# 
 ###  

And finally, the whole region is full of oxygen after a total of four minutes:

 ##   
#OO## 
#O#OO#
#OOO# 
 ###  

So, in this example, all locations contain oxygen after 4 minutes.

Use the repair droid to get a complete map of the area. How many minutes will it
take to fill with oxygen?

"""
import itertools
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.animation as animation
import random

class Computer():
    def __init__(self, name, inp, 
                 phase_setting=None, input_code=None, debug_level='off'):
        self.name = name
        self.mem = [int(i) for i in inp.split(',')] + \
            [0]*len(inp.split(','))*100
        self.input_stack = []
        if phase_setting is not None:
            self.input_stack += [phase_setting]
        if input_code is not None:
            self.input_stack += [input_code]
        self.rel_base = 0
        self.output = None
        self.output_pos = None
        self.cur_opcode = None
        self.total_output = []
        self.this_runs_output = []
        self.debug_level = debug_level


    def parse_param_modes(self, param_int, nparams):
        params = [0] * nparams
        if param_int:
            param_str = f'{param_int:0{nparams}g}'
        else:
            param_str = '0' * nparams
        for i, mode in enumerate(param_str[::-1]):
            param_val = self.mem[self.pos + i + 1]
            if int(mode) == 0:
                # position mode, so value is position in memory of parameter
                if i < 2 and self.cur_opcode != 3:
                    params[i] = self.mem[param_val]
                else:
                    # unless it's the output value, then it's just the position
                    params[i] = param_val
            elif int(mode) == 1:
                # immediate mode, so value is just the parameter
                params[i] = param_val
            elif int(mode) == 2:
                # relative mode (similar to position, but with rel_base added)
                # for opcode 3, since we're writing, we want to be in immediate 
                # mode:
                if i < 2:
                    params[i] = self.mem[param_val + self.rel_base]
                else:
                    # unless it's the output value, then it's just the position 
                    # (this is immediate mode)
                    params[i] = param_val + self.rel_base
            else:
                raise ValueError('Parameter mode should be either 0 or 1')
        for p in params: self.dbg_print(str(p), space=' ')
        self.dbg_print('\t' * (1 if nparams==1 else 0) + '| ')
        return params

    
    def print_mem_array(self):
        print('indx: ', end='')
        for num in range(len(self.mem)):
            print(f'{num:4g} ', end='')
        print('')
        print('vals: ', end='')
        for num in self.mem[:100]:
            print(f'{num:4g} ', end='')
        print('')

    
    def dbg_print(self, string, space='\t', newline=False):
        if self.debug_level == 'all':
            print(space + string,
                  end='' if not newline else '\n')
        if self.debug_level == 'output':
            if self.cur_opcode in [3, 4]:
                print(space + string,
                    end='' if not newline else '\n')


    def run_intcode(self, new_input=None):
        """
        inp : str
            The comma-separated string of inputs
        """
        if not hasattr(self, 'pos'):
            self.pos = 0
        if not hasattr(self, 'iteration'):
            self.iteration = 1
        if not hasattr(self, 'last_output'):
            self.last_output = None
        self.this_runs_output = []
        
        # opcode 1 means add; opcode 2 means multiply
        # next three numbers are first input index, second input index, and index to
        # write to
        
        # opcode 3 means take an input and save it to position
        # opcode 4 means output (print) the parameter
        while True:
            opcode = self.mem[self.pos]
            param_int = None
            params = None
            jumped = False

            if opcode == 99:
                print('REACHED OPCODE 99 -- BREAKING')
                return False

            if opcode > 9:
                # we have more than two digits, so split opcode and parameters
                reduced_opcode = int(str(opcode)[-2:])
                param_int = int(str(opcode)[:-2])
                opcode = reduced_opcode

            self.cur_opcode = opcode

            self.dbg_print(f'({self.pos:04g})', space='\n')
            self.dbg_print(f'{opcode}')

            if opcode == 1:
                # add values of first two parameters and store in third param
                nparams = 3
                params = self.parse_param_modes(param_int, nparams)
                self.dbg_print(f'ADD ({nparams})')
                self.mem[params[2]] = params[0] + params[1]
                self.dbg_print(f'\t\t| {params[0]} + {params[1]} -> mem[{params[2]}]')
            elif opcode == 2:
                # multiply values of first two parameters and store in third param
                nparams = 3
                params = self.parse_param_modes(param_int, nparams)
                self.dbg_print(f'MULT ({nparams})')
                self.mem[params[2]] = params[0] * params[1]
                self.dbg_print(f'\t| {params[0]} * {params[1]} -> mem[{params[2]}]')
            elif opcode == 3:
                # take input from user and store at postion of only parameter
                nparams = 1
                params = self.parse_param_modes(param_int, nparams)
                self.dbg_print(f'INPUT ({nparams})')
                if len(self.input_stack) > 0:
                    input_code = int(self.input_stack.pop(0))
                    self.dbg_print(f'\t| got {input_code} from input_stack')
                else:
                    if new_input is not None:
                        input_code = int(new_input)
                        self.dbg_print(f'\t| got {input_code} from new_input')
                        # make sure to clear new_input, so we don't think we
                        # got another input the next time we see an opcode 3                        
                        new_input = None
                    # we've run out of inputs, so we have to pause and wait
                    # for the program to continue with a new input
                    # Return None to indicate that we're not done yet
                    else:
                        self.output = self.last_output
                        self.dbg_print('\t| no new input; pausing', 
                                       newline=True)
                        return None
                self.mem[params[0]] = input_code
                self.dbg_print(f'| {input_code} -> mem[{params[0]}]')
            elif opcode == 4:
                # output value of the only parameter
                nparams = 1
                params = self.parse_param_modes(param_int, nparams)
                self.dbg_print(f'OUTPUT ({nparams})')
                self.last_output = params[0]
                self.output_pos = self.pos
                self.output = self.last_output
                self.total_output += [self.last_output]
                self.this_runs_output += [self.last_output]
                self.dbg_print(f'\t* **OUTPUT** {self.output}')
            elif opcode == 5:
                nparams = 2
                params = self.parse_param_modes(param_int, nparams)
                self.dbg_print(f'JMP_IF_NONZERO ({nparams})')
                if params[0] != 0:
                    self.pos = params[1]
                    jumped = True
                    self.dbg_print(f'| {params[0]} != 0, so jumped | {params[1]} -> pos')
                else:
                    self.dbg_print(f'| {params[0]} == 0, so did not jump')
            elif opcode == 6:
                nparams = 2
                params = self.parse_param_modes(param_int, nparams)
                self.dbg_print(f'JMP_IF_ZERO ({nparams})')
                if params[0] == 0:
                    self.pos = params[1]
                    jumped = True
                    self.dbg_print(f'\t| {params[0]} == 0, so jumped | {params[1]} -> pos')
                else:
                    self.dbg_print(f'\t| {params[0]} != 0, so did not jump')

            elif opcode == 7:
                nparams = 3
                params = self.parse_param_modes(param_int, nparams)
                self.dbg_print(f'LESS_THAN ({nparams})')
                if params[0] < params[1]:
                    self.mem[params[2]] = 1
                    self.dbg_print(f'\t| {params[0]} < {params[1]}, so 1 -> {params[2]}')
                else:
                    self.mem[params[2]] = 0
                    self.dbg_print(f'\t| {params[0]} !< {params[1]}, so 0 -> {params[2]}')
            elif opcode == 8:
                nparams = 3
                params = self.parse_param_modes(param_int, nparams)
                self.dbg_print(f'EQUALS ({nparams})')
                if params[0] == params[1]:
                    self.mem[params[2]] = 1
                    self.dbg_print(f'\t| was_equal | 1 -> mem[{params[2]}]')
                else:
                    self.mem[params[2]] = 0
                    self.dbg_print(f'\t| not_equal | 0 -> mem[{params[2]}]')
            elif opcode == 9:
                nparams = 1
                params = self.parse_param_modes(param_int, nparams)
                self.dbg_print('ADJ_RELBASE')
                self.dbg_print(f'\t| {self.rel_base} += {params[0]}')
                self.rel_base += params[0]
                self.dbg_print(f' = {self.rel_base}', space='')
                
            
            if not jumped:
                self.pos += nparams + 1
            
            self.iteration += 1

        self.output = self.last_output



from collections import defaultdict
grid = defaultdict(lambda: '.')

def get_min_max_grid(grid):
    min_x, max_x, min_y, max_y = 1, 0, 1, 0
    
    for k, v in grid.items():
        if k == 'goal_pos':
            continue
        min_x = min(k[0], min_x)
        max_x = max(k[0], max_x)
        min_y = min(k[1], min_y)
        max_y = max(k[1], max_y)
    
    return min_x, max_x, min_y, max_y

def print_grid(cur_x, cur_y, np_grid=None):
    output_string = ''

    if np_grid is None:
        this_grid = grid
        min_x, max_x, min_y, max_y = get_min_max_grid(this_grid)
    else:
        this_grid = np_grid
        min_x, min_y = 0, 0
        max_y, max_x = this_grid.shape

    out_dict = {WALL:     '█', 
                OPEN:     ' ',
                GOAL:     'O',
                UNKNOWN:  '·',
                ON_PATH:  '+',
                BLOCKED:  '▓',
                OXY:      'O',
                START:    '*'
                }
    for y in range(min_y, max_y)[::-1]:
        for x in range(min_x, max_x):
            if (x, y) == (cur_x, cur_y):
                output_string += 'X'
            # elif (x, y) == (0, 0):
            #     output_string += '*'
            else:
                if np_grid is None:
                    output_string += out_dict[this_grid[(x, y)]]
                else:
                    output_string += out_dict[this_grid[y, x]]
        output_string += '\n'
    
    output_string += '\n'

    print(output_string)

    return max_y - min_y


NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

WALL = 0
OPEN = 1
GOAL = 2
BLOCKED = 9
UNKNOWN = 15
ON_PATH = 5
OXY = 4
START = 3

# dict to simulate a right-handed turn
right_turn = {NORTH: EAST,
              SOUTH: WEST,
              WEST: NORTH,
              EAST: SOUTH}

backwards = {NORTH: SOUTH,
             SOUTH: NORTH,
             WEST: EAST,
             EAST: WEST}

def get_next_pos(x, y, direction):
    if direction == NORTH:
        y += 1
    elif direction == SOUTH:
        y -= 1
    elif direction == EAST:
        x += 1
    elif direction == WEST:
        x -= 1
    else:
        raise ValueError('Direction should be NORTH, SOUTH, EAST, or WEST')
    
    return x, y

def map_surroundings(x, y):
    poss_next_moves = []
    
    for d in [NORTH, EAST, SOUTH, WEST]:
        c.run_intcode(new_input=d)
        status_code = c.last_output
        if status_code == WALL:
            grid[get_next_pos(x, y, d)] = WALL         # we hit a wall
        elif status_code == OPEN:
            if grid[get_next_pos(x, y, d)] == ON_PATH:
                pass
            else:
                grid[get_next_pos(x, y, d)] = OPEN
                poss_next_moves.append(d)
            # the intcode computer will move, so go back to current position
            c.run_intcode(new_input=backwards[d])
            if c.last_output not in [OPEN, GOAL]:
                raise RuntimeError("Something went wrong... spot should be open")
        elif status_code == GOAL:
            grid[get_next_pos(x, y, d)] = GOAL
            poss_next_moves.append(d)

    return poss_next_moves

def find_path(x, y, grid, last_x=None, last_y=None):
    # examine what's around us
    # print(x,y)
    if grid[(x, y)] == GOAL: 
        print(f'setting grid["goal_pos"] to {(x, y)}')
        grid['goal_pos'] = (x, y)
        # return True
    elif grid[(x, y)] == WALL: return False
    grid[(x,y)] = ON_PATH
    poss_next_moves = map_surroundings(x, y)
    print_grid(x, y)
    if NORTH in poss_next_moves:
        c.run_intcode(new_input=NORTH)
        if find_path(x    , y + 1, grid, x, y): return True    # NORTH
    if EAST in poss_next_moves:
        c.run_intcode(new_input=EAST)
        if find_path(x + 1, y    , grid, x, y): return True    # EAST
    if SOUTH in poss_next_moves:
        c.run_intcode(new_input=SOUTH)
        if find_path(x    , y - 1, grid, x, y): return True    # SOUTH
    if WEST in poss_next_moves:
        c.run_intcode(new_input=WEST)
        if find_path(x - 1, y    , grid, x, y): return True    # WEST
    grid[(x, y)] = BLOCKED
    print_grid(x, y)
    # print('backtracking')
    if last_x is not None and last_y is not None:
        if last_x - x == -1:
            # we last moved East, so move back West
            c.run_intcode(new_input=WEST)
        elif last_x - x == 1:
            # previous position was less than this one, so we moved west; go back east
            c.run_intcode(new_input=EAST)
        elif last_y - y == -1:
            # previous Y is greater than this Y, so we moved north; go back south
            c.run_intcode(new_input=SOUTH)
        elif last_y - y == 1:
            # previous Y is less than this Y, so we moved south; go back north
            c.run_intcode(new_input=NORTH)
    return False


with open('15/input', 'r') as f:
    inp = f.readline()

c = Computer('maze', inp, debug_level='off')


import dill
import os
import numpy as np

if __name__ == '__main__':


    if os.path.isfile('15/puzz2.pkl'):
        with open("15/puzz2.pkl", "rb") as f:
            grid = dill.load(f)

    else:
        # default value for a grid position is '.', which means we haven't visited
        # 0 is wall; 1 is open; 2 is end position
        cur_x, cur_y = 0, 0
        grid[(cur_x, cur_y)] = OPEN

        find_path(0, 0, grid)
        with open("15/puzz2.pkl", "wb") as f:
            dill.dump(grid, f)

    print(f'grid["goal_pos"] is {grid["goal_pos"]}')
    
    min_x, max_x, min_y, max_y = get_min_max_grid(grid)
    x_size = max_x - min_x
    y_size = max_y - min_y

    goal_pos = grid.pop('goal_pos')
    goal_pos_x = goal_pos[0] - min_x
    goal_pos_y = goal_pos[1] - min_y
    start_pos = (0, 0)
    start_pos_x = start_pos[0] - min_x
    start_pos_y = start_pos[1] - min_y
    
    np_grid = np.zeros((y_size + 1, x_size + 1), dtype=int)

    for k, v in grid.items():
        x = k[0] - min_x
        y = k[1] - min_y
        if v == '.': v = UNKNOWN
        np_grid[y, x] = v
    
    np_grid[np_grid == BLOCKED] = OPEN
    np_grid[goal_pos_y, goal_pos_x] = GOAL
    np_grid[start_pos_y, start_pos_x] = START


    np_goal_x = np.argwhere(np_grid == GOAL)[0][1]
    np_goal_y = np.argwhere(np_grid == GOAL)[0][0]
    
    np_grid[np_goal_y, np_goal_x] = OXY

    total = 0
    for status_s, status in \
        zip(['WALL', 'OPEN', 'GOAL', 'BLOCKED', 'UNKNOWN', 'ON_PATH', 'OXY', 'START'],
            [WALL, OPEN, GOAL, BLOCKED, UNKNOWN, ON_PATH, OXY, START]):
        total += (np_grid == status).sum()
        print(f'Total {status_s} is {(np_grid == status).sum()}')
    print(f'Total is {total}; np_grid size is {np_grid.size}')

    iters = 0
    new_oxy = np.argwhere(np_grid == OXY)
    next_oxy = new_oxy
    while True:
        if (np_grid == OPEN).sum() == 0:
            break
        new_oxy = next_oxy
        next_oxy = None
        for y, x in new_oxy:
            for new_y, new_x in [(y+1, x), (y-1,x), (y,x+1), (y,x-1)]:
                if 0< new_y <= y_size and 0< new_x <= x_size:
                    if np_grid[new_y, new_x] in [OPEN, START]:
                        if next_oxy is None:
                            next_oxy = np.array([(new_y, new_x)])
                        else:
                            next_oxy = np.append(next_oxy, np.array([(new_y, new_x)]), axis=0)
                        np_grid[new_y, new_x] = OXY
                print_grid(new_x, new_y, np_grid)
        iters += 1
        # break

    print(f'Filling the space took {iters} iterations (minutes)')
    
    # Answer is 364