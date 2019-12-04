"""
--- Part Two ---
An Elf just remembered one more important detail: the two adjacent matching
digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the
following are now true:

- 112233 meets these criteria because the digits never decrease and all repeated
  digits are exactly two digits long.
- 123444 no longer meets the criteria (the repeated 44 is part of a larger group
  of 444).
- 111122 meets the criteria (even though 1 is repeated more than twice, it still
  contains a double 22).

How many different passwords within the range given in your puzzle input meet
all of the criteria?

Puzzle input is 254032-789860
"""


def has_two_adjacent_digits(inp):
    strinp = str(inp)

    for i in range(len(strinp) - 1):
        c = strinp[i]
        cnext = strinp[i+1]
        if strinp[i] == strinp[i+1]:
            # we're in a double... are there more?
            try:
                if strinp[i] == strinp[i-1]:
                    # there's a previous match, so continue rather than return true
                    continue
            except IndexError:
                # there was no previous number, so just keep on testing
                pass
            try:
                if strinp[i] == strinp[i+2]:
                    # there's another match after this one, so continue rather than return true
                    continue
            except IndexError:
                pass

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

    assert (has_two_adjacent_digits(112233) and is_increasing(112233))
    assert not (has_two_adjacent_digits(123444) and is_increasing(123444))
    assert (has_two_adjacent_digits(111122) and is_increasing(111122))

    for i in range(minval, maxval + 1):
        if has_two_adjacent_digits(i) and is_increasing(i):
            total_matches += 1
    
    print(total_matches)

# Answer is 670