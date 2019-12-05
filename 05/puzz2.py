"""
--- Part Two ---

The air conditioner comes online! Its cold air feels good for a while, but then
the TEST alarms start to go off. Since the air conditioner can't vent its heat
anywhere but back into the spacecraft, it's actually making the air inside the
ship warmer.

Instead, you'll need to use the TEST to extend the thermal radiators.
Fortunately, the diagnostic program (your puzzle input) is already equipped for
this. Unfortunately, your Intcode computer is not.

Your computer is only missing a few opcodes:

- Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the
  instruction pointer to the value from the second parameter. Otherwise, it does
  nothing.
- Opcode 6 is jump-if-false: if the first parameter is zero, it sets the
  instruction pointer to the value from the second parameter. Otherwise, it does
  nothing.
- Opcode 7 is less than: if the first parameter is less than the second
  parameter, it stores 1 in the position given by the third parameter.
  Otherwise, it stores 0.
- Opcode 8 is equals: if the first parameter is equal to the second parameter,
  it stores 1 in the position given by the third parameter. Otherwise, it stores
  0. 
  
Like all instructions, these instructions need to support parameter modes as
described above.

Normally, after an instruction is finished, the instruction pointer increases by
the number of values in that instruction. However, if the instruction modifies
the instruction pointer, that value is used and the instruction pointer is not
automatically increased.

For example, here are several programs that take one input, compare it to the
value 8, and then produce one output:

- 3,9,8,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input is
  equal to 8; output 1 (if it is) or 0 (if it is not).
- 3,9,7,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input is
  less than 8; output 1 (if it is) or 0 (if it is not).
- 3,3,1108,-1,8,3,4,3,99 - Using immediate mode, consider whether the input is
  equal to 8; output 1 (if it is) or 0 (if it is not).
- 3,3,1107,-1,8,3,4,3,99 - Using immediate mode, consider whether the input is
  less than 8; output 1 (if it is) or 0 (if it is not). Here are some jump tests
  that take an input, then output 0 if the input was zero or 1 if the input was
  non-zero:

- 3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9 (using position mode)
- 3,3,1105,-1,9,1101,0,0,12,4,12,99,1 (using immediate mode)

Here's a larger example:

3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99

The above example program uses an input instruction to ask for a single number.
The program will then output 999 if the input value is below 8, output 1000 if
the input value is equal to 8, or output 1001 if the input value is greater than
8.

This time, when the TEST diagnostic program runs its input instruction to get
the ID of the system to test, provide it 5, the ID for the ship's thermal
radiator controller. This diagnostic test suite only outputs one number, the
diagnostic code.

What is the diagnostic code for system ID 5?
"""


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


def run_intcode(inp, user_input=None):
    """
    inp : str
        The comma-separated string of inputs
    user_input : None or str
        If None, opcode 3 will ask the user for an input, otherwise user_input 
        is used
    """
    pos = 0
    iteration = 1
    last_output = None
    inp = [int(i) for i in inp.split(',')]
    # print(f'iteration {iteration}: {inp}')

    # opcode 1 means add; opcode 2 means multiply
    # next three numbers are first input index, second input index, and index to
    # write to
    
    # opcode 3 means take an input and save it to position
    # opcode 4 means output (print) the parameter
    while True:
        opcode = inp[pos]
        param_int = None
        jumped = False
        # print(f'iteration {iteration}')
        # print(f'pos: {pos}; opcode: {opcode}; inp: {inp}')


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
            params = parse_param_modes(param_int, nparams, pos, inp)
            inp[params[2]] = params[0] + params[1]
        elif opcode == 2:
            # multiply values of first two parameters and store in third param
            nparams = 3
            params = parse_param_modes(param_int, nparams, pos, inp)
            inp[params[2]] = params[0] * params[1]
        elif opcode == 3:
            # take input from user and store at postion of only parameter
            nparams = 1
            if user_input:
                input_code = int(user_input)
            else:
                input_code = int(input('Enter program input: '))
            inp[inp[pos+1]] = input_code
        elif opcode == 4:
            # output value of the only parameter
            nparams = 1
            params = parse_param_modes(param_int, nparams, pos, inp)
            print(f'OUTPUT: {params[0]}')
            last_output = params[0]
        elif opcode == 5:
            nparams = 2
            params = parse_param_modes(param_int, nparams, pos, inp)
            if params[0] != 0:
                pos = params[1]
                jumped = True
        elif opcode == 6:
            nparams = 2
            params = parse_param_modes(param_int, nparams, pos, inp)
            if params[0] == 0:
                pos = params[1]
                jumped = True
        elif opcode == 7:
            nparams = 3
            params = parse_param_modes(param_int, nparams, pos, inp)
            if params[0] < params[1]:
                inp[params[2]] = 1
            else:
                inp[params[2]] = 0
        elif opcode == 8:
            nparams = 3
            params = parse_param_modes(param_int, nparams, pos, inp)
            if params[0] == params[1]:
                inp[params[2]] = 1
            else:
                inp[params[2]] = 0
        
        if not jumped:
            pos += nparams + 1
        
        iteration += 1
    return last_output


if __name__ == '__main__':

    print('Running tests:\n--------------')

    # Testing equal to 8 (position mode):
    assert run_intcode('3,9,8,9,10,9,4,9,99,-1,8', '8') == 1
    assert run_intcode('3,9,8,9,10,9,4,9,99,-1,8', '1') == 0
    assert run_intcode('3,9,8,9,10,9,4,9,99,-1,8', '40') == 0

    # Testing less than 8 (position mode):
    assert run_intcode('3,9,7,9,10,9,4,9,99,-1,8', '8') == 0
    assert run_intcode('3,9,7,9,10,9,4,9,99,-1,8', '1') == 1
    assert run_intcode('3,9,7,9,10,9,4,9,99,-1,8', '40') == 0

    # Testing equal to 8 (immediate mode):
    assert run_intcode('3,3,1108,-1,8,3,4,3,99', '8') == 1
    assert run_intcode('3,3,1108,-1,8,3,4,3,99', '1') == 0
    assert run_intcode('3,3,1108,-1,8,3,4,3,99', '40') == 0

    # Testing less than 8 (immediate mode):
    assert run_intcode('3,3,1107,-1,8,3,4,3,99', '8') == 0
    assert run_intcode('3,3,1107,-1,8,3,4,3,99', '1') == 1
    assert run_intcode('3,3,1107,-1,8,3,4,3,99', '40') == 0

    # Testing input was zero (position mode) with jumps:
    assert run_intcode('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', '0') == 0
    assert run_intcode('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', '1') == 1
    assert run_intcode('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', '100') == 1

    # Testing input was zero (immediate mode) with jumps:
    assert run_intcode('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', '0') == 0
    assert run_intcode('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', '1') == 1
    assert run_intcode('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', '100') == 1

    # Larger test:
    inp = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,' + \
          '1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,' + \
          '999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'
    assert run_intcode(inp, '0') == 999
    assert run_intcode(inp, '7') == 999
    assert run_intcode(inp, '8') == 1000
    assert run_intcode(inp, '9') == 1001
    assert run_intcode(inp, '500') == 1001
    
    print('\n\nRunning real program:\n---------------------')

    with open('05/input', 'r') as f:
        inp = f.readline()
    
    run_intcode(inp, '5')

    # Answer is 3892695
