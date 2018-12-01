total = 0

with open('input', 'r') as f:
    for line in f:
        line = line.strip('\n')
        if line[0] == '+':
            total += int(line[1:])
        else:
            total -= int(line[1:])

print(total)