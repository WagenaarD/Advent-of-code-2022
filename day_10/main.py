"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 09:56
Part 1  - 09:12
Part 2  - 09:23
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
x_values = {cycle: x}
for line in input:
    if line == 'noop':
        cycle += 1
    else:
        amount = int(line.split()[1])
        x_values[cycle+1] = x
        cycle += 2
        x += amount
    x_values[cycle] = x
print('Part 1:', sum([c * x_values[c] for c in (20, 60, 100, 140, 180, 220)]))

output = ''
for cycle, x in x_values.items():
    if (cycle - 1) % 40 + 1 in [x, x+1, x+2]:
        output += '#'
    else:
        output += '.'
    if cycle >= 240:
        break
    elif cycle % 40 == 0:
        output += '\n'
print('Part 2:\n' + output)


