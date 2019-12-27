"""
--- Part Two ---
Now that your FFT is working, you can decode the real signal.

The real signal is your puzzle input repeated 10000 times. Treat this new signal
as a single input list. Patterns are still calculated as before, and 100 phases
of FFT are still applied.

The first seven digits of your initial input signal also represent the message
offset. The message offset is the location of the eight-digit message in the
final output list. Specifically, the message offset indicates the number of
digits to skip before reading the eight-digit message. For example, if the first
seven digits of your initial input signal were 1234567, the eight-digit message
would be the eight digits after skipping 1,234,567 digits of the final output
list. Or, if the message offset were 7 and your final output list were
98765432109876543210, the eight-digit message would be 21098765. (Of course,
your real message offset will be a seven-digit number, not a one-digit number
like 7.)

Here is the eight-digit message in the final output list after 100 phases. The
message offset given in each input has been highlighted. (Note that the inputs
given below are repeated 10000 times to find the actual starting input lists.)

- 03036732577212944063491565474664 becomes 84462026.
- 02935109699940807407585447034323 becomes 78725270.
- 03081770884921959731165446850517 becomes 53553731.

After repeating your input signal 10000 times and running 100 phases of FFT,
what is the eight-digit message embedded in the final output list?

"""

from itertools import cycle
from itertools import repeat
from itertools import chain
from tqdm import tqdm

base_pattern = ['0', '1', '0', '-1']

def fft(fname, num_phases):
    with open(fname, 'r') as f:
        inp = f.readline().strip() * 10000
    message_offset = int(inp[:7])
    # first message_offset digits of pattern will be zeros, rest will be ones
    # so we just have to sum digits, rather than doing all the i * p stuff
    
    # last digit of output is just last digit of input
    # N-1 digit of output is sum of last two input digits; mod 10
    # N-2 digit of output is sum of last three input digits; mod 10
    inp = inp[message_offset:]
    for itr in tqdm(range(num_phases)):
        output = [' '] * len(inp)
        
        cumsum = 0
        for idx, i in enumerate(inp[::-1]):
            cumsum += int(i)
            this_out = str(cumsum % 10)
            output[-1*(idx+1)] = this_out
            pass

        inp =  ''.join(output)

    return ''.join(output[:8])

if __name__ == '__main__':

    assert fft('16/test_input5', 100) == '84462026'
    assert fft('16/test_input6', 100) == '78725270'
    assert fft('16/test_input7', 100) == '53553731'

    print(fft('16/input', 100))

    # Answer is 19422575

    