if __name__ == '__main__':
    with open('input', 'r') as f:
        ids = [line.strip('\n')for line in f]

    twos, threes = 0, 0

    for this_id in ids:
        this_id_2 = False
        this_id_3 = False

        # print(this_id)
        for char in this_id:
            if not this_id_2:
                if this_id.count(char) == 2:
                    this_id_2 = True
                    twos += 1
            if not this_id_3:
                if this_id.count(char) == 3:
                    this_id_3 = True
                    threes += 1

    print("Checksum is: {}".format(twos * threes))
