"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 09:12
Part 2  - 
Cleanup - 
"""

import sys
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict
import re
import pprint


input = sys.stdin.read().strip().split('\n')

x, cycle = 1, 1
# x_values = []
x_values = {cycle: x}
for line in input:
    print(cycle, x, line)
    if line == 'noop':
        cycle += 1
    else:
        amount = int(line.split()[1])
        x_values[cycle+1] = x
        cycle += 2
        x += amount
    x_values[cycle] = x
print(cycle, x, 'done')

print([x_values[c] for c in (20, 60, 100, 140, 180, 220)])
print([c * x_values[c] for c in (20, 60, 100, 140, 180, 220)])
print('Part 1:', sum([c * x_values[c] for c in (20, 60, 100, 140, 180, 220)]))


