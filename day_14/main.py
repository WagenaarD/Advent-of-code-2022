"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 
Part 2  - 
Cleanup - 
"""

import sys
sys.path.insert(0, '/'.join(__file__.replace('\\\\', '/').split('/')[:-2]))
from _utils.print_function import print_function
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict
import re
import numpy as np
from pprint import pprint


def visualize_grid(rocks: set, sand: set = set()) -> None:
    x_min = min([pair[0] for pair in rocks | sand])
    x_max = max([pair[0] for pair in rocks | sand])
    y_min = min([pair[1] for pair in rocks | sand])
    y_max = max([pair[1] for pair in rocks | sand])
    print('(x_min, x_max), (y_min, y_max)', (x_min, x_max), (y_min, y_max))

    print('    ' + ' ' * (500 - x_min) + 'V')
    for y in range(y_min, y_max + 1):
        output = '{:3} '.format(y)
        for x in range(x_min, x_max + 1):
            if (x, y) in rocks:
                output += '■'
            elif (x, y) in sand:
                output += 'o'
            else:
                output += '.'
        print(output)


# @print_function(prefix = ' - ')
def find_next_sand_position(rocks: set, sand: set) -> tuple:
    y_max = max([pair[1] for pair in rocks | sand])
    x, y = 500, 0
    while True:
        # print('x, y', x, y)
        if (x, y) in sand | rocks:
            visualize_grid(rocks, sand)
            raise(Exception('Can\'t place sand'))
        elif y >= y_max:
            return None
        elif not (x, y + 1) in (sand | rocks):
            y += 1
        elif not (x - 1, y + 1) in (sand | rocks):
            x -= 1
            y += 1
        elif not (x + 1, y + 1) in (sand | rocks):
            x += 1
            y += 1
        else:
            return (x, y)


input = sys.stdin.read().strip()
print(input)
lines = input.split('\n')

rocks = set()
for line in lines:
    line_pairs = [tuple(map(int, pair.split(','))) for pair in re.findall('[0-9]+,[0-9]+', line)]
    # print('line_pairs', line_pairs)
    for ((xs, ys), (xe, ye)) in zip(line_pairs[:-1], line_pairs[1:]):
        dir = (min(1, max(-1, xe - xs)), min(1, max(-1, ye - ys)))
        # print('(xs, ys), (xe, ye), dir = ', (xs, ys), (xe, ye), dir)
        for idx in range(max(abs(xe - xs), abs(ys - ye)) + 1):
            rocks.add((xs + dir[0] * idx, ys + dir[1] * idx))
        # print('rocks = ', rocks)

visualize_grid(rocks)

sand = set()
while True:
    next_pos = find_next_sand_position(rocks, sand)
    if next_pos == None:
        break
    sand.add(next_pos)
    # visualize_grid(rocks, sand)

visualize_grid(rocks, sand)
print('Part 1:', len(sand))

