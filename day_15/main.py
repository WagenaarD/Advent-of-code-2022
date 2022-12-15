"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 4737443 (ex 26)
Part 2  - (ex 56000011)
Cleanup - 
"""

import sys
sys.path.insert(0, '/'.join(__file__.replace('\\', '/').split('/')[:-2]))
from _utils.print_function import print_function
# import itertools as it
# from dataclasses import dataclass, field
# from collections import defaultdict
import re
# import numpy as np
from pprint import pprint


def can_be_beacon(x: int, y: int, sensors: list) -> bool:
    for (sx, sy, sd) in sensors:
        coord_distance = abs(sx - x) + abs(sy - y)
        if coord_distance <= sd:
            return False
    return True



@print_function(run_time = True)
def solve_part_1(int_line):
    y_target = 10 if len(int_lines) == 14 else 2000000

    # 
    blocked = set()
    beacons = set()
    for xs, ys, xb, yb in int_lines:
        d_beacon = abs(xb - xs) + abs(yb - ys)
        d_row = abs(y_target - ys)
        for x in range(xs - (d_beacon - d_row), xs + (d_beacon - d_row) + 1):
            blocked.add(x)
        if yb == y_target:
            beacons.add(xb)
    return len(blocked - beacons)
    # print('Part 1:', len(blocked - beacons), {'y': y_target})

@print_function(run_time = True)
def solve_part_2(int_lines):
    # # The following is already too slow, we need to find a quicker way for part 2!:
    # for x in range(xy_max + 1):
    #     for y in range(xy_max + 1):
    #         x + y

    xy_max = 20 if len(int_lines) == 14 else 4000000

    # New approach, scan only the edges of the sensor ranges
    sensors = [(s[0], s[1], abs(s[0] - s[2]) + abs(s[1] - s[3])) for s in int_lines]
    sensors.sort(key = lambda x: x[2])
    for idx, (sx, sy, sd) in enumerate(sensors):
        print('Progress = {:%}'.format(idx / len(sensors)))
        for x in range(sx - (sd + 1), sx + (sd + 1) + 1):
            if not 0 <= x <= xy_max:
                continue
            dy = (sd + 1) - abs(x - sx)
            for y in {sy - dy, sy + dy}:
                if not 0 <= y <= xy_max:
                    continue
                if can_be_beacon(x, y, sensors):
                    return x * 4000000 + y

if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    lines = sys.stdin.read().strip().split('\n')
    int_lines = [list(map(int, re.findall('-?[0-9]+', line))) for line in lines]

    print('Part 1:', solve_part_1(int_lines))
    print('Part 1:', solve_part_2(int_lines))





