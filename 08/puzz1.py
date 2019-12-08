"""
--- Day 8: Space Image Format ---
The Elves' spirits are lifted when they realize you have an opportunity to
reboot one of their Mars rovers, and so they are curious if you would spend a
brief sojourn on Mars. You land your ship near the rover.

When you reach the rover, you discover that it's already in the process of
rebooting! It's just waiting for someone to enter a BIOS password. The Elf
responsible for the rover takes a picture of the password (your puzzle input)
and sends it to you via the Digital Sending Network.

Unfortunately, images sent via the Digital Sending Network aren't encoded with
any normal encoding; instead, they're encoded in a special Space Image Format.
None of the Elves seem to remember why this is the case. They send you the
instructions to decode it.

Images are sent as a series of digits that each represent the color of a single
pixel. The digits fill each row of the image left-to-right, then move downward
to the next row, filling rows top-to-bottom until every pixel of the image is
filled.

Each image actually consists of a series of identically-sized layers that are
filled in this way. So, the first digit corresponds to the top-left pixel of the
first layer, the second digit corresponds to the pixel to the right of that on
the same layer, and so on until the last digit, which corresponds to the
bottom-right pixel of the last layer.

For example, given an image 3 pixels wide and 2 pixels tall, the image data
123456789012 corresponds to the following image layers:

Layer 1: 123
         456

Layer 2: 789
         012

The image you received is 25 pixels wide and 6 pixels tall.

To make sure the image wasn't corrupted during transmission, the Elves would
like you to find the layer that contains the fewest 0 digits. On that layer,
what is the number of 1 digits multiplied by the number of 2 digits?
"""

import numpy as np
import matplotlib.pyplot as plt


def proc_image(x, y, inp):
    z = int(len(inp)/(x*y))
    res = np.zeros((z, y, x))
    
    res_flat = res.flatten('C')

    for i in range(len(inp)):
        res_flat[i % len(res_flat)] = inp[i]

    res = res_flat.reshape((z, y, x))

    min_layer = None
    num_lowest_zeros = 1000000 
    for i in range(z):  
        this_layer_zeros = sum(sum(res[i, :, :] == 0))
        print(f'Layer {i} has {this_layer_zeros} zeros')
        if this_layer_zeros < num_lowest_zeros:
            min_layer = i
            num_lowest_zeros = this_layer_zeros

    print(f'\nLayer {min_layer}:')
    print(res[min_layer, :, :])

    num_ones = sum(sum(res[min_layer, :, :] == 1))
    print(f'Layer {min_layer} has {num_ones} ones')
    num_twos = sum(sum(res[min_layer, :, :] == 2))
    print(f'Layer {min_layer} has {num_twos} twos')

    return num_ones * num_twos



if __name__ == '__main__':

    with open('08/input', 'r') as f:
        inp = f.readline()

    with open('08/test_input', 'r') as f:
        test_inp = f.readline()

    print(proc_image(25, 6, inp))

    # Answer is 1206