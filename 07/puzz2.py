"""
--- Part Two ---
It's no good - in this configuration, the amplifiers can't generate a large
enough output signal to produce the thrust you'll need. The Elves quickly talk
you through rewiring the amplifiers into a feedback loop:

      O-------O  O-------O  O-------O  O-------O  O-------O
0 -+->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-.
   |  O-------O  O-------O  O-------O  O-------O  O-------O |
   |                                                        |
   '--------------------------------------------------------+
                                                            |
                                                            v
                                                     (to thrusters)

Most of the amplifiers are connected as they were before; amplifier A's output
is connected to amplifier B's input, and so on. However, the output from
amplifier E is now connected into amplifier A's input. This creates the feedback
loop: the signal will be sent through the amplifiers many times.

In feedback loop mode, the amplifiers need totally different phase settings:
integers from 5 to 9, again each used exactly once. These settings will cause
the Amplifier Controller Software to repeatedly take input and produce output
many times before halting. Provide each amplifier its phase setting at its first
input instruction; all further input/output instructions are for signals.

Don't restart the Amplifier Controller Software on any amplifier during this
process. Each one should continue receiving and sending signals until it halts.

All signals sent or received in this process will be between pairs of amplifiers
except the very first signal and the very last signal. To start the process, a 0
signal is sent to amplifier A's input exactly once.

Eventually, the software on the amplifiers will halt after they have processed
the final loop. When this happens, the last output signal from amplifier E is
sent to the thrusters. Your job is to find the largest output signal that can be
sent to the thrusters using the new phase settings and feedback loop
arrangement.

Here are some example programs:

- Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5):

    3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
    27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5

- Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6):

    3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
    -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
    53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10

Try every combination of the new phase settings on the amplifier feedback loop.
What is the highest signal that can be sent to the thrusters?
"""

import itertools

class Computer():
    def __init__(self, name, inp, phase_setting, input_code):
        self.name = name
        self.mem = [int(i) for i in inp.split(',')]
        self.input_stack = [phase_setting, input_code]
        self.output = None
        self.output_pos = None

    @staticmethod
    def parse_param_modes(param_int, nparams, pos, inp):
        params = [0] * nparams
        if param_int:
            param_str = f'{param_int:0{nparams}g}'
        else:
            param_str = '0' * nparams
        for i, mode in enumerate(param_str[::-1]):
            # print(i, mode)
            param_val = inp[pos + i + 1]
            if int(mode) == 0:
                # position mode, so value is position in memory of parameter
                if i < 2:
                    params[i] = inp[param_val]
                else:
                    # unless it's the output value, then it's just the position
                    params[i] = param_val
            elif int(mode) == 1:
                # immediate mode, so value is just the parameter
                params[i] = param_val
            else:
                raise ValueError('Parameter mode should be either 0 or 1')
        return params

    
    def print_mem_array(self):
        print('indx: ', end='')
        for num in range(len(self.mem)):
            print(f'{num:4g} ', end='')
        print('')
        print('vals: ', end='')
        for num in self.mem:
            print(f'{num:4g} ', end='')
        print('')


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
        # print(f'self.iteration {self.iteration}: {self.mem}')

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
            # print(f'self.iteration {self.iteration}')
            # print(f'{self.name}, self.pos: {self.pos}; opcode: {opcode}; \ninp_stack: {self.input_stack};')
            # print(f'Last output position was {self.output_pos} with value {self.output}')
            # self.print_mem_array()


            if opcode == 99:
                # print(self.name, self.mem)
                return 'DONE'

            if opcode > 9:
                # we have more than two digits, so split opcode and parameters
                reduced_opcode = int(str(opcode)[-2:])
                param_int = int(str(opcode)[:-2])
                opcode = reduced_opcode

            if opcode == 1:
                # add values of first two parameters and store in third param
                nparams = 3
                params = Computer.parse_param_modes(param_int, nparams, 
                                                    self.pos, self.mem)
                # print(f'params: {params}')
                self.mem[params[2]] = params[0] + params[1]
            elif opcode == 2:
                # multiply values of first two parameters and store in third param
                nparams = 3
                params = Computer.parse_param_modes(param_int, nparams, 
                                                    self.pos, self.mem)
                # print(f'params: {params}')
                self.mem[params[2]] = params[0] * params[1]
            elif opcode == 3:
                # take input from user and store at postion of only parameter
                nparams = 1
                if len(self.input_stack) > 0:
                    input_code = int(self.input_stack.pop(0))
                else:
                    if new_input:
                        # print(f'{self.name} GOT INPUT {new_input}')
                        input_code = int(new_input)
                        # make sure to clear new_input, so we don't think we
                        # got another input the next time we see an opcode 3                        
                        new_input = None
                    # we've run out of inputs, so we have to pause and wait
                    # for the program to continue with a new input
                    # Return None to indicate that we're not done yet
                    else:
                        self.output = self.last_output
                        # print(f'{self.name} is PAUSING FOR NEXT INPUT at pos {self.pos};'
                        #       f'last output was: {self.output}')
                        return None
                # print(f'Param num is {self.pos+1}')
                # print(f'Param val (mem num to set) is {self.mem[self.pos+1]}')
                # print(f'Setting position {self.mem[self.pos+1]} to {input_code}')
                self.mem[self.mem[self.pos+1]] = input_code
            elif opcode == 4:
                # output value of the only parameter
                nparams = 1
                params = Computer.parse_param_modes(param_int, nparams, 
                                                    self.pos, self.mem)
                # print(f'params: {params}')                                                    
                self.last_output = params[0]
                self.output_pos = self.pos
                # print(f'{self.name} OUTPUT at pos {self.output_pos}: {self.last_output}')
                self.output = self.last_output
            elif opcode == 5:
                nparams = 2
                params = Computer.parse_param_modes(param_int, nparams, 
                                                    self.pos, self.mem)
                # print(f'params: {params}')
                if params[0] != 0:
                    self.pos = params[1]
                    jumped = True
            elif opcode == 6:
                nparams = 2
                params = Computer.parse_param_modes(param_int, nparams, 
                                                    self.pos, self.mem)
                # print(f'params: {params}')
                if params[0] == 0:
                    self.pos = params[1]
                    jumped = True
            elif opcode == 7:
                nparams = 3
                params = Computer.parse_param_modes(param_int, nparams, 
                                                    self.pos, self.mem)
                # print(f'params: {params}')
                if params[0] < params[1]:
                    self.mem[params[2]] = 1
                else:
                    self.mem[params[2]] = 0
            elif opcode == 8:
                nparams = 3
                params = Computer.parse_param_modes(param_int, nparams, 
                                                    self.pos, self.mem)
                # print(f'params: {params}')
                if params[0] == params[1]:
                    self.mem[params[2]] = 1
                else:
                    self.mem[params[2]] = 0
            
            if not jumped:
                self.pos += nparams + 1
            
            self.iteration += 1

            # print('\n')
        self.output = self.last_output


