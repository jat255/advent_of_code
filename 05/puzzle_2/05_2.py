"""
Time to improve the polymer.

One of the unit types is causing problems; it's preventing the polymer from
collapsing as much as it should. Your goal is to figure out which unit type
is causing the most problems, remove all instances of it (regardless of
polarity), fully react the remaining polymer, and measure its length.

For example, again using the polymer dabAcCaCBAcCcaDA from above:

Removing all A/a units produces dbcCCBcCcD. Fully reacting this polymer
produces dbCBcD, which has length 6.

Removing all B/b units produces daAcCaCAcCcaDA. Fully reacting this polymer
produces daCAcaDA, which has length 8.

Removing all C/c units produces dabAaBAaDA. Fully reacting this polymer
produces daDA, which has length 4.

Removing all D/d units produces abAcCaCBAcCcaA. Fully reacting this polymer
produces abCBAc, which has length 6.

In this example, removing all C/c units was best, producing the answer 4.

What is the length of the shortest polymer you can produce by removing all units of exactly one type and fully reacting the result?
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


def remove_all_matches(inp):
    i = 0
    while True:
        i += 1
        if i % 100 == 0:
            pass
            # print(i)
        output = remove_one_match(inp)
        # if the output and input are not the same, then we removed something:
        if not output == inp:
            inp = output
        else:
            # print(len(output), output)
            return output


if __name__ == '__main__':
    with open('input', 'r') as f:
        lines = [line.strip('\n') for line in f]

    inp = lines[0]

    # test input:
    # inp = 'dabAcCaCBAcCcaDA'
    unique_chars = sorted(list(set(inp.lower())))
    print('input is {} characters long'.format(len(inp)))
    print('{} unique characters'.format(len(unique_chars)))
    print()

    length_results = {}
    for char in unique_chars:
        print('Removed ' + char)
        reduced_inp = inp.replace(char, '').replace(char.upper(), '')
        result = remove_all_matches(reduced_inp)
        print(char, len(result), result)
        length_results[char] = len(result)
        print()

    min_char = min(length_results, key=length_results.get)
    min_length = length_results[min_char]
    print('smallest resulting polymer of length {} is when removing '
          '{}'.format(min_length, min_char))


