import numpy as np
import re


if __name__ == '__main__':
    with open('input', 'r') as f:
        lines = [line.strip('\n') for line in f]

    # with open('test_input', 'r') as f:
    #     lines = [line.strip('\n') for line in f]

    canvas_size = 1000
    canvas = np.zeros((canvas_size, canvas_size), dtype=int)

    regex = r'#([0-9]*) @ ([0-9]*),([0-9]*): ([0-9]*)x([0-9]*)'
    for line in lines:
        m = re.match(regex, line)
        this_id, x, y, w, h = [int(m.group(i))
                               for i in range(1, m.lastindex + 1)]

        canvas[x:x+w, y:y+h] += 1

    print((canvas > 1).sum())

