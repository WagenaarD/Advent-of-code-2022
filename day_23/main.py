"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 3966
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


DIRECTIONS = ('NSWE', 'SWEN', 'WENS', 'ENSW')
# DIR = {
#     'N': (-1,  0),
#     'S': ( 1,  0),
#     'W': ( 0, -1),
#     'E': ( 0,  1),
# }
# SURROUND = ()
DIR_CHECK = {
    'N': ((-1, -1), (-1,  1), (-1,  0)), 
    'S': (( 1, -1), ( 1,  1), ( 1,  0)), 
    'W': ((-1, -1), ( 1, -1), ( 0, -1)), 
    'E': ((-1,  1), ( 1,  1), ( 0,  1)), 
}


def print_board(elves):
    min_row = min([elf[0] for elf in elves])
    max_row = max([elf[0] for elf in elves])
    min_col = min([elf[1] for elf in elves])
    max_col = max([elf[1] for elf in elves])
    for row in range(min_row - 1, max_row + 2):
        output = '{:3} - '.format(row)
        for col in range(min_col - 1, max_col + 2):
            output += '#' if (row, col) in elves else '.'
        print(output)
    print('')


lines = sys.stdin.read().strip().split('\n')
elves = list()
for row, line in enumerate(lines):
    for col, char in enumerate(line):
        if char == '#':
            elves.append((row, col))

print_board(elves)

dir_cycle = it.cycle(DIRECTIONS)
for round in range(10):
    # First half of round
    new_positions = list()
    dir = next(dir_cycle)
    for row, col in elves:
        # Consider eight cells around. Only move if at least one other elf present
        no_neighbours = sum([(nrow, ncol) in elves \
            for nrow in range(row-1, row+2) for ncol in range(col-1, col+2)]) - 1
        # print('(row, col, no_neighbours)', (row, col, no_neighbours))
        if no_neighbours == 0:
            new_positions.append((row, col, row, col))
            continue
        # Consider all directions
        for dir_key in dir:
            for drow, dcol in DIR_CHECK[dir_key]:
                if (row + drow, col + dcol) in elves:
                    break
            else:
                # drow, dcol = DIR[dir_key]
                # new_positions.append((row + drow, col + dcol))
                new_positions.append((row + drow, col + dcol, row, col))
                break
        else:
            # No new position found. Do not move
            new_positions.append((row, col, row, col))
    # Second half of round
    move_targets = [(pos[0], pos[1]) for pos in new_positions]
    elves = list()
    vectors = set()
    for nrow, ncol, row, col in new_positions:
        if move_targets.count((nrow, ncol)) == 1:
            vectors.add((nrow - row, ncol - col))
            elves.append((nrow, ncol))
        else:
            vectors.add((0, 0))
            elves.append((row, col))
    print('== End of Round {} =='.format(round + 1))
    print_board(elves)
    if len(vectors) == 1:
        break
min_row = min([elf[0] for elf in elves])
max_row = max([elf[0] for elf in elves])
min_col = min([elf[1] for elf in elves])
max_col = max([elf[1] for elf in elves])

print('Part 1', (max_row - min_row + 1) * (max_col - min_col + 1) - len(elves))

    
            



