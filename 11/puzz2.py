"""
--- Part Two ---
You're not sure what it's trying to paint, but it's definitely not a
registration identifier. The Space Police are getting impatient.

Checking your external ship cameras again, you notice a white panel marked
"emergency hull painting robot starting panel". The rest of the panels are still
black, but it looks like the robot was expecting to start on a white panel, not
a black one.

Based on the Space Law Space Brochure that the Space Police attached to one of
your windows, a valid registration identifier is always eight capital letters.
After starting the robot on a single white panel instead, what registration
identifier does it paint on your hull? 

"""

# Black is 0
# White is 1

import itertools

class Computer():
    def __init__(self, name, inp, 
                 phase_setting=None, input_code=None, debug=False):
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
        self.debug = debug


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
        if self.debug:
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
            self.dbg_print(f'({self.pos:04g})', space='\n')
            self.dbg_print(f'{opcode}')

            if opcode == 99:
                print('REACHED OPCODE 99 -- BREAKING')
                return False

            if opcode > 9:
                # we have more than two digits, so split opcode and parameters
                reduced_opcode = int(str(opcode)[-2:])
                param_int = int(str(opcode)[:-2])
                opcode = reduced_opcode

            self.cur_opcode = opcode

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

if __name__ == '__main__':

    from collections import defaultdict
    from matplotlib import pyplot as plt
    import numpy as np

    with open('11/input', 'r') as f:
        inp = f.readline()

    grid = defaultdict(int)
    grid[(0,0)] = 1
    comp = Computer('intcode', inp, input_code=grid[(0,0)], debug=False)
    cur_x, cur_y = (0,0)
    cur_ang = 90

    # 90 is up, 180 is left, 0 is right, 270 is down
    # +x is right, +y is up

    res = comp.run_intcode()
    i = 0
    
    while True:
        color = comp.total_output[0]
        direction = comp.total_output[1]
        comp.total_output = []

        # process color
        grid[(cur_x, cur_y)] = color
        if i % 1000 == 0:
            print(f'pos: ({cur_x}, {cur_y}) - move {i} - output: '
                  f'{comp.total_output}')
            print(f'Got {color}, so painted ({cur_x}, {cur_y}) {"white" if color else "black"}')

        # process turn and move
        if direction == 0:
            cur_ang += 90
        else:
            cur_ang -= 90
        cur_ang %= 360
        
        if cur_ang == 0:
            cur_x += 1
        elif cur_ang == 90:
            cur_y += 1
        elif cur_ang == 180:
            cur_x -= 1
        elif cur_ang == 270:
            cur_y -= 1
        else:
            raise ValueError(f'got bad value for cur_ang: {cur_ang}')

        res = comp.run_intcode(new_input=grid[(cur_x, cur_y)])
        if res == False:
            print(f'Painted {len(grid)} panels at least once')
            break
        i += 1

    min_x, min_y, max_x, max_y = (1, 1, -1, -1)
    for k in grid.keys():
        min_x = min(k[0], min_x)
        min_y = min(k[1], min_y)
        max_x = max(k[0], max_x)
        max_y = max(k[1], max_y)

    print('min_x, max_x:', min_x, max_x)
    print('min_y, max_y:', min_y, max_y)
    print('')
    
    arr = np.zeros((max_y - min_y + 1, max_x - min_x + 1), dtype=int)

    for y in range(min_y, max_y+1)[::-1]:
        print(f'line {y:03g}: ', end='')
        for x in range(min_x, max_x+1):
            print('.' if grid[x,y] == 0 else '#', end='')
            arr[y - min_y, x - min_x] = grid[x,y]
        print('')

    arr = np.flip(arr, 0)
    plt.imshow(arr)
    plt.show()

# Answer is EFCKUEGC
