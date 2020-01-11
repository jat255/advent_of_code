"""
--- Part Two ---
After a while, you realize your shuffling skill won't improve much more with
merely a single deck of cards. You ask every 3D printer on the ship to make you
some more cards while you check on the ship repairs. While reviewing the work
the droids have finished so far, you think you see Halley's Comet fly past!

When you get back, you discover that the 3D printers have combined their power
to create for you a single, giant, brand new, factory order deck of
119315717514047 space cards.

Finally, a deck of cards worthy of shuffling!

You decide to apply your complete shuffle process (your puzzle input) to the
deck 101741582076661 times in a row.

You'll need to be careful, though - one wrong move with this many cards and you
might overflow your entire ship!

After shuffling your new, giant, factory order deck that many times, what number
is on the card that ends up in position 2020?

"""
from tqdm import tqdm
from copy import deepcopy

def process_instructions(fname, size):
    with open(fname, 'r') as f:
        lines = f.readlines()
    
    lines = [l.strip() for l in lines]
    instr = [tuple(l.split(' ')) for l in lines]
    
    lcfs = []
    for i, tup in enumerate(instr):
        if tup[:2] == ('deal', 'into'):
            lcf = (-1, -1)
        elif tup[:2] == ('deal', 'with'):
            n = int(tup[-1])
            lcf = (n, 0)
        elif tup[0] == 'cut':
            n = int(tup[-1])
            lcf = (1, -1*n)
        else:
            raise ValueError(f"did not understand instruction: {tup}")

        lcfs.append(lcf)

    return lcfs

def reduce_instr(lcfs, size, debug=True):
    lcf = lcfs[0]

    for i in range(1, len(lcfs)):
        a, b = lcf
        c, d = lcfs[i]

        lcf = ((a*c) % size, (b*c + d) % size)

    return lcf

def apply_lcf(lcf, stack):
    new_stack = deepcopy(stack)
    for old_idx in range(len(stack)):
        new_idx = (lcf[0] * old_idx + lcf[1]) % size
        new_stack[new_idx] = stack[old_idx]
    return new_stack

def compose_lcf_self(lcf1, size, times=2):
    lcf2 = lcf1
    for i in range(times):
        a, b = lcf1
        c, d = lcf2
        lcf1 = ((a*c) % size, (b*c + d) % size)

    return lcf1

def power_mod(x, n, m):
    """
    Calculate x**n mod m
    """
    if n == 0: return 1
    if n % 2 == 0:
        t = power_mod(x, n/2, m)
        return t * t % m
    else:
        t = power_mod(x, (n-1)/2, m)
        return t * t * x % m

if __name__ == '__main__':

    # With all credit due to https://codeforces.com/blog/entry/72527 and
    # https://codeforces.com/blog/entry/72593 for walking me through this
    # since I had no idea what modular arithmetic was before I started

    # recreating part 1 with new LCF method:
    size = 10007
    lcfs = process_instructions('22/input', size)
    lcf = reduce_instr(lcfs, size)
    shuffled = apply_lcf(lcf, list(range(size)))
    # lcf is (a, b) where f(x) = a*x + b mod m
    assert shuffled.index(2019) == 3143
    
    size = 119315717514047
    m = size
    lcfs = process_instructions('22/input', size)
    lcf = reduce_instr(lcfs, size)
    print(lcf)
    print('')

    a, b = lcf

    k = 101741582076661

    # we have a shuffle, but now need to shuffle 101741582076661 times...
    # this can be reduced to the a*x + b mod m tuple of:
    #   (a**k mod m, b * (1 - a**k) * (1-a)**-1 mod m)

    new_a = power_mod(a, k, m)
    new_b = b * (1 - new_a) * power_mod(1-a, m-2, m)

    # print(new_a, new_b)

    # we now have F^k(x) = a*x + b mod m, but we want F^-k(x), which we can 
    # calculate to be F^-k(x) = (x-B)/A mod m = (x-B)*A**-1 mod m
    # modular multiplicative inverse makes this
    # F^-k(x) = (x-B) A**(m-2) mod m

    def f(x, A, B, m):
        return (x - B)*power_mod(A, m-2, m) % m

    print(f(2020, new_a, new_b, m))

    # Answer is 3920265924568

