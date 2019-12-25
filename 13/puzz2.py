"""

--- Part Two ---
The game didn't run because you didn't put in any quarters. Unfortunately, you
did not bring any quarters. Memory address 0 represents the number of quarters
that have been inserted; set it to 2 to play for free.

The arcade cabinet has a joystick that can move left and right. The software
reads the position of the joystick with input instructions:

- If the joystick is in the neutral position, provide 0.
- If the joystick is tilted to the left, provide -1.
- If the joystick is tilted to the right, provide 1.

The arcade cabinet also has a segment display capable of showing a single number
that represents the player's current score. When three output instructions
specify X=-1, Y=0, the third output instruction is not a tile; the value instead
specifies the new score to show in the segment display. For example, a sequence
of output values like -1,0,12345 would show 12345 as the player's current score.

Beat the game by breaking all the blocks. What is your score after the last
block is broken?

"""
import itertools
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.animation as animation

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

def chunks(l, n):
    """Break a list l into chunks of size l"""
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield tuple(l[i:i+n])


def tiles_to_board(tiles):
    """tiles is list of 3-tuples"""
    min_x, max_x, min_y, max_y = 1, 0, 1, 0
    
    for t in tiles:
        min_x = min(t[0], min_x)
        max_x = max(t[0], max_x)
        min_y = min(t[1], min_y)
        max_y = max(t[1], max_y)

    x_size = max_x - min_x + 1
    y_size = max_y - min_y + 1

    board = np.zeros((y_size, x_size), dtype=int)

    for t in tiles:
        x, y, val = t
        board[y, x] = val
    
    return board


def render_board(board, fig=None, im=None, ims=None):
    if im is None:
        fig, _ = plt.subplots(1,1)
        im = plt.imshow(board[:, :-1], animated=True)
    else:
        im = plt.imshow(board[:, :-1], animated=True)
        # fig.canvas.draw_idle()
        # plt.pause(.001)

    ims.append([im])

    return fig, im, ims

if __name__ == '__main__':

    with open('13/input', 'r') as f:
        inp = f.readline()

    c = Computer('game', inp, debug_level='off')
    c.mem[0] = 2
    ims = []
    fig, im = None, None
    c.run_intcode()
    iters = 1

    tiles = list(chunks(c.total_output, 3))
    board = tiles_to_board(tiles)
    ball_x = [t for t in tiles if t[2] == 4][0][0]
    paddle_x = [t for t in tiles if t[2] == 3][0][0]
    score = [t for t in tiles if t[0] == -1 and t[1] == 0][-1][0]
    
    fig, im, ims = render_board(board, fig, im, ims)

    while True:
        if paddle_x < ball_x:
            # paddle is left of ball, so move right
            new_inp = 1
        elif paddle_x > ball_x:
            # paddle is right of ball, so move left
            new_inp = -1
        else:
            # paddle is at ball position, so do not move
            new_inp = 0

        if c.cur_opcode == 3:
            c.run_intcode(new_input=new_inp)
            tiles = list(chunks(c.this_runs_output, 3))
            for t in tiles:
                x, y, val = t
                board[y, x] = val
            if iters % 100 == 0:
                print(f'{iters:05g} - Ball: {ball_x} - Paddle: {paddle_x} - Providing input {new_inp} - Score: {score}')
            fig, im, ims = render_board(board, fig, im, ims)
            
            ball_x = np.argwhere(board == 4)[0][1]
            paddle_x = np.argwhere(board == 3)[0][1]
            iters += 1
        else:
            print("Breaking while loop")
            break

    print(f'Final score is {board[0, -1]}')
    
    # This takes a while, so disable by default
    ani = animation.ArtistAnimation(fig, ims, interval=5, blit=True,
                                    repeat_delay=1000)
    ani.save('13/movie_output.mp4')
    # plt.show()
    
    # Answer is 16171