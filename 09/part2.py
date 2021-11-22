"""
--- Part Two ---
Apparently, the file actually uses version two of the format.

In version two, the only difference is that markers within decompressed data are decompressed. This, the documentation explains, provides much more substantial compression capabilities, allowing many-gigabyte files to be stored in only a few kilobytes.

For example:

- (3x3)XYZ still becomes XYZXYZXYZ  (9), as the decompressed section contains no markers.
- X(8x2)(3x3)ABCY becomes XABCABCABCABCABCABCY  (20) , because the decompressed data from the (8x2) marker is then further decompressed, thus triggering the (3x3) marker twice for a total of six ABC sequences.
- (27x12)(20x12)(13x14)(7x10)(1x12)A decompresses into a string of A repeated 241920 times.
- (25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN becomes 445 characters long.

(25x3)(3x3)ABC(2x3)XY(5x2)PQRST  --  X -- (18x9)(3x2)TWO(5x7)SEVEN
   3 * (9     +  6    +   10)     +  1   +  9  ( 6   +    35 )
              75               +     1   +     369  
                        =  445
ABCABCABCXYXYXYPQRSTPQRSTABCABCABCXYXYXYPQRSTPQRSTABCABCABCXYXYXYPQRSTPQRSTXTWOTWOSEVENSEVENSEVENSEVENSEVENSEVENSEVENTWOTWOSEVENSEVENSEVENSEVENSEVENSEVENSEVENTWOTWOSEVENSEVENSEVENSEVENSEVENSEVENSEVENTWOTWOSEVENSEVENSEVENSEVENSEVENSEVENSEVENTWOTWOSEVENSEVENSEVENSEVENSEVENSEVENSEVENTWOTWOSEVENSEVENSEVENSEVENSEVENSEVENSEVENTWOTWOSEVENSEVENSEVENSEVENSEVENSEVENSEVENTWOTWOSEVENSEVENSEVENSEVENSEVENSEVENSEVENTWOTWOSEVENSEVENSEVENSEVENSEVENSEVENSEVEN

So we have to identify the blocks to add together, then multiply by the right
number of repeats

Unfortunately, the computer you brought probably doesn't have enough memory to actually decompress the file; you'll have to come up with another way to get its decompressed length.

What is the decompressed length of the file using this improved format?
"""

# %%
with open('input.txt') as f:
  lines = [l.strip() for l in f.readlines()]

import re

def decompress(s):
  outp = ''
  i = 0
  while i < len(s):
    if s[i] == '(':
      # about to read a marker
      x_idx = s[i:].index('x') + i
      r_paren_idx = s[i:].index(')') + i
      n_char = int(s[i+1:x_idx])
      char_limit_idx = r_paren_idx + 1 + n_char
      n_rep = int(s[x_idx+1:r_paren_idx])
      outp += s[r_paren_idx+1:char_limit_idx] * n_rep
      i = char_limit_idx
    else:
      outp += s[i]
      i += 1
  return outp

def v2_decompress(s):
  while '(' in s or ')' in s:
    print(f"{s.count('(')} patterns remaining")
    s = decompress(s)
  return s

def get_nchar_nreps(s):
  nchar, nreps = re.match('\((\d*)x(\d*)\)', s).groups()
  l = len(nchar + nreps) + 3
  return (int(nchar), int(nreps), s[l:l + int(nchar)])

def calc_length(s):
  # if s.count('(') == 1:
  #   nchar, nreps = get_nchar_nreps(s)
  #   return nchar * nreps
  length = 0
  i = 0
  while i < len(s):
    if s[i] != '(':
      length += 1
      i += 1
    else:
      r_index = s[i:].index(')')
      this_marker = s[i:r_index + 1]
      nchar, nreps = get_nchar_nreps(this_marker)
      this_string = s[r_index + 1:r_index + 1 + nchar]
      if '(' in this_string:
        return calc_length(this_string)
      else:
        length += nchar * nreps
        i = r_index + nchar + 1
  return length

# (25x3)(3x3)ABC(2x3)XY(5x2)PQRST  --  X -- (18x9)(3x2)TWO(5x7)SEVEN
  #  3 * (9     +  6    +   10)     +  1   +  9  ( 6   +    35 )
              # 75               +     1   +     369  
                        # =  445

def l_calc(s):
  if not '(' in s:
    return len(s)
  c, r, new_s = get_nchar_nreps(s)
  if not '(' in new_s:
    return len(new_s)
  if '(' in new_s:
    return r * l_calc(new_s)
  

# assert v2_decompress('ADVENT') == 'ADVENT'
# assert v2_decompress('A(1x5)BC') == 'ABBBBBC'
# assert v2_decompress('(3x3)XYZ') == 'XYZXYZXYZ'
# assert decompress('A(2x2)BCD(2x2)EFG') == 'ABCBCDEFEFG'
# assert decompress('(6x1)(1x3)A') == '(1x3)A'
# assert v2_decompress('X(8x2)(3x3)ABCY') == 'XABCABCABCABCABCABCY'
# assert len(v2_decompress('(27x12)(20x12)(13x14)(7x10)(1x12)A')) == 241920
# print(v2_decompress('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN'))
# print(calc_length('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN'))
# print(calc_length('(3x3)XYZZ'))

print(get_nchar_nreps('(25x3)(3x3)ABC(2x3)XY(5x2)PQRST'))
print(get_nchar_nreps('(3x3)ABC(2x3)XY(5x2)PQRST'))
print(l_calc('(25x3)(3x3)ABC(2x3)XY(5x2)PQRST'))

inp = lines[0]
# print(len(v2_decompress(inp)))

# 110346
