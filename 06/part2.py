"""
--- Part Two ---
Of course, that would be the message - if you hadn't agreed to use a modified repetition code instead.

In this modified code, the sender instead transmits what looks like random data, but for each character, the character they actually want to send is slightly less likely than the others. Even after signal-jamming noise, you can look at the letter distributions in each column and choose the least common letter to reconstruct the original message.

In the above example, the least common character in the first column is a; in the second, d, and so on. Repeating this process for the remaining characters produces the original message, advent.

Given the recording in your puzzle input and this new decoding methodology, what is the original message that Santa is trying to send?
"""

with open('input.txt') as f:
  lines = [l.strip() for l in f.readlines()]

import numpy as np
from scipy.stats import mode 

data = np.array([list(l) for l in lines], dtype=str)
output = ''
int_data = np.vectorize(ord)(data)

for i in range(data.shape[1]):
  counts = np.bincount(int_data[:, i])
  min_count = np.min([i for i in counts if i != 0])
  min_ord = np.argwhere(counts == min_count)
  output += chr(min_ord[0][0])

print(output)

# owlaxqvq
