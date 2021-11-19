"""
--- Part Two ---
Now that you've helpfully marked up their design documents, it occurs to you that triangles are specified in groups of three vertically. Each set of three numbers in a column specifies a triangle. Rows are unrelated.

For example, given the following specification, numbers with the same hundreds digit would be part of the same triangle:

101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603

In your puzzle input, and instead reading by columns, how many of the listed triangles are possible?
"""

with open('input.txt') as f:
  lines = [l.strip() for l in f.readlines()]

import numpy as np
data = [[int(i) for i in l] for l in [l.split() for l in lines]]
data = np.array(data)
possible = 0
for j in range(data.shape[1]):
  print(f'column {j}')
  for i in range(0, data.shape[0]-2, 3):
    t = [data[i, j], data[i+1,j], data[i+2,j]]
    # print(t)
    if t[0] + t[1] > t[2] and t[1] + t[2] > t[0] and t[0] + t[2] > t[1]:
      possible += 1 

print(possible)

# 1544