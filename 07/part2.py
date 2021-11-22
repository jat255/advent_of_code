"""
--- Part Two ---
You would also like to know which IPs support SSL (super-secret listening).

An IP supports SSL if it has an Area-Broadcast Accessor, or ABA, anywhere in the supernet sequences (outside any square bracketed sections), and a corresponding Byte Allocation Block, or BAB, anywhere in the hypernet sequences. An ABA is any three-character sequence which consists of the same character twice with a different character between them, such as xyx or aba. A corresponding BAB is the same characters but in reversed positions: yxy and bab, respectively.

For example:

- aba[bab]xyz supports SSL (aba outside square brackets with corresponding bab within square brackets).
- xyx[xyx]xyx does not support SSL (xyx, but no corresponding yxy).
- aaa[kek]eke supports SSL (eke in supernet with corresponding kek in hypernet; the aaa sequence is not related, because the interior character must be different).
- zazbz[bzb]cdb supports SSL (zaz has no corresponding aza, but zbz has a corresponding bzb, even though zaz and zbz overlap).

How many IPs in your puzzle input support SSL?
"""
import re

## approach is to look for aba sequences not inside []
## and then look for matching bab sequences inside []

with open('input.txt') as f:
  lines = [l.strip() for l in f.readlines()]

def aba_finder(s):
  aba_strings = []
  for i in range(len(s) - 2):
    if s[i] == s[i+2] and s[i] != s[i+1]:
      aba_strings.append(s[i:i+3])
  return aba_strings

def supports_ssl(ip: str):
  aba_strings = []
  am_outside = True
  s = ip
  while len(s) > 0:
    if am_outside:
      # if we have no brackets, we're down to the first part
      # so s looks like "asasdasd"
      if ']' not in s:
        aba_strings.extend(aba_finder(s))
        s = ''
      else:
        # s looks like asdasd[asdadsasd]asdasdas
        r_bracket_idx = s.rindex(']')
        this_section = s[r_bracket_idx + 1:]
        aba_strings.extend(aba_finder(this_section))
        s = s[:r_bracket_idx]
        am_outside = False
    else:
      # s looks like asdasdasd[asdasdasdasd
      l_bracket_idx = s.rindex('[')
      this_section = s[l_bracket_idx + 1:]
      s = s[:l_bracket_idx]
      am_outside = True
  
  for s in aba_strings:
    bab = s[1] + s[0] + s[1]
    # find "[" character, followed by any number of characters that
    # are not "[", then the bab string, then any number of characters
    # that are not "[", then finally "]"
    pattern = f'\[[^\[]*{bab}[^\[]*\]'
    if len(re.findall(pattern, ip)) > 0:
      return True
  
  return False

total = 0
# for s in ['aba[bab]xyz', 'xyx[xyx]xyx', 
#           'aaa[kek]eke', 'zazbz[bzb]cdb']:
#   print(s, supports_ssl(s))

for l in lines:
  if supports_ssl(l):
    total += 1

print(total)

# 242
