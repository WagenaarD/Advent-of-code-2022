"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 
Part 2  - 
Cleanup - 
"""

import sys
sys.path.insert(0, '/'.join(__file__.replace('\\', '/').split('/')[:-2]))
from _utils.print_function import print_function
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict
import re
import numpy as np
from pprint import pprint

# @print_function()
def valve_path(source, target, d = 0):
    """
    Returns a shortest path between the source and the target. 

    Broad first increase of both source and target until they overlap. Once they overlap, the same 
    algorithm is done between the source and the overlapping node and the node to the target. 
    At some point the source and terget are next to eachother and the direct path is returned
    
    Holy fuck this actually worked.
    """
    # If next to eachother return result
    if target in valves[source][1]:
        return [source, target]
    # Look from both ends
    source_keys, target_keys = [source], [target]
    source_depth, target_depth = 0, 0
    while True:
        source_depth += 1
        target_depth += 1
        for key in source_keys[:]:
            for valve in valves[key][1]:
                if valve not in source_keys:
                    source_keys.append(valve)
                    if valve in target_keys:
                        return valve_path(source, valve, d+1)[:-1] + valve_path(valve, target, d+1)
        for key in target_keys[:]:
            for valve in valves[key][1]:
                if valve not in target_keys:
                    target_keys.append(valve)
                    if valve in source_keys:
                        return valve_path(source, valve, d+1)[:-1] + valve_path(valve, target, d+1)
    

def get_all_paths(keys, path = ['AA'], t = 0, flow = 0, released = 0, tmax = 30):
    """
    Broad first algorithm. Calculates the release for every possible path between keys without 
    exceeding tmax.
    """
    paths = []
    for key in keys:
        if key not in path:
            delta_t = len(valve_path(path[-1], key)) - 1 + 1
            # if ', '.join(path + [key]) in 'AA, DD, BB, JJ, HH, EE, CC':
            #     # print('path: {} - t {}'.format(path + [key], t + delta_t))
            #     print('path: {}, t={}, f={}, r={}'.format(
            #         path + [key], t + delta_t, flow + valves[key][0], released + flow * delta_t
            #     ))
            if t + delta_t < tmax:
                paths += get_all_paths(
                    keys, 
                    path + [key], 
                    t + delta_t,
                    flow = flow + valves[key][0],
                    released = released + flow * delta_t,
                )
    if not paths:
        paths = [(path, released + flow * (tmax - t))]
    return paths


lines = sys.stdin.read().strip().split('\n')

# Process input
valves = {}
for line in lines:
    valves[line[6:8]] = (
        int(re.findall('[0-9]+', line)[0]),
        line.replace(',', '').split()[9:],
    )

# Part 1
non_zero_valves = {key: value for key, value in valves.items() if value[0] > 0}
pprint(non_zero_valves)
options = get_all_paths(list(non_zero_valves.keys()))
print('Part 1:', max([opt[1] for opt in options]))
