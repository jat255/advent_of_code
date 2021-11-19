"""
--- Part Two ---
With all the decoy data out of the way, it's time to decrypt this list and get moving.

The room names are encrypted by a state-of-the-art shift cipher, which is nearly unbreakable without the right software. However, the information kiosk designers at Easter Bunny HQ were not expecting to deal with a master cryptographer like yourself.

To decrypt a room name, rotate each letter forward through the alphabet a number of times equal to the room's sector ID. A becomes B, B becomes C, Z becomes A, and so on. Dashes become spaces.

For example, the real name for qzmt-zixmtkozy-ivhz-343 is very encrypted name.

What is the sector ID of the room where North Pole objects are stored?
"""

with open('input.txt') as f:
  lines = [l.strip() for l in f.readlines()]

total = 0

def rotate_letter(letter, degree):
  if letter == '-':
    return ' '

  new_ord = ord(letter) + (degree % 26)
  if new_ord > ord('z'):
    new_ord -= 26
  return chr(new_ord)

assert rotate_letter('q', 343) == 'v'
assert rotate_letter('z', 343) == 'e'
assert rotate_letter('m', 343) == 'r'
assert rotate_letter('t', 343) == 'y'

for l in lines:
  checksum = l[-7:].strip('[]')
  sector_id = int(l[:-7].split('-')[-1])
  letters = ''.join(l[:-7].split('-')[:-1])
  counts = []
  for lett in set(letters):
    counts.append((lett, letters.count(lett)))
  srt = sorted(counts, key=lambda x:(-x[1], x[0]), reverse=False)
  this_checksum = ''.join([x[0] for x in srt[:5]])
  if this_checksum == checksum:
    new_string = ''.join([rotate_letter(i, sector_id) for i in '-'.join(l[:-7].split('-')[:-1])])
    if 'north' in new_string:
      print(sector_id, new_string) 

# 984 northpole object storage
