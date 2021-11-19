"""
--- Part Two ---
As the door slides open, you are presented with a second door that uses a slightly more inspired security mechanism. Clearly unimpressed by the last version (in what movie is the password decrypted in order?!), the Easter Bunny engineers have worked out a better solution.

Instead of simply filling in the password from left to right, the hash now also indicates the position within the password to fill. You still look for hashes that begin with five zeroes; however, now, the sixth character represents the position (0-7), and the seventh character is the character to put in that position.

A hash result of 000001f means that f is the second character in the password. Use only the first result for each position, and ignore invalid positions.

For example, if the Door ID is abc:

The first interesting hash is from abc3231929, which produces 0000015...; so, 5 goes in position 1: _5______.
In the previous method, 5017308 produced an interesting hash; however, it is ignored, because it specifies an invalid position (8).
The second interesting hash is at index 5357525, which produces 000004e...; so, e goes in position 4: _5__e___.
You almost choke on your popcorn as the final character falls into place, producing the password 05ace8e3.

Given the actual Door ID and this new method, what is the password? Be extra proud of your solution if it uses a cinematic "decrypting" animation.
"""

# with open('input.txt') as f:
#   lines = [l.strip() for l in f.readlines()]
inp = 'cxdnnyjw'

import hashlib

test_inp = 'abc'

i = 0
output = ['-'] * 8
while output.count('-') > 0:
  hex = hashlib.md5(f"{inp}{i}".encode()).hexdigest()
  if hex[:5] == '00000':
    pos = hex[5]
    next_char = hex[6]
    if pos in '01234567' and output[int(pos)] == '-':
      output[int(pos)] = next_char
      print(f'Found character {next_char} at position {pos}')
  i += 1

print(''.join(output))

# 999828ec
