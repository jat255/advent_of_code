"""
--- Part Two ---
Then, you notice the instructions continue on the back of the Recruiting Document. Easter Bunny HQ is actually at the first location you visit twice.

For example, if your instructions are R8, R4, R4, R8, the first location you visit twice is 4 blocks away, due East.

How many blocks away is the first location you visit twice?
"""
import sys
with open('input.txt') as f:
  lines = [l.strip() for l in f.readlines()][0]

# lines = 'R8, R4, R4, R8'

instructions = lines.split(', ')
print(instructions)
angle = 0
x, y = (0, 0)
positions = []
positions.append((0,0))
for i in instructions:
  print(positions)
  if i[0] == 'R':
    angle += 90
  else:
    angle -= 90
  angle %= 360
  dist = int(i[1:])
  if angle == 0:
    # north
    for d in range(1, dist+1):
      new_pos = (x, y+d)
      if new_pos in positions:
        print(f'been here: {new_pos}')
        print(abs(new_pos[0]) + abs(new_pos[1]))
        sys.exit()
      positions.append(new_pos)
    y += dist
  elif angle == 90:
    # east
    for d in range(1, dist+1):
      new_pos = (x+d, y)
      if new_pos in positions:
        print(f'been here: {new_pos}')
        print(abs(new_pos[0]) + abs(new_pos[1]))
        sys.exit()
      positions.append(new_pos)
    x += dist
  elif angle == 180:
    # south
    for d in range(1, dist+1):
      new_pos = (x, y-d)
      if new_pos in positions:
        print(f'been here: {new_pos}')
        print(abs(new_pos[0]) + abs(new_pos[1]))
        sys.exit()
      positions.append(new_pos)
    y -= dist
  elif angle == 270:
    # west
    for d in range(1, dist+1):
      new_pos = (x-d, y)
      if new_pos in positions:
        print(f'been here: {new_pos}')
        print(abs(new_pos[0]) + abs(new_pos[1]))
        sys.exit()
      positions.append(new_pos)
    x -= dist

# 116
