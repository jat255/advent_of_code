import numpy as np
import re


if __name__ == '__main__':
    with open('input', 'r') as f:
        lines = [line.strip('\n') for line in f]

    # with open('test_input', 'r') as f:
    #     lines = [line.strip('\n') for line in f]

    canvas_size = 1000
    canvas = np.zeros((canvas_size, canvas_size), dtype=str)
    canvas[:, :] = '    '

    regex = r'#([0-9]*) @ ([0-9]*),([0-9]*): ([0-9]*)x([0-9]*)'
    for line in lines:
        m = re.match(regex, line)
        this_id, x, y, w, h = [int(m.group(i))
                               for i in range(1, m.lastindex + 1)]

        for xi in range(x, x+w):
            for yi in range(y, y+h):
                if canvas[xi, yi] == ' ':
                    canvas[xi, yi] = this_id
                else:
                    canvas[xi, yi] = 'X'

    # print(canvas)
    # print((canvas == 'X').sum())

    for line in lines:
        m = re.match(regex, line)
        this_id, x, y, w, h = [int(m.group(i))
                               for i in range(1, m.lastindex + 1)]
        # print(canvas[x:x+w, y:y+h])
        test_array = np.zeros((w, h), dtype=str)
        test_array[:] = this_id
        # print(test_array)
        if np.array_equal(canvas[x:x + w, y:y + h], test_array):
            print('Claim {} is intact'.format(this_id))
        # print()

