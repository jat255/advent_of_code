"""
--- Day 5: Sunny with a Chance of Asteroids ---

You're starting to sweat as the ship makes its way toward Mercury. The Elves
suggest that you get the air conditioner working by upgrading your ship computer
to support the Thermal Environment Supervision Terminal.

The Thermal Environment Supervision Terminal (TEST) starts by running a
diagnostic program (your puzzle input). The TEST diagnostic program will run on
your existing Intcode computer after a few modifications:

First, you'll need to add two new instructions:

- Opcode 3 takes a single integer as input and saves it to the address given by
  its only parameter. For example, the instruction 3,50 would take an input
  value and store it at address 50.
- Opcode 4 outputs the value of its only parameter. For example, the instruction
  4,50 would output the value at address 50.

Programs that use these instructions will come with documentation that explains
what should be connected to the input and output. The program 3,0,4,0,99 outputs
whatever it gets as input, then halts.

Second, you'll need to add support for parameter modes:

Each parameter of an instruction is handled based on its parameter mode. Right
now, your ship computer already understands parameter mode 0, position mode,
which causes the parameter to be interpreted as a position - if the parameter is
50, its value is the value stored at address 50 in memory. Until now, all
parameters have been in position mode.

Now, your ship computer will also need to handle parameters in mode 1, immediate
mode. In immediate mode, a parameter is interpreted as a value - if the
parameter is 50, its value is simply 50.

Parameter modes are stored in the same value as the instruction's opcode. The
opcode is a two-digit number based only on the ones and tens digit of the value,
that is, the opcode is the rightmost two digits of the first value in an
instruction. Parameter modes are single digits, one per parameter, read
right-to-left from the opcode: the first parameter's mode is in the hundreds
digit, the second parameter's mode is in the thousands digit, the third
parameter's mode is in the ten-thousands digit, and so on. Any missing modes are
0.

For example, consider the program 1002,4,3,4,33.

The first instruction, 1002,4,3,4, is a multiply instruction - the rightmost two
digits of the first value, 02, indicate opcode 2, multiplication. Then, going
right to left, the parameter modes are 0 (hundreds digit), 1 (thousands digit),
and 0 (ten-thousands digit, not present and therefore zero):

ABCDE
 1002

DE - two-digit opcode,      02 == opcode 2
 C - mode of 1st parameter,  0 == position mode
 B - mode of 2nd parameter,  1 == immediate mode
 A - mode of 3rd parameter,  0 == position mode,
                                  omitted due to being a leading zero

This instruction multiplies its first two parameters. The first parameter, 4 in
position mode, works like it did before - its value is the value stored at
address 4 (33). The second parameter, 3 in immediate mode, simply has value 3.
The result of this operation, 33 * 3 = 99, is written according to the third
parameter, 4 in position mode, which also works like it did before - 99 is
written to address 4.

Parameters that an instruction writes to will never be in immediate mode.

Finally, some notes:

- It is important to remember that the instruction pointer should increase by
  the number of values in the instruction after the instruction finishes.
  Because of the new instructions, this amount is no longer always 4.
- Integers can be negative: 1101,100,-1,4,0 is a valid program (find 100 + -1,
  store the result in position 4). The TEST diagnostic program will start by
  requesting from the user the ID of the system to test by running an input
  instruction - provide it 1, the ID for the ship's air conditioner unit.

It will then perform a series of diagnostic tests confirming that various parts
of the Intcode computer, like parameter modes, function correctly. For each
test, it will run an output instruction indicating how far the result of the
test was from the expected value, where 0 means the test was successful.
Non-zero outputs mean that a function is not working correctly; check the
instructions that were run before the output instruction to see which one
failed.

Finally, the program will output a diagnostic code and immediately halt. This
final output isn't an error; an output followed immediately by a halt means the
program finished. If all outputs were zero except the diagnostic code, the
diagnostic program ran successfully.

After providing 1 to the only input instruction and passing all the tests, what
diagnostic code does the program produce?
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


def run_intcode(inp):
    pos = 0
    iteration = 1
    print(f'iteration {iteration}: {inp}')

    # opcode 1 means add; opcode 2 means multiply
    # next three numbers are first input index, second input index, and index to
    # write to
    
    # opcode 3 means take an input and save it to position
    # opcode 4 means output (print) the parameter
    while True:
        print(f'iteration {iteration}')
        opcode = inp[pos]
        param_int = None

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
            input_code = int(input('Enter program input: '))
            inp[inp[pos+1]] = input_code
        elif opcode == 4:
            # output value of the only parameter
            nparams = 1
            params = parse_param_modes(param_int, nparams, pos, inp)
            print(f'OUTPUT: {params[0]}')
        
        pos += nparams + 1
        iteration += 1
    return inp


if __name__ == '__main__':

    with open('05/input', 'r') as f:
        inp = f.readline()

    inp = [int(i) for i in inp.split(',')]
    inp = run_intcode(inp)

    # Answer is 13787043