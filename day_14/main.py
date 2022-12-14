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


# @print_function(prefix = ' - ', run_time = True)
def find_next_sand_position(rocks: set, sand: set, floor: bool = False) -> tuple:
    old_path: list = find_next_sand_position.last_path
    for _ in range(len(old_path)):
        x, y = old_path.pop()
        path = old_path[:]
        while True:
            path.append((x, y))
            # print('(x, y)', (x, y))
            # print('path =', path)
            if (x, y) in sand | rocks:
                visualize_grid(rocks, sand)
                raise(Exception('Can\'t place sand'))
            elif y >= find_next_sand_position.y_max:
                # print('Max reached, {} >= {}'.format(y, find_next_sand_position.y_max))
                if floor:
                    find_next_sand_position.last_path = path[:-1]
                    return (x, y)
                else:
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
                find_next_sand_position.last_path = path[:-1]
                return (x, y)
find_next_sand_position.last_path = None
find_next_sand_position.y_max = None

# Start script
lines = sys.stdin.read().strip().split('\n')

# Find rock positions
rocks = set()
for line in lines:
    line_pairs = [tuple(map(int, pair.split(','))) for pair in re.findall('[0-9]+,[0-9]+', line)]
    for ((xs, ys), (xe, ye)) in zip(line_pairs[:-1], line_pairs[1:]):
        dir = (min(1, max(-1, xe - xs)), min(1, max(-1, ye - ys)))
        for idx in range(max(abs(xe - xs), abs(ys - ye)) + 1):
            rocks.add((xs + dir[0] * idx, ys + dir[1] * idx))
# visualize_grid(rocks)

# Calculate part 1
find_next_sand_position.last_path = [(500, 0)]
find_next_sand_position.y_max = max([pair[1] for pair in rocks])
sand = set()
while True:
    next_pos = find_next_sand_position(rocks, sand, False)
    if next_pos == None:
        break
    sand.add(next_pos)
# visualize_grid(rocks, sand)
print('Part 1:', len(sand))

# Calculate initial floor
# x_min = min([pair[0] for pair in rocks | sand])
# x_max = max([pair[0] for pair in rocks | sand])
# y_max = max([pair[1] for pair in rocks | sand])
# for x in range(x_min - 2, x_max + 3):
#     rocks.add((x, y_max + 2))
# visualize_grid(rocks)

find_next_sand_position.last_path = [(500, 0)]
find_next_sand_position.y_max = max([pair[1] for pair in rocks | sand]) + 1
sand = set()
while True:
    next_pos = find_next_sand_position(rocks, sand, True)
    sand.add(next_pos)
    # rocks.add((next_pos[0] - 2, y_max + 2))
    # rocks.add((next_pos[0] + 2, y_max + 2))
    if next_pos == (500, 0):
        break
    # visualize_grid(rocks, sand)
    if len(sand) % 500 == 0:
        print(len(sand))
visualize_grid(rocks, sand)
print('Part 2:', len(sand))
