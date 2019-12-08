"""
--- Part Two ---
Now you're ready to decode the image. The image is rendered by stacking the
layers and aligning the pixels with the same positions in each layer. The digits
indicate the color of the corresponding pixel: 0 is black, 1 is white, and 2 is
transparent.

The layers are rendered with the first layer in front and the last layer in
back. So, if a given position has a transparent pixel in the first and second
layers, a black pixel in the third layer, and a white pixel in the fourth layer,
the final image would have a black pixel at that position.

For example, given an image 2 pixels wide and 2 pixels tall, the image data
0222112222120000 corresponds to the following image layers:

Layer 1: 02
         22

Layer 2: 11
         22

Layer 3: 22
         12

Layer 4: 00
         00

Then, the full image can be found by determining the top visible pixel in each
position:

- The top-left pixel is black because the top layer is 0.
- The top-right pixel is white because the top layer is 2 (transparent), but the
  second layer is 1.
- The bottom-left pixel is white because the top two layers are 2, but the third
  layer is 1.
- The bottom-right pixel is black because the only visible pixel in that
  position is 0 (from layer 4).

So, the final image looks like this:

01
10

What message is produced after decoding your image?

"""

import numpy as np
import matplotlib.pyplot as plt


def checksum(res, z):
    min_layer = None
    num_lowest_zeros = 1000000 
    for i in range(z):  
        this_layer_zeros = sum(sum(res[i, :, :] == 0))
        # print(f'Layer {i} has {this_layer_zeros} zeros')
        if this_layer_zeros < num_lowest_zeros:
            min_layer = i
            num_lowest_zeros = this_layer_zeros

    # print(f'\nLayer {min_layer}:')
    # print(res[min_layer, :, :])

    num_ones = sum(sum(res[min_layer, :, :] == 1))
    # print(f'Layer {min_layer} has {num_ones} ones')
    num_twos = sum(sum(res[min_layer, :, :] == 2))
    # print(f'Layer {min_layer} has {num_twos} twos')

    return num_ones * num_twos


def proc_image(x, y, inp):
    z = int(len(inp)/(x*y))
    res = np.zeros((z, y, x), dtype=int)
    
    res_flat = res.flatten('C')

    for i in range(len(inp)):
        res_flat[i % len(res_flat)] = inp[i]

    res = res_flat.reshape((z, y, x))

    # print(checksum(res, z)) 

    return res


def get_pixel_val(arr):
    """
    arr : 1d numpy array
      one pixel stack from the image

    0 is black
    1 is white
    2 is transparent
    """
    val = 2
    i = 0
    while val == 2:
        val = arr[i]
        i += 1
    return val


if __name__ == '__main__':

    with open('08/input', 'r') as f:
        inp = f.readline()

    # test_inp = '0222112222120000'

    res = proc_image(25, 6, inp)

    final_res = np.zeros(res[0,:,:].shape, dtype=int)

    for ix in np.ndindex(*res[0,:,:].shape):
        pix_stack = res[:, ix[0], ix[1]]
        val = get_pixel_val(pix_stack)
        final_res[ix[0], ix[1]] = val
        # print(pix_stack, val)


    print(final_res)

    plt.imshow(final_res)
    plt.show()

    # Answer is EJRGP