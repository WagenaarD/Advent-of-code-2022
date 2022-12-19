"""
Advent of code challenge 2022
>> python3 main.py < in
Part 1  - 1365 (ex 33)
Part 2  - 4864 (ex 3472) 
"""

import sys
sys.path.insert(0, '/'.join(__file__.replace('\\', '/').split('/')[:-2]))
from _utils.print_function import print_function
import re
from functools import cache
import math


# Optimization ideas:
#  x delta_t geode shortest -> always geode
#  x Never build more robots than the max. required for that resource
#  x Never build more robots than the robot cap. If none of the top scoring tracks include at least 
#      up to the cap amount of robots, quit.
#  x DIDNT WORK: If obsidian has the next-shortest dt, only consider it.
#  x DIDNT WORK: If obsidian has the next-shortest dt, only consider it or geode
#  x DIDNT WORK: If increasing the cap doesnt improve total_score, quit


@cache
def dfs(blueprint, robot_cap, t = 24, robots = (1,0,0,0), resource = (0,0,0,0)):
    output = []
    delta_ts = []
    for rob in range(4):
        # Optimziation: Don't build more robots than allowed
        if robots[rob] >= robot_cap[rob]:
            delta_ts.append(t)
            continue
        required = blueprint[rob]
        dt = 0
        for res in range(3):
            # Test if we can already produce this
            if required[res] == 0:
                continue
            # Test if we produce this at all
            elif robots[res] == 0:
                dt = t
            # Calculate time to produce this
            else:
                dt = max(dt, 1, 1+math.ceil((required[res] - resource[res]) / robots[res]))
        delta_ts.append(dt)
    if min(delta_ts) == delta_ts[-1]:
        rob == 3
        if delta_ts[rob] < t:
            # Investigate the result of buying this robot next
            output += dfs(
                blueprint,
                robot_cap,
                t - delta_ts[rob],
                tuple(robots[i] + (1 if i == rob else 0) for i in range(4)),
                tuple(resource[i] + robots[i] * delta_ts[rob] - blueprint[rob][i] \
                    for i in range(4)),
            )
    else:
        for rob in range(4):
            if delta_ts[rob] < t:
                # Investigate the result of buying this robot next
                output += dfs(
                    blueprint,
                    robot_cap,
                    t - delta_ts[rob],
                    tuple(robots[i] + (1 if i == rob else 0) for i in range(4)),
                    tuple(resource[i] + robots[i] * delta_ts[rob] - blueprint[rob][i] \
                        for i in range(4)),
                )
    # If nothing is produced, return the result of waiting out the rest of the time
    resource = tuple(resource[i] + robots[i] * t for i in range(4))
    output.append(
        (resource, robots, t)
    )
    return output


@print_function(run_time = True, include_args = False)
def run_dfs(blueprint, t = 24):
    dfs.cache_clear()
    max_cost = [max(bp[i] for bp in blueprint) for i in range(4)]
    max_cost[-1] = t
    cap = tuple(max_cost)
    while True:
        output = dfs(tuple(blueprint), cap, t)
        top_score = max([out[0][3] for out in output])
        max_robots_used = [max([out[1][rob] for out in output if out[0][3] == top_score]) \
            for rob in range(4)]
        new_cap = tuple(min(max_cost[i], max(cap[i], max_robots_used[i] + 1)) for i in range(4))
        if new_cap == cap:
            break
        else:
            cap = new_cap

    return top_score


@print_function(run_time = True, include_args = False)
def solve_1(blueprints):
    total_q = 0
    for idx, blueprint in enumerate(blueprints):
        total_q += (idx + 1) * run_dfs(blueprint, 24)
    return total_q


@print_function(run_time = True, include_args = False)
def solve_2(blueprints):
    result = 1
    for blueprint in blueprints[0:3]:
        result *= run_dfs(blueprint, 32)
    return result


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    
    lines = sys.stdin.read().strip().split('\n')

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

    solve_1(blueprints)
    solve_2(blueprints)
