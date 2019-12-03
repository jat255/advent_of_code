"""
--- Part Two --- 
It turns out that this circuit is very timing-sensitive; you
actually need to minimize the signal delay.

To do this, calculate the number of steps each wire takes to reach each
intersection; choose the intersection where the sum of both wires' steps is
lowest. If a wire visits a position on the grid multiple times, use the steps
value from the first time it visits that position when calculating the total
value of a specific intersection.

The number of steps a wire takes is the total number of grid squares the wire
has entered to get to that location, including the intersection being
considered. Again consider the example from above:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........

In the above example, the intersection closest to the central port is reached
after 8+5+5+2 = 20 steps by the first wire and 7+6+4+3 = 20 steps by the second
wire for a total of 20+20 = 40 steps.

However, the top-right intersection is better: the first wire takes only 8+5+2 =
15 and the second wire takes only 7+6+2 = 15, a total of 15+15 = 30 steps.

Here are the best steps for the extra examples from above:

- R75,D30,R83,U83,L12,D49,R71,U7,L72
  U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
- R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
  U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps 

What is the fewest combined steps the wires must take to reach an
intersection?
"""


if __name__ == '__main__':
    # matplotlib.use('Qt5Agg')

    with open('03/input', 'r') as f:
        lines = f.readlines()

    wire1 = [i.strip('\n') for i in lines[0].split(',')]
    wire2 = [i.strip('\n') for i in lines[1].split(',')]

    length = 200000
    wire1_pos = [(0,0)] * length
    
    i = 0
    for instruction in wire1:
        direction = instruction[0]
        distance = int(instruction[1:])
        cur_pos = wire1_pos[i]
        if direction == 'R':
            for j in range(distance):
                next_pos = (cur_pos[0] + 1, cur_pos[1])
                wire1_pos[i+1] = next_pos
                cur_pos = next_pos
                i += 1
        elif direction == 'L':
            for j in range(distance):
                next_pos = (cur_pos[0] - 1, cur_pos[1])
                wire1_pos[i+1] = next_pos
                cur_pos = next_pos
                i += 1
        elif direction == 'U':
            for j in range(distance):
                next_pos = (cur_pos[0] , cur_pos[1] + 1)
                wire1_pos[i+1] = next_pos
                cur_pos = next_pos
                i += 1
        elif direction == 'D':
            for j in range(distance):
                next_pos = (cur_pos[0] , cur_pos[1] - 1)
                wire1_pos[i+1] = next_pos
                cur_pos = next_pos
                i += 1
        
    wire2_pos = [(0,0)] * length
    i = 0
    for instruction in wire2:
        direction = instruction[0]
        distance = int(instruction[1:])
        cur_pos = wire2_pos[i]
        if direction == 'R':
            for j in range(distance):
                next_pos = (cur_pos[0] + 1, cur_pos[1])
                wire2_pos[i+1] = next_pos
                cur_pos = next_pos
                i += 1
        elif direction == 'L':
            for j in range(distance):
                next_pos = (cur_pos[0] - 1, cur_pos[1])
                wire2_pos[i+1] = next_pos
                cur_pos = next_pos
                i += 1
        elif direction == 'U':
            for j in range(distance):
                next_pos = (cur_pos[0] , cur_pos[1] + 1)
                wire2_pos[i+1] = next_pos
                cur_pos = next_pos
                i += 1
        elif direction == 'D':
            for j in range(distance):
                next_pos = (cur_pos[0] , cur_pos[1] - 1)
                wire2_pos[i+1] = next_pos
                cur_pos = next_pos
                i += 1
        
        
    
    for i in range(length-1, 0, -1):
        if wire1_pos[i] == (0,0):
            last_wire1_index = i - 1
        if wire2_pos[i] == (0,0):
            last_wire2_index = i - 1
    
    print(last_wire1_index)
    print(last_wire2_index)

    wire1_pos = wire1_pos[:last_wire1_index]
    wire2_pos = wire2_pos[:last_wire2_index]

    intersections = set(wire1_pos) & set(wire2_pos)
    times = [0] * len(intersections)
    for i, (x, y) in enumerate(intersections):
        wire1_steps = wire1_pos.index((x, y))
        wire2_steps = wire2_pos.index((x, y))
        times[i] = wire1_steps + wire2_steps

    while 0 in times:
        times.remove(0)
    print(times)
    # print(wire1_pos[:5])
    # print(wire2_pos[:5])
    print(min(times))

    # Answer is 