"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 1365 (ex 33)
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
from functools import cache
import math


@cache
def dfs(blueprint, robot_cap, t = 24, robots = (1,0,0,0), resource = (0,0,0,0), order = ''):
    # We have three options and a non-option: Create one of three robots or wait out the time
    output = []
    # if '11121233'.startswith(order):
    # if '0011111222223233'.startswith(order):
    #     print('(t, 25-t, robots, resource) =', (t, 25-t, robots, resource))
    for rob in range(4):
        # Optimization: Don't build more of a robot than you can use per minute
        if robots[rob] >= max([bp[rob] for bp in blueprint for rob in range(4)]):
            continue
        # Optimziation: Don't build more robots than allowed
        if robots[rob] >= robot_cap[rob]:
            continue
        required = blueprint[rob]
        delta_t = 0
        for res in range(3):
            # Test if we can already produce this
            if required[res] == 0:
                continue
            # Test if we produce this at all
            elif robots[res] == 0:
                delta_t = t + 1
            # Calculate time to produce this
            else:
                delta_t = max(delta_t, 1, 1+math.ceil((required[res] - resource[res]) / robots[res]))
        if delta_t >= t:
            continue
        # Investigate the result of buying this robot next
        output += dfs(
            blueprint,
            robot_cap,
            t - delta_t,
            tuple(robots[i] + (1 if i == rob else 0) for i in range(4)),
            tuple(resource[i] + robots[i] * delta_t - required[i] for i in range(4)),
            order + str(rob),
        )
    # If nothing is produced, return the result of waiting out the rest of the time
    resource = tuple(resource[i] + robots[i] * t for i in range(4))
    output.append(
        (resource, robots, order, t)
    )
    return output


@print_function(run_time = True)
def run_dfs(blueprint):
    dfs.cache_clear()
    print('blueprint =', blueprint)
    max_cost = [max(bp[i] for bp in blueprint) for i in range(4)]
    max_cost[3] = 24
    print('max_cost =', max_cost)
    cap = (3, 3, 10, 25)
    for iter_idx in range(20):
        output = dfs(tuple(blueprint), cap)
        top_score = max([out[0][3] for out in output])
        max_used_robots = [max([out[1][rob] for out in output if out[0][3] == top_score]) for rob in range(4)]
        new_cap = tuple(min(max_cost[i], max(cap[i], max_used_robots[i] + 1)) for i in range(4))
        print('(iter_idx, top_score, cap) =', (iter_idx, top_score, cap))
        if new_cap == cap:
            break
        else:
            cap = new_cap
    min_no_robots = min([sum(out[1]) for out in output if out[0][3] == top_score])
    best_out = [out for out in output if sum(out[1]) == min_no_robots and out[0][3] == top_score][0]
    print('(score, robots, order, t) =', (top_score, best_out[1], best_out[2], best_out[3]))

    return top_score


@print_function(run_time = True)
def solve(lines):
    blueprints = []
    for line in lines:
        blueprint = []
        for robot in line.split('.')[:-1]:
            blueprint.append(tuple(map(int, (
                re.findall('(\d+) ore', robot)[0] if re.findall('(\d+) ore', robot) else 0,
                re.findall('(\d+) clay', robot)[0] if re.findall('(\d+) clay', robot) else 0,
                re.findall('(\d+) obsidian', robot)[0] if re.findall('(\d+) obsidian', robot) else 0,
                0,
            ))))
        blueprints.append(blueprint)
    
    total_q = 0
    # for idx, blueprint in enumerate(blueprints[0:1]):
    for idx, blueprint in enumerate(blueprints):
        total_q += (idx + 1) * run_dfs(blueprint)
    print('Part 1:', total_q)


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    
    lines = sys.stdin.read().strip().split('\n')
    solve(lines)






