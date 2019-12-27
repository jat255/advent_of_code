"""
--- Part Two ---
Now for the tricky part: notifying all the other robots about the solar flare.
The vacuum robot can do this automatically if it gets into range of a robot.
However, you can't see the other robots on the camera, so you need to be
thorough instead: you need to make the vacuum robot visit every part of the
scaffold at least once.

The vacuum robot normally wanders randomly, but there isn't time for that today.
Instead, you can override its movement logic with new rules.

Force the vacuum robot to wake up by changing the value in your ASCII program at
address 0 from 1 to 2. When you do this, you will be automatically prompted for
the new movement rules that the vacuum robot should use. The ASCII program will
use input instructions to receive them, but they need to be provided as ASCII
code; end each line of logic with a single newline, ASCII code 10.

First, you will be prompted for the main movement routine. The main routine may
only call the movement functions: A, B, or C. Supply the movement functions to
use as ASCII text, separating them with commas (,, ASCII code 44), and ending
the list with a newline (ASCII code 10). For example, to call A twice, then
alternate between B and C three times, provide the string A,A,B,C,B,C,B,C and
then a newline.

Then, you will be prompted for each movement function. Movement functions may
use L to turn left, R to turn right, or a number to move forward that many
units. Movement functions may not call other movement functions. Again, separate
the actions with commas and end the list with a newline. For example, to move
forward 10 units, turn left, move forward 8 units, turn right, and finally move
forward 6 units, provide the string 10,L,8,R,6 and then a newline.

Finally, you will be asked whether you want to see a continuous video feed;
provide either y or n and a newline. Enabling the continuous video feed can help
you see what's going on, but it also requires a significant amount of processing
power, and may even cause your Intcode computer to overheat.

Due to the limited amount of memory in the vacuum robot, the ASCII definitions
of the main routine and the movement functions may each contain at most 20
characters, not counting the newline.

For example, consider the following camera feed:

#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......

In order for the vacuum robot to visit every part of the scaffold at least once,
one path it could take is:

R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2

Without the memory limit, you could just supply this whole string to function A
and have the main routine call A once. However, you'll need to split it into
smaller parts.

One approach is:

- Main routine: A,B,C,B,A,C
  (ASCII input: 65, 44, 66, 44, 67, 44, 66, 44, 65, 44, 67, 10)
- Function A:   R,8,R,8
  (ASCII input: 82, 44, 56, 44, 82, 44, 56, 10)
- Function B:   R,4,R,4,R,8
  (ASCII input: 82, 44, 52, 44, 82, 44, 52, 44, 82, 44, 56, 10)
- Function C:   L,6,L,2
  (ASCII input: 76, 44, 54, 44, 76, 44, 50, 10)

Visually, this would break the desired path into the following parts:

A,        B,            C,        B,            A,        C
R,8,R,8,  R,4,R,4,R,8,  L,6,L,2,  R,4,R,4,R,8,  R,8,R,8,  L,6,L,2

CCCCCCA...BBBBB
C.....A...B...B
C.....A...B...B
......A...B...B
......A...CCC.B
......A.....C.B
^AAAAAAAA...C.B
......A.A...C.B
......AAAAAA#AB
........A...C..
....BBBB#BBBB..
....B...A......
....B...A......
....B...A......
....BBBBA......

Of course, the scaffolding outside your ship is much more complex.

As the vacuum robot finds other robots and notifies them of the impending solar
flare, it also can't help but leave them squeaky clean, collecting any space
dust it finds. Once it finishes the programmed set of movements, assuming it
hasn't drifted off into space, the cleaning robot will return to its docking
station and report the amount of space dust it collected as a large, non-ASCII
value in a single output instruction.

After visiting every part of the scaffold at least once, how much dust does the
vacuum robot report it has collected?

"""
import itertools
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.animation as animation
import random

