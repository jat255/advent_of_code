"""
--- Day 4: Security Through Obscurity ---
Finally, you come across an information kiosk with a list of rooms. Of course, the list is encrypted and full of decoy data, but the instructions to decode the list are barely hidden nearby. Better remove the decoy data first.

Each room consists of an encrypted name (lowercase letters separated by dashes) followed by a dash, a sector ID, and a checksum in square brackets.

A room is real (not a decoy) if the checksum is the five most common letters in the encrypted name, in order, with ties broken by alphabetization. For example:

- aaaaa-bbb-z-y-x-123[abxyz] is a real room because the most common letters are a (5), b (3), and then a tie between x, y, and z, which are listed alphabetically.
- a-b-c-d-e-f-g-h-987[abcde] is a real room because although the letters are all tied (1 of each), the first five are listed alphabetically.
- not-a-real-room-404[oarel] is a real room.
- totally-real-room-200[decoy] is not.

Of the real rooms from the list above, the sum of their sector IDs is 1514.

What is the sum of the sector IDs of the real rooms?
"""

with open('input.txt') as f:
  lines = [l.strip() for l in f.readlines()]

total = 0

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
    total += sector_id

print(total)

# 185371