def run_sequence(inp, phase_codes):
    itr = 0

    # print(f'Iter: {itr}')
    A = Computer('A', inp, phase_codes[0], 0); A.run_intcode()
    # print('A', A.output, A.pos, A.iteration)
    B = Computer('B', inp, phase_codes[1], A.output); B.run_intcode()
    # print('B', B.output, B.pos, B.iteration)
    C = Computer('C', inp, phase_codes[2], B.output); C.run_intcode()
    # print('C', C.output, C.pos, C.iteration)
    D = Computer('D', inp, phase_codes[3], C.output); D.run_intcode()
    # print('D', D.output, D.pos, D.iteration)
    E = Computer('E', inp, phase_codes[4], D.output); E.run_intcode()
    # print('E', E.output, E.pos, E.iteration)
    
    while True:
        itr += 1
        # print(f'\nIter: {itr}')
        A_res = A.run_intcode(E.output)
        B_res = B.run_intcode(A.output)
        C_res = C.run_intcode(B.output)
        D_res = D.run_intcode(C.output)
        E_res = E.run_intcode(D.output)
        
        # print('A_res', A_res, A.output, A.pos, A.iteration)
        # print('B_res', B_res, B.output, B.pos, B.iteration)
        # print('C_res', C_res, C.output, C.pos, C.iteration)
        # print('D_res', D_res, D.output, D.pos, D.iteration)
        # print('E_res', E_res, E.output, E.pos, E.iteration)
        
        if E_res == 'DONE': 
            break

    # for m in [A,B,C,D,E]:
    #     print(m.name, m.output)

    return E.output


if __name__ == '__main__':

    with open('07/input', 'r') as f:
        inp = f.readline()
    
    
    assert run_sequence('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,' +
                        '27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5', 
                        [9,8,7,6,5]) == 139629729

    results = {}

    for curr_phase_setting in itertools.permutations(range(5, 10)):
        print(f'Current phase settings: {curr_phase_setting}')
        phase_string = ''.join([str(i) for i in curr_phase_setting])
        results[phase_string] = run_sequence(inp, curr_phase_setting)
    
    print(f'Max signal is for phase setting ({max(results, key=results.get)}) '
          f'and is {results[max(results, key=results.get)]}')

# Answer is 54163586