class Computer():
    def __init__(self, name, inp, 
                 phase_setting=None, input_code=None, 
                 interactive=False, debug_level='off'):
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
        self.interactive = interactive
        self.total_output = []
        self.this_runs_output = []
        self.debug_level = debug_level


    def parse_param_modes(self, param_int, nparams):
        params = [0] * nparams
        if self.pos == 995:
            print('', end='')
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
                # i is parameter number (0, 1, or 3); if i==2, we're writing   
                if i < 2 and self.cur_opcode != 3:
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
            if self.pos == 989:
                print('', end='')

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
                    if self.interactive and new_input is None:
                        in_string = input('Enter input for intcode computer: ')
                        try: 
                            input_code = int(in_string)
                        except ValueError:
                            self.output = self.last_output
                            self.dbg_print('\t| no new input; pausing', 
                                        newline=True)
                            return None
                        self.dbg_print(f'\t| got {input_code} from interactive input')
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
                self.dbg_print(f'JMP_IF_NONZERO ({nparams})', space='\t\t')
                if params[0] != 0:
                    self.pos = params[1]
                    jumped = True
                    self.dbg_print(f'| {params[0]} != 0, so jumped | {params[1]} -> pos')
                else:
                    self.dbg_print(f'| {params[0]} == 0, so did not jump')
            elif opcode == 6:
                nparams = 2
                params = self.parse_param_modes(param_int, nparams)
                self.dbg_print(f'JMP_IF_ZERO ({nparams})', space='\t\t')
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
                if self.pos == 995:
                    print('', end='')
                    pass
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

def print_output(output):
    print(''.join([chr(o) for o in output]))

def scaffold_to_numpy(scaffold, dtype=int):
    if dtype == int:
        newlines = [[]]
        inner_count = 0
        for l in scaffold:
            if l == 10:
                newlines.append([])
                inner_count += 1
            else:
                newlines[inner_count].append(l)
            
        newlines = [l for l in newlines if len(l) == 43]
        arr = np.array(newlines, dtype=int)
   
    elif dtype == str:
        lines = ''.join([chr(o) for o in scaffold]).strip('\n').split('\n')
        lines = [list(l) for l in lines]
        arr = np.array(lines, dtype=str)
    
    return arr

def test_intersection(arr, index, dtype=int):
    y = index[0]
    x = index[1]
    val_to_test = 35 if dtype==int else '#'
    
    if y == 0 or x == 0 or y == arr.shape[0] - 1 or x == arr.shape[1] - 1:
        return False

    # to be an intersection, all four (up, down, left right) values must be
    # 35 (#)
    if arr[y+1, x] == val_to_test and arr[y-1, x] == val_to_test and \
        arr[y, x+1] == val_to_test and arr[y, x-1] == val_to_test and \
            arr[y, x] == val_to_test:
        return True
    else:
        return False

def input_string(s, debug_print=False):
    for i in s:
        code = ord(i)
        if debug_print:
            print(f'inputting "{i}" as "{code}"')
        if c.run_intcode(new_input=code) is False:
            print_output(c.this_runs_output)
            break
        

if __name__ == '__main__':

    with open('17/input', 'r') as f:
        inp = f.readline()

    c = Computer('maze', inp, debug_level='off')    

    c.mem[0] = 2
    c.run_intcode()

    print_output(c.this_runs_output)

    arr = scaffold_to_numpy(c.this_runs_output)    

    double_newline = None
    for idx, i in enumerate(c.this_runs_output[:-1]):
        if i == 10 and c.this_runs_output[idx+1] == 10:
            double_newline = idx

    print(''.join([chr(i) for i in c.this_runs_output[double_newline:]]))
    
    # c.interactive = True
    # c.debug_level = 'output'
    # while True:
    #     c.run_intcode()
    #     print_output(c.this_runs_output)
    #     pass

    # 65 44 66 44 65 44 67 44 66 44 67 44 66 44 67 44 65 44 66 10
    main_routine = 'A,B,A,C,B,C,B,C,A,B\n'
    c.debug_level = 'output'
    input_string(main_routine, debug_print=True)
    print('')
    print_output(c.this_runs_output)

    c.debug_level = 'output'
    func_A = 'L,6,L,4,R,8\n'				
    input_string(func_A, debug_print=True)
    print_output(c.this_runs_output)

    func_B = 'R,8,L,6,L,4,L,10,R,8\n'
    input_string(func_B, debug_print=True)
    print_output(c.this_runs_output)

    func_C = 'L,4,R,4,L,4,R,8\n'		
    input_string(func_C, debug_print=True)
    print_output(c.this_runs_output)

    c.debug_level = 'off'
    input_string('n\n', debug_print=True)
    print_output(c.this_runs_output)
    # c.run_intcode(10)

    print(c.last_output)
    
    # Answer is 714866