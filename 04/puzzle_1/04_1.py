import datetime as dt

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
    sleep_times = {}
    for i, d in enumerate(data):
        guard_num = d[1]
        # guard number is given, so just store it and move on
        if guard_num is not None:
            current_num = guard_num
            continue
        # elsewise, we're at a sleep or wake event
        elif d[2] == 'asleep':
            sleep_time = data[i+1][0] - d[0]
            if current_num not in sleep_times:
                sleep_times[current_num] = sleep_time
            else:
                sleep_times[current_num] += sleep_time

    print(len(sleep_times))
    ids = []
    for d in data:
        if d[1] is not None:
            ids.append(d[1])

    # print(sleep_times)
    max_guard = max(sleep_times, key=sleep_times.get)
    print('Guard {} sleeps the most at {} total time'.format(
        max_guard, sleep_times[max_guard]))

    minutes_asleep = [0]*60
    for i, d in enumerate(data):
        guard_num = d[1]
        # guard number is given, so just store it and move on
        if guard_num is not None:
            current_num = guard_num
            continue

        if current_num == max_guard:
            if d[2] == 'asleep':
                for m in range(d[0].minute, data[i+1][0].minute):
                    minutes_asleep[m] += 1
                # print('{} to {}'.format(d[0].minute, data[i+1][0].minute))

    max_minute = minutes_asleep.index(max(minutes_asleep))
    print('Guard {} sleeps the most at minute {}'
          ''.format(max_guard, max_minute))

    print('{} x {} = {}'.format(max_guard, max_minute, int(max_guard)*int(
        max_minute)))

