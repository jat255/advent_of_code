"""
--- Day 7: Amplification Circuit ---

Based on the navigational maps, you're going to need to send more power to your
ship's thrusters to reach Santa in time. To do this, you'll need to configure a
series of amplifiers already installed on the ship.

There are five amplifiers connected in series; each one receives an input signal
and produces an output signal. They are connected such that the first
amplifier's output leads to the second amplifier's input, the second amplifier's
output leads to the third amplifier's input, and so on. The first amplifier's
input value is 0, and the last amplifier's output leads to your ship's
thrusters.

    O-------O  O-------O  O-------O  O-------O  O-------O
0 ->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-> (to thrusters)
    O-------O  O-------O  O-------O  O-------O  O-------O

The Elves have sent you some Amplifier Controller Software (your puzzle input),
a program that should run on your existing Intcode computer. Each amplifier will
need to run a copy of the program.

When a copy of the program starts running on an amplifier, it will first use an
input instruction to ask the amplifier for its current phase setting (an integer
from 0 to 4). Each phase setting is used exactly once, but the Elves can't
remember which amplifier needs which phase setting.

The program will then call another input instruction to get the amplifier's
input signal, compute the correct output signal, and supply it back to the
amplifier with an output instruction. (If the amplifier has not yet received an
input signal, it waits until one arrives.)

Your job is to find the largest output signal that can be sent to the thrusters
by trying every possible combination of phase settings on the amplifiers. Make
sure that memory is not shared or reused between copies of the program.

For example, suppose you want to try the phase setting sequence 3,1,2,4,0, which
would mean setting amplifier A to phase setting 3, amplifier B to setting 1, C
to 2, D to 4, and E to 0. Then, you could determine the output signal that gets
sent from amplifier E to the thrusters with the following steps:

- Start the copy of the amplifier controller software that will run on amplifier
  A. At its first input instruction, provide it the amplifier's phase setting,
  3. At its second input instruction, provide it the input signal, 0. After some
     calculations, it will use an output instruction to indicate the amplifier's
     output signal.
- Start the software for amplifier B. Provide it the phase setting (1) and then
  whatever output signal was produced from amplifier A. It will then produce a
  new output signal destined for amplifier C.
- Start the software for amplifier C, provide the phase setting (2) and the
  value from amplifier B, then collect its output signal.
- Run amplifier D's software, provide the phase setting (4) and input value, and
  collect its output signal.
- Run amplifier E's software, provide the phase setting (0) and input value, and
  collect its output signal.

The final output signal from amplifier E would be sent to the thrusters.
However, this phase setting sequence may not have been the best one; another
sequence might have sent a higher signal to the thrusters.

Here are some example programs:

- Max thruster signal 43210 (from phase setting sequence 4,3,2,1,0):

    3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0 

- Max thruster signal 54321 (from phase setting sequence 0,1,2,3,4):

    3,23,3,24,1002,24,10,24,1002,23,-1,23, 101,5,23,23,1,24,23,23,4,23,99,0,0

- Max thruster signal 65210 (from phase setting sequence 1,0,4,3,2):

    3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
    1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0 

Try every combination of phase settings on the amplifiers. What is the highest
signal that can be sent to the thrusters?
"""

import itertools

class Computer():
    def __init__(self, inp, phase_setting, input_code):
        self.mem = [int(i) for i in inp.split(',')]
        self.input_stack = [phase_setting, input_code]
        self.output = None


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


    def run_intcode(self):
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
            jumped = False
            # print(f'self.iteration {self.iteration}')
            # print(f'self.pos: {self.pos}; opcode: {opcode}; inp: {self.mem}')


            if opcode == 99:
                break

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
                self.mem[params[2]] = params[0] + params[1]
            elif opcode == 2:
                # multiply values of first two parameters and store in third param
                nparams = 3
                params = Computer.parse_param_modes(param_int, nparams, 
                                                    self.pos, self.mem)
                self.mem[params[2]] = params[0] * params[1]
            elif opcode == 3:
                # take input from user and store at postion of only parameter
                nparams = 1
                if len(self.input_stack) > 0:
                    input_code = int(self.input_stack.pop(0))
                else:
                    # we've run out of inputs, so we have to pause and wait
                    # for the 
                    input_code = int(input('Enter program input: '))
                self.mem[self.mem[self.pos+1]] = input_code
            elif opcode == 4:
                # output value of the only parameter
                nparams = 1
                params = Computer.parse_param_modes(param_int, nparams, 
                                                    self.pos, self.mem)
                print(f'OUTPUT: {params[0]}')
                self.last_output = params[0]
            elif opcode == 5:
                nparams = 2
                params = Computer.parse_param_modes(param_int, nparams, 
                                                    self.pos, self.mem)
                if params[0] != 0:
                    self.pos = params[1]
                    jumped = True
            elif opcode == 6:
                nparams = 2
                params = Computer.parse_param_modes(param_int, nparams, 
                                                    self.pos, self.mem)
                if params[0] == 0:
                    self.pos = params[1]
                    jumped = True
            elif opcode == 7:
                nparams = 3
                params = Computer.parse_param_modes(param_int, nparams, 
                                                    self.pos, self.mem)
                if params[0] < params[1]:
                    self.mem[params[2]] = 1
                else:
                    self.mem[params[2]] = 0
            elif opcode == 8:
                nparams = 3
                params = Computer.parse_param_modes(param_int, nparams, 
                                                    self.pos, self.mem)
                if params[0] == params[1]:
                    self.mem[params[2]] = 1
                else:
                    self.mem[params[2]] = 0
            
            if not jumped:
                self.pos += nparams + 1
            
            self.iteration += 1

        self.output = self.last_output


def run_sequence(inp, phase_codes):
    A = Computer(inp, phase_codes[0], 0); A.run_intcode()
    B = Computer(inp, phase_codes[1], A.output); B.run_intcode()
    C = Computer(inp, phase_codes[2], B.output); C.run_intcode()
    D = Computer(inp, phase_codes[3], C.output); D.run_intcode()
    E = Computer(inp, phase_codes[4], D.output); E.run_intcode()
    
    # print(E.output, type(E.output))

    return E.output


if __name__ == '__main__':

    with open('07/input', 'r') as f:
        inp = f.readline()
    
    assert run_sequence('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', 
                        [4,3,2,1,0]) == 43210
    assert run_sequence('3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,' +
                        '23,1,24,23,23,4,23,99,0,0', [0,1,2,3,4]) == 54321
    assert run_sequence('3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,' +
                        '1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0',
                        [1,0,4,3,2]) == 65210

    results = {}

    for curr_phase_setting in itertools.permutations(range(5)):
        # print(f'Current phase settings: {curr_phase_setting}')
        phase_string = ''.join([str(i) for i in curr_phase_setting])
        results[phase_string] = run_sequence(inp, curr_phase_setting)
    
    print(f'Max signal is for phase setting ({max(results, key=results.get)}) '
          f'and is {results[max(results, key=results.get)]}')

# Answer is 46248