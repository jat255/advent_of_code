"""
--- Day 4: Secure Container ---
You arrive at the Venus fuel depot only to discover it's protected by a
password. The Elves had written the password on a sticky note, but someone threw
it out.

However, they do remember a few key facts about the password:

- It is a six-digit number.
- The value is within the range given in your puzzle input.
- Two adjacent digits are the same (like 22 in 122345).
- Going from left to right, the digits never decrease; they only ever increase
  or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

- 111111 meets these criteria (double 11, never decreases).
- 223450 does not meet these criteria (decreasing pair of digits 50).
- 123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle input meet
these criteria?

Puzzle input is 254032-789860
"""


def has_two_adjacent_digits(inp):
    strinp = str(inp)

    for i in range(len(strinp) - 1):
        if strinp[i] == strinp[i+1]:
            return True
    
    return False


def is_increasing(inp):
    strinp = str(inp)

    for i in range(1, len(strinp)):
        if int(strinp[i]) < int(strinp[i-1]):
            return False
    
    return True


if __name__ == '__main__':

    minval = 254032
    maxval = 789860

    total_matches = 0

    assert has_two_adjacent_digits(122345)
    assert is_increasing(111123)
    assert is_increasing(135679)

    assert (has_two_adjacent_digits(111111) and is_increasing(111111))
    assert not (has_two_adjacent_digits(223450) and is_increasing(223450))
    assert not (has_two_adjacent_digits(123789) and is_increasing(123789))

    for i in range(minval, maxval + 1):
        if has_two_adjacent_digits(i) and is_increasing(i):
            total_matches += 1
    
    print(total_matches)

# Answer is 1033