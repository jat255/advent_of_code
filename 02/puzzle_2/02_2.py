def get_two_ids():
    with open('input', 'r') as f:
        ids = [line.strip('\n') for line in f]

    # with open('test_input', 'r') as f:
    #     ids = [line.strip('\n') for line in f]

    num_chars = len(ids[0])

    for this_id in ids:
        for that_id in ids:
            matches = 0
            for a, b in zip(this_id, that_id):
                if a == b:
                    matches += 1
            if matches == num_chars - 1:
                print("this id: {}; that id: {}; matches: {}".format(this_id,
                                                                     that_id,
                                                                     matches))
                return this_id, that_id


if __name__ == '__main__':
    this_id, that_id = get_two_ids()

    common = []
    for a, b in zip(this_id, that_id):
        if a == b:
            common.append(a)

    print(''.join(common))

