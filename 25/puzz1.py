"""
--- Day 25: Cryostasis ---
As you approach Santa's ship, your sensors report two important details:

First, that you might be too late: the internal temperature is -40 degrees.

Second, that one faint life signature is somewhere on the ship.

The airlock door is locked with a code; your best option is to send in a small
droid to investigate the situation. You attach your ship to Santa's, break a
small hole in the hull, and let the droid run in before you seal it up again.
Before your ship starts freezing, you detach your ship and set it to
automatically stay within range of Santa's ship.

This droid can follow basic instructions and report on its surroundings; you can
communicate with it through an Intcode program (your puzzle input) running on an
ASCII-capable computer.

As the droid moves through its environment, it will describe what it encounters.
When it says Command?, you can give it a single instruction terminated with a
newline (ASCII code 10). Possible instructions are:

- Movement via north, south, east, or west.
- To take an item the droid sees in the environment, use the command take <name
  of item>. For example, if the droid reports seeing a red ball, you can pick it
  up with take red ball.
- To drop an item the droid is carrying, use the command drop <name of item>.
  For example, if the droid is carrying a green ball, you can drop it with drop
  green ball.
- To get a list of all of the items the droid is currently carrying, use the
  command inv (for "inventory").

Extra spaces or other characters aren't allowed - instructions must be provided
precisely.

Santa's ship is a Reindeer-class starship; these ships use pressure-sensitive
floors to determine the identity of droids and crew members. The standard
configuration for these starships is for all droids to weigh exactly the same
amount to make them easier to detect. If you need to get past such a sensor, you
might be able to reach the correct weight by carrying items from the
environment.

Look around the ship and see if you can find the password for the main airlock.
"""
import sys
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

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

            self.dbg_print(f'{self.name}:', space='\n')
            self.dbg_print(f'({self.pos:04g})', space='\t')
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

def go_direction(direction, print=True):
    input_string(c, f'{direction}\n', print=True)
    if print: print_output(c.this_runs_output)

def take_item(item, print=True):
    input_string(c, f'take {item}\n', print=True)
    if print: print_output(c.this_runs_output)

def drop_item(item, print=True):
    input_string(c, f'drop {item}\n', print=True)
    if print: print_output(c.this_runs_output)

def print_inv():
    input_string(c, f'inv\n', print=True)
    if print: print_output(c.this_runs_output)

import re
def get_room_name():
    return re.findall('(?<=\n\n\n== )(.*)(?= ==\n)', 
                      get_output(c.this_runs_output))[0]

def get_possible_dirs():
    dirs = []
    for d in ['north', 'south', 'east', 'west']: 
        if f'- {d}' in get_output(c.this_runs_output):
            dirs.append(d)
    return dirs

def get_items_here():
    out = get_output(c.this_runs_output)
    items_idx = out.find('Items here:')
    command_idx = out.find('Command?')
    if items_idx > -1:
        out = out[items_idx+12:command_idx]
        items = re.findall('(?<=- )(.*)(?=\n)',out)
    else:
        items = None
    return items

BACKTRACK = {
    'south': 'north',
    'north': 'south',
    'east': 'west', 
    'west': 'east'
}


def search(G):

    dirs = get_possible_dirs()

    adj_rooms = []

    for d in get_possible_dirs():
        go_direction(d)
        next_room = get_room_name()
        items = get_items_here()
        G.add_node(next_room)
        G.add_edge(this_room, next_room)
        go_direction(BACKTRACK[d])

    name = get_room_name()

    if name == 'Security Checkpoint':
        print('Found security checkpoint')
        return True
    elif len(dirs) == 1:
        print('reached deadend')
        return False
    elif name in G.graph['visited']:
        print('already visited')
        return False
     
    # mark as visited
    G.add_node(name)

    # explore neighbors clockwise starting by the one on the right
    if ((x < len(grid)-1 and search(x+1, y))
        or (y > 0 and search(x, y-1))
        or (x > 0 and search(x-1, y))
        or (y < len(grid)-1 and search(x, y+1))):
        return True
    
    return False


def go_to_checkpoint():
    # hull breach
    go_direction('east', print=True) # [east, south, west]
    # engineering
    go_direction('east', True)
    # sick bay
    go_direction('south', True)
    # crew quarters
    go_direction('west', True) # [west, east]
    # warp drive maint
    go_direction('south', True)
    # observatory
    go_direction('west', True)
    # gift wrapping center
    go_direction('south', True)


