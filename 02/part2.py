"""
--- Part Two ---
You finally arrive at the bathroom (it's a several minute walk from the lobby so visitors can behold the many fancy conference rooms and water coolers on this floor) and go to punch in the code. Much to your bladder's dismay, the keypad is not at all like you imagined it. Instead, you are confronted with the result of hundreds of man-hours of bathroom-keypad-design meetings:

X X 1 X X   
X 2 3 4 X 
5 6 7 8 9
X A B C X 
X X D X X   

You still start at "5" and stop when you're at an edge, but given the same instructions as above, the outcome is very different:

You start at "5" and don't move at all (up and left are both edges), ending at 5.
Continuing from "5", you move right twice and down three times (through "6", "7", "B", "D", "D"), ending at D.
Then, from "D", you move five more times (through "D", "B", "C", "C", "B"), ending at B.
Finally, after five more moves, you end at 3.
So, given the actual keypad layout, the code would be 5DB3.

Using the same instructions in your puzzle input, what is the correct bathroom code?
"""

with open('input.txt') as f:
  lines = [l.strip() for l in f.readlines()]


keypad = {
  (0, 0): 0, (1, 0):  0 , (2, 0):  1 , (3, 0):  0 , (4, 0): 0,
  (0, 1): 0, (1, 1):  2 , (2, 1):  3 , (3, 1):  4 , (4, 1): 0,
  (0, 2): 5, (1, 2):  6 , (2, 2):  7 , (3, 2):  8 , (4, 2): 9,
  (0, 3): 0, (1, 3): 'A', (2, 3): 'B', (3, 3): 'C', (4, 3): 0,
  (0, 4): 0, (1, 4):  0 , (2, 4): 'D', (3, 4):  0 , (4, 4): 0,
}

code = ''
x, y = (0, 2)
for l in lines:
  # print(f"processing {l}")
  for char in l:
    if char == 'L':
      new_pos = (x-1, y)
      if x-1 < 0 or keypad[new_pos] == 0:
        pass
      else:
        x, y = new_pos
    elif char == 'R':
      new_pos = (x+1, y)
      if x+1 > 4 or keypad[new_pos] == 0:
        pass
      else:
        x, y = new_pos
    elif char == 'U':
      new_pos = (x, y-1)
      if y-1 < 0 or keypad[new_pos] == 0:
        pass
      else:
        x, y = new_pos
    elif char == 'D':
      new_pos = (x, y+1)
      if y+1 > 4 or keypad[new_pos] == 0:
        pass
      else:
        x, y = new_pos
    # print(f"x, y is {x}, {y} = {keypad[(x, y)]}")

  code += str(keypad[(x, y)])

print(code)
# DD483