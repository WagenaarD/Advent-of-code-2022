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
# from _utils.print_function import print_function
# import itertools as it
# from dataclasses import dataclass, field
# from collections import defaultdict
import re
# import numpy as np
from pprint import pprint


lines = sys.stdin.read().strip().split('\n')
y_target = 10 if len(lines) == 14 else 2000000

# lines = [list(map(int, re.findall('[0-9]+', line))) for line in sys.stdin.read().strip().split('\n')]
blocked = set()
beacons = set()
for xs, ys, xb, yb in [list(map(int, re.findall('-?[0-9]+', line))) for line in lines]:
    d_beacon = abs(xb - xs) + abs(yb - ys)
    d_target = abs(y_target - ys)
    # if d_target <= d_beacon:
    for x in range(xs - (d_beacon - d_target), xs + (d_beacon - d_target) + 1):
        blocked.add(x)
    if yb == y_target:
        beacons.add(xb)

print('Part 1:', len(blocked - beacons), ' at row = ', y_target)
    # else:
    #     print(xs, ys, xb, yb, 'NO', d_target, d_beacon)

    # width_at_target_y = (d_beacon - d_target) * 2 + 1




