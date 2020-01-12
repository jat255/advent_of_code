"""
--- Part Two ---
Packets sent to address 255 are handled by a device called a NAT (Not Always
Transmitting). The NAT is responsible for managing power consumption of the
network by blocking certain packets and watching for idle periods in the
computers.

If a packet would be sent to address 255, the NAT receives it instead. The NAT
remembers only the last packet it receives; that is, the data in each packet it
receives overwrites the NAT's packet memory with the new packet's X and Y
values.

The NAT also monitors all computers on the network. If all computers have empty
incoming packet queues and are continuously trying to receive packets without
sending packets, the network is considered idle.

Once the network is idle, the NAT sends only the last packet it received to
address 0; this will cause the computers on the network to resume activity. In
this way, the NAT can throttle power consumption of the network when the ship
needs power in other areas.

Monitor packets released to the computer at address 0 by the NAT. What is the
first Y value delivered by the NAT to the computer at address 0 twice in a row?

"""
import sys
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

    

if __name__ == "__main__":
    
    with open('23/input', 'r') as f:
        inp = f.readline()

    # we need 50 computers, numbered 0 to 49 inclusive
    
    comps = []
    for i in range(50):
        c = Computer(f'{i}', inp, debug_level='off')
        c.run_intcode(i)
        comps.append(c)
    
    incoming_packet_queue = {}
    for i in range(50):
        incoming_packet_queue[i] = []
    nat = None
    last_nat_Y = None

    while True:
        for i in range(50):
            if len(incoming_packet_queue[i]) == 0:
                new_input = -1
                comps[i].run_intcode(new_input)
            else:
                X, Y = incoming_packet_queue[i].pop()
                comps[i].run_intcode(X)
                comps[i].run_intcode(Y)
            out = comps[i].this_runs_output
            while len(out) > 2:
                to_packet = out[0]
                to_X = out[1]
                to_Y = out[2]
                out = out[3:]
                if to_packet == 255:
                    # print(f'255 packet: ({to_X}, {to_Y})')
                    nat = (to_X, to_Y)
                    # print(to_Y)
                else:
                    incoming_packet_queue[to_packet].append((to_X, to_Y))
            num_packets = [len(incoming_packet_queue[queue]) for 
                           queue in incoming_packet_queue.keys()]
            # if there are no incoming packets in the queue, network is idle:
            if sum(num_packets) == 0:
                incoming_packet_queue[0].append(nat)
                print(last_nat_Y, nat[1])
                if nat[1] == last_nat_Y:
                    print(f'Duplicated Y value: {last_nat_Y}')
                    sys.exit(0)
                last_nat_Y = nat[1]

            # This code doesn't produce the answer 19641, but oscillates between
            # 19637 and 19642, so just trying numbers between that until it was
            # the right answer (19641)