"""
--- Part Two ---
You aren't sure how large Santa's ship is. You aren't even sure if you'll need
to use this thing on Santa's ship, but it doesn't hurt to be prepared. You
figure Santa's ship might fit in a 100x100 square.

The beam gets wider as it travels away from the emitter; you'll need to be a
minimum distance away to fit a square of that size into the beam fully. (Don't
rotate the square; it should be aligned to the same axes as the drone grid.)

For example, suppose you have the following tractor beam readings:

#.......................................
.#......................................
..##....................................
...###..................................
....###.................................
.....####...............................
......#####.............................
......######............................
.......#######..........................
........########........................
.........#########......................
..........#########.....................
...........##########...................
...........############.................
............############................
.............#############..............
..............##############............
...............###############..........
................###############.........
................#################.......
.................########OOOOOOOOOO.....
..................#######OOOOOOOOOO#....
...................######OOOOOOOOOO###..
....................#####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
......................###OOOOOOOOOO#####
.......................##OOOOOOOOOO#####
........................#OOOOOOOOOO#####
.........................OOOOOOOOOO#####
..........................##############
..........................##############
...........................#############
............................############
.............................###########

In this example, the 10x10 square closest to the emitter that fits entirely
within the tractor beam has been marked O. Within it, the point closest to the
emitter (the only highlighted O) is at X=25, Y=20.

Find the 100x100 square closest to the emitter that fits entirely within the
tractor beam; within that square, find the point closest to the emitter. What
value do you get if you take that point's X coordinate, multiply it by 10000,
then add the point's Y coordinate? (In the example above, this would be 250020.)

Although it hasn't changed, you can still get your puzzle input.

"""
import itertools
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.animation as animation
import random
from tqdm import tqdm
import multiprocessing as mp
import pickle

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
                # print('REACHED OPCODE 99 -- BREAKING')
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
        

def run_part1(inp):
    arr = np.zeros((50,50))
    
    for y,x in tqdm(np.ndindex(arr.shape), total=50**2):
        c = Computer('tractorbeam', inp, debug_level='off')    
        c.run_intcode(x)
        c.run_intcode(y)
        arr[y,x] = c.last_output
        # print(x, y, c.last_output)

    output_str = ''
    for y in range(arr.shape[0]):
        for x in range(arr.shape[1]):
            output_str += '#' if arr[y,x] else '.'
        output_str += '\n'

    print(output_str)

    return arr


def run_part2_one_value(inp, xy, size=None):
    x, y = xy
    if size is not None:
        itr = x*size + y
        perc = itr/(size**2) * 100
    
    c = Computer('tractorbeam', inp, debug_level='off')    
    c.run_intcode(x)
    c.run_intcode(y)
    # print(f'{perc:.2f}%:', x, y, c.last_output)
    return (x, y, c.last_output)


def run_part2_1000():
    with open('19/input', 'r') as f:
        inp = f.readline()
    
    size = 1000

    print(f'Using {mp.cpu_count()} threads')
    pool = mp.Pool(mp.cpu_count())
    
    results = [pool.apply(run_part2_one_value, args=(inp, xy, size)) 
               for xy in np.ndindex((size,size))]
    
    pool.close()
    
    with open('19/puzz2_1.pk', 'wb') as f:
        pickle.dump(results, f)

def run_part2_serial(size):
    with open('19/input', 'r') as f:
        inp = f.readline()

    arr = np.zeros((size, size), dtype=int)
    arr[:] = -1

    full_sample = 10
    print(f'total is {size**2}')

    t = tqdm(total=size**2)
    for y in range(size):
        num_zeros = 0
        if y < full_sample:
            first_x = 0
            last_x = size
            to_check = list(range(first_x, last_x))
        else: 
            try:
                ones_loc = np.where(arr[y-1, :] == 1)[0]
                first_x = ones_loc.min()
                last_x = ones_loc.max() + 2
                to_check = list(range(first_x, last_x))
                if len(to_check) >= 20:
                    to_check = to_check[:10] + to_check[-10:]
                    val = np.where(np.diff(to_check) > 1)[0]
                    if val:
                        val = val[0]
                        set_to_1_range = list(range(to_check[val], 
                                                    to_check[val+1]))
                        # print(f'val is {val} + {set_to_1_range}')
                        arr[y, set_to_1_range] = 1
            except Exception as e:
                plt.imshow(arr)
                plt.show()
                raise e
        for x in to_check:
            xy = (x, y)
            t.set_description(f'({x}, {y}) - {to_check[0]}/{to_check[-1]}')
            t.n = y * size + x
            if y != 0 and y % 1000 == 0 and x == to_check[0]:
                plt.imshow(arr)
                plt.show()
            t.refresh()
            if x < full_sample and y < full_sample:
                arr[y, x] = run_part2_one_value(inp, xy)[2]
            else:
                arr[y, x] = run_part2_one_value(inp, xy)[2]
                if arr[y, x] != 0:
                    num_zeros = 0
                else:
                    num_zeros += 1
                    if num_zeros > 2:
                        # break when we find more than two zeros in a row
                        break

    t.close()
    return arr


from skimage.util import view_as_windows
import pdb

if __name__ == '__main__':

    # arr = run_part2_serial(5000)
    # np.savez_compressed('19/part2.npz', arr)

    chunk_start = 600

    with np.load('19/part2.npz') as data:
        arr = data['arr_0'][chunk_start:chunk_start+600, 
                            chunk_start:chunk_start+600]

    print('computing windows...')
    windows = view_as_windows(arr, (100,100))

    match_array = np.ones((100,100), dtype=int)

    print('matching windows')
    res = (windows == match_array).all(axis=(2,3)).nonzero()
    min_x = res[1][0] + chunk_start
    min_y = res[0][0] + chunk_start
    print(f'({min_x}, {min_y})')
    print(f'{min_x*10000 + min_y}')

    for y, x in zip(res[0], res[1]):
        arr[y, x] = 3

    with np.load('19/part2.npz') as data:
        arr1 = data['arr_0']

    arr1[chunk_start:chunk_start+600, 
         chunk_start:chunk_start+600] = arr
    arr1[min_y:min_y+100, min_x:min_x+100] = 4

    plt.imshow(arr1)
    plt.show()

    # Answer is 7720975
 
