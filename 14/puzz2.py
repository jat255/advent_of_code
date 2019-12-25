"""
--- Part Two ---

After collecting ORE for a while, you check your cargo hold: 1 trillion
(1000000000000) units of ORE.

With that much ore, given the examples above:

- The 13312 ORE-per-FUEL example could produce 82892753 FUEL.
- The 180697 ORE-per-FUEL example could produce 5586022 FUEL.
- The 2210736 ORE-per-FUEL example could produce 460664 FUEL.

Given 1 trillion ORE, what is the maximum amount of FUEL you can produce?

"""
import networkx as nx
import math
import matplotlib.pyplot as plt

def round_w_base(x, base=10):
    return base * math.ceil(x/base)

def process_reactions(fname, fuel_to_produce=1):

    # print(f'\n{fname}')
    with open(fname, 'r') as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
    
    G = nx.DiGraph()

    for l in lines:
        inp, outp = l.split(' => ')
        if ',' in inp:
            inp = inp.split(', ')
        else:
            inp = [inp]
        inp = [tuple([int(i.split(' ')[0]), i.split(' ')[1]]) for i in inp]

        outp = outp.split(' ')
        outp = int(outp[0]), outp[1]

        for i in inp:
            G.add_edge(i[1], outp[1], 
                       inp_quant=i[0], yield_quant=outp[0], 
                       label=f'I:{i[0]} O:{outp[0]}')

    pos=nx.spring_layout(G)
    nx.draw(G,pos)
    nx.set_node_attributes(G, 0, 'num_required')
    G.nodes['FUEL']['num_required'] = fuel_to_produce
    labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_labels(G,pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    to_analyze = list(reversed(list(nx.topological_sort(G))))
    
    for node in to_analyze:
        in_edges = G.in_edges(node, data=True)
        this_node_needed_N = G.nodes[node]['num_required']
        for e in in_edges:
            extra = 0
            nd = e[0]
            data = e[2]
            rounded_node_N = round_w_base(this_node_needed_N, data['yield_quant'])
            quant_inp = data['inp_quant']
            quant_yield = data['yield_quant']
            stoic_num = math.ceil(rounded_node_N / quant_yield)
            nd_req = quant_inp * stoic_num
            G.nodes[nd]['num_required'] += nd_req
            extra = rounded_node_N - this_node_needed_N
            # print(f'{G.nodes[node]["num_required"]} {node} requires {nd_req} of {nd} ({G.nodes[nd]["num_required"]} {nd} now needed)' + (f' ({extra} extra {node})' if extra > 0 else ''))
            pass

    print(f"{G.nodes['ORE']['num_required']} total ORE required for {fuel_to_produce} FUEL")
    return G.nodes['ORE']['num_required']


def binsearch(lst, target, fname, ore_req):
    min = 0
    max = len(lst)-1
    avg = (min+max)//2
    # uncomment next line for traces
    # print(lst, target, avg, ore_req)
    while (min < max):
        ore_req = process_reactions(fname, lst[avg])
        if (ore_req == target):
            return avg
        elif (ore_req < target):
            return avg + 1 + binsearch(lst[avg+1:], target, fname, ore_req)
        else:
            return binsearch(lst[:avg], target, fname, ore_req)

    # avg may be a partial offset so no need to print it here
    # print("The location of the number in the array is", avg)
    print('')
    return avg if ore_req < target else avg-1

if __name__ == '__main__':

    total_ore = 1000000000000
    
    test3_output = binsearch(range(100000000000), total_ore, '14/test_input3', 0)
    assert test3_output == 82892753
    
    test4_output = binsearch(range(100000000), total_ore, '14/test_input4', 0) 
    assert test4_output == 5586022
    
    test5_output = binsearch(range(10000000), total_ore, '14/test_input5', 0)
    assert test5_output == 460664

    print(f"{total_ore} ORE can produce {binsearch(range(10000000), total_ore, '14/input', 0)} FUEL")

    # Answer is 4366186