def go_to_kitchen():
    # hull breach
    go_direction('east', print=True) # [east, south, west]
    # engineering
    go_direction('east', True)
    # sick bay
    go_direction('south', True)
    # crew quarters
    go_direction('east', True)
    # hot chocolate fountain
    # go_direction('south', True)
    go_direction('north', True)
    go_direction('west', True)


def go_to_corridor():
    # hull breach
    go_direction('east', print=True) # [east, south, west]
    # engineering
    go_direction('east', True)
    # sick bay
    go_direction('south', True)
    # crew quarters
    go_direction('east', True)
    # hot chocolate fountain
    go_direction('south', True)


def go_to_science_lab():
    go_direction('south', True)  


def go_to_arcade():
    go_direction('west', True)
    go_direction('south', True)
    go_direction('east', True)

def go_to_storage():
    go_direction('west', True)
    go_direction('south', True)
    go_direction('south', True)

def get_all_items(print_output=False):
    go_direction('west', print_output)
    go_direction('west', print_output)
    # take_item('giant electromagnet', print_output)
    go_direction('north', print_output)
    take_item('space heater', print_output)
    go_direction('south', print_output)
    go_direction('east', print_output)
    go_direction('south', print_output)
    take_item('festive hat', print_output)
    go_direction('south', print_output)
    take_item('sand', print_output)
    go_direction('north', print_output)
    go_direction('east', print_output)
    take_item('whirled peas', print_output)
    go_direction('west', print_output)
    go_direction('north', print_output)
    go_direction('east', print_output)

    go_direction('south', print_output)
    take_item('weather machine', print_output)
    go_direction('north', print_output)

    go_direction('east', print_output)
    take_item('mug', print_output)
    go_direction('east', print_output)
    # take_item('escape pod', print_output)
    go_direction('south', print_output)
    go_direction('east', print_output)
    # take_item('photons', print_output)
    go_direction('south', print_output)
    take_item('easter egg', print_output)
    go_direction('north', print_output)
    go_direction('north', print_output)
    # take_item('molten lava', print_output)
    go_direction('west', print_output)
    go_direction('east', print_output)
    go_direction('south', print_output)
    go_direction('west', print_output)
    go_direction('west', print_output)
    go_direction('south', print_output)
    # take_item('infinite loop', print_output)
    go_direction('west', print_output)
    take_item('shell', print_output)
    go_direction('south', print_output)

def all_combinations(any_list):
    return itertools.chain.from_iterable(
        itertools.combinations(any_list, i + 1)
        for i in range(len(any_list)))


if __name__ == '__main__':

    with open('25/input', 'r') as f:
        inp = f.readline()

    G = nx.Graph()

    c = Computer('droid', inp, debug_level='off')
    c.run_intcode()
    # print_output(c.this_runs_output)
    
    this_room = get_room_name()
    get_items_here()
    G.add_node(this_room)
    G.graph['cur_node'] = this_room
    G.graph['queue'] = deque()


    # search(G)

    # for d in get_possible_dirs():
    #     go_direction(d)
    #     next_room = get_room_name()
    #     get_items_here()
    #     G.add_node(next_room)
    #     G.add_edge(this_room, next_room)
    #     go_direction(BACKTRACK[d])

    # nx.draw(G, with_labels=True)
    # plt.show()

    # go_to_checkpoint()
    # go_to_kitchen()
    # go_to_corridor()
    # go_to_science_lab()
    # go_to_arcade()

    get_all_items()
    all_items = ['space heater', 'festive hat', 'sand', 'whirled peas', 
                 'weather machine', 'mug', 'easter egg', 'shell']

    # finding out what combination of items to drop:
    # import itertools
    # for comb in all_combinations(all_items):
    #     print(f'dropping {comb}')
    #     if get_items_here() is not None:
    #         for it in get_items_here():    # pick up all items that are here
    #             take_item(it, False)
    #     for it in comb:
    #         drop_item(it, False)
    #     go_direction('south', True)
    #     if 'Alert' not in get_output(c.this_runs_output):
    #         print_inv()
    #         break

    for it in ('festive hat', 'whirled peas', 'weather machine', 'shell'):
        drop_item(it, False)
    
    # Items that will get you through door:
    # easter egg, mug, sand, space heater

    go_direction('south', False)
    
    # Answer is 2424308736