"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 795
Part 2  - 30214
Cleanup - 

Not a very fast implementation. Keeping a set and storing all positions is faster for part 1 but 
slower for part 2 compared to keeping track of a grid and all items in it (how Tamara did it). Code
had to be optimized as it would initially take too long (minutes to reach 10.000 and slowing down 
each iteration). Current version was 0.07s for part 1, and 50s for part 2.
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

    print('    ' + ' ' * (501 - x_min) + 'V')
    for y in range(y_min, y_max + 1):
        output = '{:3} '.format(y)
        for x in range(x_min - 1, x_max + 2):
            if (x, y) in rocks:
                output += '■'
            elif (x, y) in sand:
                output += 'o'
            else:
                output += '.'
        print(output)


def find_next_sand_position(rocks: set, sand: set, floor: bool = False) -> tuple:
    old_path: list = find_next_sand_position.last_path
    for _ in range(len(old_path)):
        x, y = old_path.pop()
        path = old_path[:]
        while True:
            path.append((x, y))
            if (x, y) in sand | rocks:
                visualize_grid(rocks, sand)
                raise(Exception('Can\'t place sand'))
            elif y >= find_next_sand_position.y_max:
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


@print_function(prefix = ' - ', run_time = True)
def solve(rocks: set, y_max: int, floor: bool) -> int:
    find_next_sand_position.last_path = [(500, 0)]
    find_next_sand_position.y_max = y_max
    sand = set()
    while True:
        next_pos = find_next_sand_position(rocks, sand, floor)
        if next_pos == None:
            break
        sand.add(next_pos)
    visualize_grid(rocks, sand)

    return len(sand)


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    
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
    visualize_grid(rocks)
    y_max = max([pair[1] for pair in rocks])

    # Calculate result
    print('Part 1:', solve(rocks, y_max, False))
    print('Part 2:', solve(rocks, y_max + 1, True))
