import datetime as dt
import itertools

if __name__ == '__main__':
    with open('input', 'r') as f:
        lines = [line.strip('\n') for line in f]

    data = [None] * len(lines)

    for i, line in enumerate(lines):
        ts = dt.datetime.strptime(line[1:17],
                                  '%Y-%m-%d %H:%M')
        remainder = line[19:]
        action = None
        if "begins" in remainder:
            action = 'start'
        elif "wakes up" in remainder:
            action = 'wake'
        elif "falls" in remainder:
            action = 'asleep'

        guard_num = None
        if action == 'start':
            guard_num = remainder.split(' ')[1][1:]

        res = [ts, guard_num, action]
        data[i] = res

    data = sorted(data, key=lambda x: x[0])
    current_num = 0
    this_dt = dt.datetime.now()
    minutes_asleep = [0] * 60
    strings = []

    for i, d in enumerate(data):
        guard_num = d[1]
        # guard number is given, so just store it and move on
        if guard_num is not None:
            # print last guards output
            to_print = [this_dt.strftime('%m-%d'), '{:04g}'.format(
                int(current_num)), None]
            str_to_print = ''
            for m in minutes_asleep:
                if m == 0:
                    str_to_print += '.'
                else:
                    str_to_print += '#'
            to_print[2] = str_to_print
            strings.append(to_print)

            current_num = guard_num
            this_dt = d[0]
            minutes_asleep = [0] * 60
            continue

        if d[2] == 'asleep':
            for m in range(d[0].minute, data[i + 1][0].minute):
                minutes_asleep[m] += 1

    del strings[0]
    strings = [x[1:] for x in strings]

    data = sorted(strings, key=lambda x: (x[0]))
    records = {}
    for p in itertools.groupby(data, key=lambda x: x[0]):
        records[p[0]] = [x[1] for x in list(p[1])]

    final_rec = {}
    prev_max = 0
    prev_min_max = 0
    max_id = 0
    for k, v in records.items():
        mins = [0] * 60
        # print(k)
        for day in v:
            for i, minute in enumerate(day):
                if minute == '#':
                    mins[i] += 1
        final_rec[k] = mins
        print(''.join(['{:2g} '.format(m) for m in range(60)]))
        print(''.join(['{:2g} '.format(m) for m in mins]))
        print()
        for m in mins:
            if m > prev_max:
                prev_max = m
                max_id = k
                prev_min_max = mins.index(m)
                print('Current ID is {} and most asleep minute '
                      'is {}'.format(k, prev_min_max))

    print('Final answer should be {} x {} = {}'.format(max_id, prev_min_max,
                                                       int(max_id) * int(
                                                           prev_min_max)))
