"""
--- Day 21: Springdroid Adventure ---
You lift off from Pluto and start flying in the direction of Santa.

While experimenting further with the tractor beam, you accidentally pull an
asteroid directly into your ship! It deals significant damage to your hull and
causes your ship to begin tumbling violently.

You can send a droid out to investigate, but the tumbling is causing enough
artificial gravity that one wrong step could send the droid through a hole in
the hull and flying out into space.

The clear choice for this mission is a droid that can jump over the holes in the
hull - a springdroid.

You can use an Intcode program (your puzzle input) running on an ASCII-capable
computer to program the springdroid. However, springdroids don't run Intcode;
instead, they run a simplified assembly language called springscript.

While a springdroid is certainly capable of navigating the artificial gravity
and giant holes, it has one downside: it can only remember at most 15
springscript instructions.

The springdroid will move forward automatically, constantly thinking about
whether to jump. The springscript program defines the logic for this decision.

Springscript programs only use Boolean values, not numbers or strings. Two
registers are available: T, the temporary value register, and J, the jump
register. If the jump register is true at the end of the springscript program,
the springdroid will try to jump. Both of these registers start with the value
false.

Springdroids have a sensor that can detect whether there is ground at various
distances in the direction it is facing; these values are provided in read-only
registers. Your springdroid can detect ground at four distances: one tile away
(A), two tiles away (B), three tiles away (C), and four tiles away (D). If there
is ground at the given distance, the register will be true; if there is a hole,
the register will be false.

There are only three instructions available in springscript:

- AND X Y sets Y to true if both X and Y are true; otherwise, it sets Y to
  false.
- OR X Y sets Y to true if at least one of X or Y is true; otherwise, it sets Y
  to false.
- NOT X Y sets Y to true if X is false; otherwise, it sets Y to false.

In all three instructions, the second argument (Y) needs to be a writable
register (either T or J). The first argument (X) can be any register (including
A, B, C, or D).

For example, the one-instruction program NOT A J means "if the tile immediately
in front of me is not ground, jump".

Or, here is a program that jumps if a three-tile-wide hole (with ground on the
other side of the hole) is detected:

NOT A J
NOT B T
AND T J
NOT C T
AND T J
AND D J

The Intcode program expects ASCII inputs and outputs. It will begin by
displaying a prompt; then, input the desired instructions one per line. End each
line with a newline (ASCII code 10). When you have finished entering your
program, provide the command WALK followed by a newline to instruct the
springdroid to begin surveying the hull.

If the springdroid falls into space, an ASCII rendering of the last moments of
its life will be produced. In these, @ is the springdroid, # is hull, and . is
empty space. For example, suppose you program the springdroid like this:

NOT D J
WALK

This one-instruction program sets J to true if and only if there is no ground
four tiles away. In other words, it attempts to jump into any hole it finds:

.................
.................
@................
#####.###########

.................
.................
.@...............
#####.###########

.................
..@..............
.................
#####.###########

...@.............
.................
.................
#####.###########

.................
....@............
.................
#####.###########

.................
.................
.....@...........
#####.###########

.................
.................
.................
#####@###########

However, if the springdroid successfully makes it across, it will use an output
instruction to indicate the amount of damage to the hull as a single giant
integer outside the normal ASCII range.

Program the springdroid with logic that allows it to survey the hull without
falling into space. What amount of hull damage does it report?

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


def print_output(output):
    print(get_output(output))

def get_output(output):
    return ''.join([chr(o) for o in output])


def input_string(c, s, print=False, debug_print=False):
    for i in s:
        code = ord(i)
        if debug_print:
            print(f'inputting "{i}" as "{code}"')
        if c.run_intcode(new_input=code) is False:
            if print: print_output(c.this_runs_output)
            break

def combos(num_instr):
    commands = ['AND', 'OR', 'NOT']
    arg1 = ['A', 'B', 'C', 'D', 'J', 'T']
    arg2 = ['J', 'T']

    all_instructions = [' '.join(cmd) + '\n' for 
                        cmd in itertools.product(commands, arg1, arg2)]

    instructions = [list(i) for i in 
                    itertools.permutations(all_instructions, num_instr)]

    return instructions

def run_part1_one_instruction(instr):
    global inp
    instr.append('WALK\n')
    c = Computer('spring', inp, debug_level='off')    
    c.run_intcode()
    for i in instr:
        input_string(c, i)
    if c.last_output > 10:
        print(instr)
        print(c.last_output)
        return c.last_output
    else:
        return None

def run_part1_brute_force():
    global inp
    with open('21/input', 'r') as f:
        inp = f.readline()

    pool = mp.Pool(mp.cpu_count())
    to_process = combos(4)
    random.shuffle(to_process)
    
    r = list(tqdm(pool.imap(run_part1_one_instruction, to_process), 
                  total=len(combos(4))))

if __name__ == "__main__":
    
    # Your springdroid can detect ground at four distances: one tile away (A),
    # two tiles away (B), three tiles away (C), and four tiles away (D).
    # ground is true, hole is false

    # The "Hard" (but really easy) way:
    # run_part1_brute_force()

    # 
    # 
    # The "actually thinking about the problem way":

    # - If there is a hole directly in front of me, I have to jump. Otherwise,
    #   if there will be a hole in front of me and I can safely land, jump.

    # - A == False is hole directly in front, so I must jump (i.e. Not(A))
    # - A jump takes 4 spaces, so D must be True where we land
    # - If there's a hole in B or C (Or(Not(B), Not(C))) and D is ground (D)

    # - Logically:

    #     !A || ((!B || !C) && D)

    # - To convert this into Springcode, we need to take small pieces, store 
    #   them in `T`, and then go from there:

    #   NOT B T
    #   NOT C J
    #   OR J T
    #   AND D T
    #   NOT A J
    #   OR T J

    instr = ['NOT B T\n',
             'NOT C J\n',
             'OR J T\n',
             'AND D T\n',
             'NOT A J\n',
             'OR T J\n',
             'WALK\n']


    with open('21/input', 'r') as f:
        inp = f.readline()

    c = Computer('spring', inp, debug_level='off')    
    c.run_intcode()
    
    for i in instr:
        input_string(c, i)

    print(c.last_output)

    # Running random permutations of length 4 took about 6 minutes until one
    # worked (running on poole with 12 processors in the pool) (1413720 
    # permutations)
    
    # Answer is 19353565 

    # Brute force solutions:
    # ['NOT C J\n', 'NOT A T\n', 'AND D J\n', 'OR T J\n', 'WALK\n']
    # ['NOT D J\n', 'OR C J\n', 'AND A J\n', 'NOT J J\n', 'WALK\n']
    
    # My solution:
    # ['NOT B T\n', 'NOT C J\n', 'OR J T\n', 'AND D T\n', 'NOT A J\n', 
    #  'OR T J\n', 'WALK\n']