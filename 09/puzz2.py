"""
--- Part Two ---
You now have a complete Intcode computer.

Finally, you can lock on to the Ceres distress signal! You just need to boost
your sensors using the BOOST program.

The program runs in sensor boost mode by providing the input instruction the
value 2. Once run, it will boost the sensors automatically, but it might take a
few seconds to complete the operation on slower hardware. In sensor boost mode,
the program will output a single value: the coordinates of the distress signal.

Run the BOOST program in sensor boost mode. What are the coordinates of the
distress signal? 
"""

import itertools

class Computer():
    def __init__(self, name, inp, phase_setting=None, input_code=None):
        self.name = name
        self.mem = [int(i) for i in inp.split(',')] + \
            [0]*len(inp.split(','))*100
        self.input_stack = []
        if phase_setting:
            self.input_stack += [phase_setting]
        if input_code:
            self.input_stack += [input_code]
        self.rel_base = 0
        self.output = None
        self.output_pos = None
        self.cur_opcode = None
        self.total_output = []


    def parse_param_modes(self, param_int, nparams):
        params = [0] * nparams
        if param_int:
            param_str = f'{param_int:0{nparams}g}'
        else:
            param_str = '0' * nparams
        for i, mode in enumerate(param_str[::-1]):
            # print(i, mode)
            param_val = self.mem[self.pos + i + 1]
            if int(mode) == 0:
                # position mode, so value is position in memory of parameter
                if i < 2:
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
                if i < 2 and self.cur_opcode != 3:
                    params[i] = self.mem[param_val + self.rel_base]
                else:
                    # unless it's the output value, then it's just the position 
                    # (this is immediate mode)
                    params[i] = param_val + self.rel_base
            else:
                raise ValueError('Parameter mode should be either 0 or 1')
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
            # print(f'Last output position was {self.output_pos} with value {self.output}')
            # self.print_mem_array()


            if opcode == 99:
                # print(self.name, self.mem)
                return self.total_output

            if opcode > 9:
                # we have more than two digits, so split opcode and parameters
                reduced_opcode = int(str(opcode)[-2:])
                param_int = int(str(opcode)[:-2])
                opcode = reduced_opcode

            self.cur_opcode = opcode

            # print(f'self.iteration {self.iteration}')
            # print(f'{self.name}, self.pos: {self.pos}; param_int: {param_int}; opcode: {opcode}; \ninp_stack: {self.input_stack};')

            if opcode == 1:
                # add values of first two parameters and store in third param
                nparams = 3
                params = self.parse_param_modes(param_int, nparams)
                # print(f'params: {params}')
                self.mem[params[2]] = params[0] + params[1]
            elif opcode == 2:
                # multiply values of first two parameters and store in third param
                nparams = 3
                params = self.parse_param_modes(param_int, nparams)
                # print(f'params: {params}')
                self.mem[params[2]] = params[0] * params[1]
            elif opcode == 3:
                # take input from user and store at postion of only parameter
                nparams = 1
                params = self.parse_param_modes(param_int, nparams)
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
                        print(f'{self.name} is PAUSING FOR NEXT INPUT at pos {self.pos};'
                              f'last output was: {self.output}')
                        return None
                # print(f'Param num is {self.pos+1}')
                # print(f'Param val (mem num to set) is {self.mem[self.pos+1]}')
                # print(f'Setting position {self.mem[self.pos+1]} to {input_code}')
                self.mem[params[0]] = input_code
            elif opcode == 4:
                # output value of the only parameter
                nparams = 1
                params = self.parse_param_modes(param_int, nparams)
                # print(f'params: {params}')                                                    
                self.last_output = params[0]
                self.output_pos = self.pos
                # print(f'{self.name} OUTPUT at pos {self.output_pos}: {self.last_output}')
                self.output = self.last_output
                self.total_output += [self.last_output]
            elif opcode == 5:
                nparams = 2
                params = self.parse_param_modes(param_int, nparams)
                # print(f'params: {params}')
                if params[0] != 0:
                    self.pos = params[1]
                    jumped = True
            elif opcode == 6:
                nparams = 2
                params = self.parse_param_modes(param_int, nparams)
                # print(f'params: {params}')
                if params[0] == 0:
                    self.pos = params[1]
                    jumped = True
            elif opcode == 7:
                nparams = 3
                params = self.parse_param_modes(param_int, nparams)
                # print(f'params: {params}')
                if params[0] < params[1]:
                    self.mem[params[2]] = 1
                else:
                    self.mem[params[2]] = 0
            elif opcode == 8:
                nparams = 3
                params = self.parse_param_modes(param_int, nparams)
                # print(f'params: {params}')
                if params[0] == params[1]:
                    self.mem[params[2]] = 1
                else:
                    self.mem[params[2]] = 0
            elif opcode == 9:
                nparams = 1
                params = self.parse_param_modes(param_int, nparams)
                self.rel_base += params[0]
            
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

    with open('09/input', 'r') as f:
        inp = f.readline()
    
    # test_inp1 = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
    # test1 = Computer('test1', test_inp1); 
    # assert ','.join([str(i) for i in test1.run_intcode()]) == test_inp1

    # test_inp2 = '1102,34915192,34915192,7,4,7,99,0'
    # test2 = Computer('test2', test_inp2)
    # assert len(str(test2.run_intcode()[-1])) == 16

    # test_inp3 = '104,1125899906842624,99'
    # test3 = Computer('test3', test_inp3)
    # assert test3.run_intcode()[-1] == 1125899906842624

    comp = Computer('actual_run', inp, input_code=2)
    res = comp.run_intcode()
    print(res)

# Answer is 86025