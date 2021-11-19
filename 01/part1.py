"""
--- Day 1: No Time for a Taxicab ---
Santa's sleigh uses a very high-precision clock to guide its movements, and the clock's oscillator is regulated by stars. Unfortunately, the stars have been stolen... by the Easter Bunny. To save Christmas, Santa needs you to retrieve all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You're airdropped near Easter Bunny Headquarters in a city somewhere. "Near", unfortunately, is as close as you can get - the instructions on the Easter Bunny Recruiting Document the Elves intercepted start here, and nobody had time to work them out further.

The Document indicates that you should start at the given coordinates (where you just landed) and face North. Then, follow the provided sequence: either turn left (L) or right (R) 90 degrees, then walk forward the given number of blocks, ending at a new intersection.

There's no time to follow such ridiculous instructions on foot, though, so you take a moment and work out the destination. Given that you can only walk on the street grid of the city, how far is the shortest path to the destination?

For example:

Following R2, L3 leaves you 2 blocks East and 3 blocks North, or 5 blocks away.
R2, R2, R2 leaves you 2 blocks due South of your starting position, which is 2 blocks away.
R5, L5, R5, R3 leaves you 12 blocks away.
How many blocks away is Easter Bunny HQ?
"""

with open('input.txt') as f:
  lines = [l.strip() for l in f.readlines()][0]

# lines = 'R5, L5, R5, R3'

instructions = lines.split(', ')

angle = 0
x, y = (0, 0)
for i in instructions:
  if i[0] == 'R':
    angle += 90
  else:
    angle -= 90
  angle %= 360
  dist = int(i[1:])
  if angle == 0:
    # north
    y += dist
  elif angle == 90:
    # east
    x += dist
  elif angle == 180:
    # south
    y -= dist
  elif angle == 270:
    x -= dist

print(f"({x}, {y})")
print(abs(x) + abs(y))

# 241