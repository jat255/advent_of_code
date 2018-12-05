"""
The polymer is formed by smaller units which, when triggered, react with
each other such that two adjacent units of the same type and opposite
polarity are destroyed.Units' types are represented by letters; units'
polarity is represented by capitalization.For instance, r and R are units
with the same type but opposite polarity, whereas r and s are entirely
different types and do not react.

For example:

In aA, a and A react, leaving nothing behind.
In abBA, bB destroys itself, leaving aA. As above, this then destroys itself, leaving nothing.
In abAB, no two adjacent units are of the same type, and so nothing happens.
In aabAAB, even though aa and AA are of the same type, their polarities match, and so nothing happens.

Now, consider a larger example, dabAcCaCBAcCcaDA:

dabAcCaCBAcCcaDA  The first 'cC' is removed.
dabAaCBAcCcaDA    This creates 'Aa', which is removed.
dabCBAcCcaDA      Either 'cC' or 'Cc' are removed (the result is the same).
dabCBAcaDA        No further actions can be taken.
After all possible reactions, the resulting polymer contains 10 units.
"""


def remove_one_match(inp):
    for i, c in enumerate(inp):
        try:
            # if the next letter is the same but opposite case, return
            # string with the match removed
            if c.swapcase() == inp[i + 1]:
                return inp[:i] + inp[i + 2:]
        except IndexError:
            # This means we've reached the end
            return inp


if __name__ == '__main__':
    with open('input', 'r') as f:
        lines = [line.strip('\n') for line in f]

    inp = lines[0]

    # test input:
    # inp = 'dabAcCaCBAcCcaDA'
    print('input is {} characters long'.format(len(inp)))

    done = False
    i = 0
    while not done:
        i += 1
        if i % 100 == 0:
            print(i)
        output = remove_one_match(inp)
        # if the output and input are not the same, then we removed something:
        if not output == inp:
            inp = output
        else:
            print(len(output), output)
            done = True
