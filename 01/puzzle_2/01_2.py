from itertools import accumulate

if __name__ == '__main__':
    total = 0

    with open('input', 'r') as f:
        nums = [int(line.strip('\n')) for line in f]

    # print(nums)

    nums = nums * 1000

    seen, result = set(), []
    cum_sum = list(accumulate(nums))

    for idx, item in enumerate(cum_sum):
        if item not in seen:
            seen.add(item)  # First time seeing the element
        else:
            result.append(idx)  # Already seen, add the index to the result

    print(cum_sum[result[0]])
