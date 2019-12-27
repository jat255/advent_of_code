"""
--- Day 15: Oxygen System ---
Out here in deep space, many things can go wrong. Fortunately, many of those
things have indicator lights. Unfortunately, one of those lights is lit: the
oxygen system for part of the ship has failed!

According to the readouts, the oxygen system must have failed days ago after a
rupture in oxygen tank two; that section of the ship was automatically sealed
once oxygen levels went dangerously low. A single remotely-operated repair droid
is your only option for fixing the oxygen system.

The Elves' care package included an Intcode program (your puzzle input) that you
can use to remotely control the repair droid. By running that program, you can
direct the repair droid to the oxygen system and fix the problem.

The remote control program executes the following steps in a loop forever:

- Accept a movement command via an input instruction.
- Send the movement command to the repair droid.
- Wait for the repair droid to finish the movement operation.
- Report on the status of the repair droid via an output instruction.

Only four movement commands are understood: north (1), south (2), west (3), and
east (4). Any other command is invalid. The movements differ in direction, but
not in distance: in a long enough east-west hallway, a series of commands like
4,4,4,4,3,3,3,3 would leave the repair droid back where it started.

The repair droid can reply with any of the following status codes:

- 0: The repair droid hit a wall. Its position has not changed.
- 1: The repair droid has moved one step in the requested direction.
- 2: The repair droid has moved one step in the requested direction; its new
  position is the location of the oxygen system.

You don't know anything about the area around the repair droid, but you can
figure it out by watching the status codes.

For example, we can draw the area using D for the droid, # for walls, . for
locations the droid can traverse, and empty space for unexplored locations.
Then, the initial state looks like this:

      
      
   D  
      
      
To make the droid go north, send it 1. If it replies with 0, you know that
location is a wall and that the droid didn't move:

      
   #  
   D  
      
      
To move east, send 4; a reply of 1 means the movement was successful:

      
   #  
   .D 
      
      
Then, perhaps attempts to move north (1), south (2), and east (4) are all met
with replies of 0:

      
   ## 
   .D#
    # 
      
Now, you know the repair droid is in a dead end. Backtrack with 3 (which you
already know will get a reply of 1 because you already know that location is
open):

      
   ## 
   D.#
    # 
      
Then, perhaps west (3) gets a reply of 0, south (2) gets a reply of 1, south
again (2) gets a reply of 0, and then west (3) gets a reply of 2:

      
   ## 
  #..#
  D.# 
   #  

Now, because of the reply of 2, you know you've found the oxygen system! In this
example, it was only 2 moves away from the repair droid's starting position.

What is the fewest number of movement commands required to move the repair droid
from its starting position to the location of the oxygen system?

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

def print_grid(cur_x, cur_y):
    output_string = ''

    min_x, max_x, min_y, max_y = 1, 0, 1, 0
    
    for k, v in grid.items():
        min_x = min(k[0], min_x)
        max_x = max(k[0], max_x)
        min_y = min(k[1], min_y)
        max_y = max(k[1], max_y)

    for y in range(min_y, max_y)[::-1]:
        for x in range(min_x, max_x):
            out_dict = {WALL:     '█', 
                        OPEN:     ' ',
                        GOAL:     'O',
                        '.':      '·',
                        ON_PATH:  '+',
                        BLOCKED:  '▓',
                        }
            if (x, y) == (cur_x, cur_y):
                output_string += 'X'
            elif (x, y) == (0, 0):
                output_string += '*'
            else:
                output_string += out_dict[grid[(x, y)]]
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
UNKNOWN = '.'
ON_PATH = 5

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
            if c.last_output != OPEN:
                raise RuntimeError("Something went wrong... spot should be open")
        elif status_code == GOAL:
            grid[get_next_pos(x, y, d)] = GOAL
            poss_next_moves = [d]
            # we're done!

    return poss_next_moves

def find_path(x, y, grid, last_x=None, last_y=None):
    # examine what's around us
    # print(x,y)
    if grid[(x, y)] == GOAL: 
        print_grid(x, y)
        return True
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


if __name__ == '__main__':


    # default value for a grid position is '.', which means we haven't visited
    # 0 is wall; 1 is open; 2 is end position
    cur_x, cur_y = 0, 0
    grid[(cur_x, cur_y)] = OPEN

    find_path(0, 0, grid)

    steps = 0
    for k, v in grid.items():
        if v == ON_PATH: steps += 1

    print(f'{steps} steps required')

    # Answer is 270