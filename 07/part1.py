"""
While snooping around the local network of EBHQ, you compile a list of IP addresses (they're IPv7, of course; IPv6 is much too limited). You'd like to figure out which IPs support TLS (transport-layer snooping).

An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or ABBA. An ABBA is any four-character sequence which consists of a pair of two different characters followed by the reverse of that pair, such as xyyx or abba. However, the IP also must not have an ABBA within any hypernet sequences, which are contained by square brackets.

For example:

- abba[mnop]qrst supports TLS (abba outside square brackets).
- abcd[bddb]xyyx does not support TLS (bddb is within square brackets, even though xyyx is outside square brackets).
- aaaa[qwer]tyui does not support TLS (aaaa is invalid; the interior characters must be different).
- ioxxoj[asdfgh]zxcvbn supports TLS (oxxo is outside square brackets, even though it's within a larger string).

How many IPs in your puzzle input support TLS?
"""

with open('input.txt') as f:
  lines = [l.strip() for l in f.readlines()]

def contains_abba(s):
  for i in range(len(s)-3):
    if s[i] != s[i+1] and s[i+1] == s[i+2] and s[i] == s[i+3]:
      return True
  return False

def supports_tls(s):
  outside_brackets = []
  inside_brackets = []
  am_outside = True
  while len(s) > 0:
    if am_outside:
      # if we have no brackets, we're down to the first part
      # so s looks like "asasdasd"
      if ']' not in s:
        outside_brackets.append(contains_abba(s))
        s = ''
      else:
        # s looks like asdasd[asdadsasd]asdasdas
        r_bracket_idx = s.rindex(']')
        this_section = s[r_bracket_idx + 1:]
        outside_brackets.append(contains_abba(this_section))
        s = s[:r_bracket_idx]
        am_outside = False
    else:
      # s looks like asdasdasd[asdasdasdasd
      l_bracket_idx = s.rindex('[')
      this_section = s[l_bracket_idx + 1:]
      inside_brackets.append(contains_abba(this_section))
      s = s[:l_bracket_idx]
      am_outside = True
  return any(outside_brackets) and not any(inside_brackets)

total = 0
for s in ['abba[mnop]qrst', 'abcd[bddb]xyyx', 
          'aaaa[qwer]tyui', 'ioxxoj[asdfgh]zxcvbn']:
  print(s, supports_tls(s))

for l in lines:
  if supports_tls(l):
    total += 1

print(total)

# 110
