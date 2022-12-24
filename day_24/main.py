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
from _utils.print_function import print_function
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict
import re
import numpy as np
from pprint import pprint
from functools import cache


def print_grid(blizzards, start, end, width, height, stack = []):
    print('■' * (start[1] + 1) + '.' + '■' * (width - start[1]))
    for row in range(height):
        output = '■'
        for col in range(width):
            bs = [b for b in blizzards if b[0] == row and b[1] == col]
            if len(bs) > 1:
                output += str(len(bs))
            elif len(bs) == 1:
                output += bs[0][2]
            elif (row, col) in stack:
                output += 'E'
            else:
                output += '.'
        print(output + '■')
    print('■' * (end[1] + 1) + '.' + '■' * (width - end[1]))
    print('')


DIRS = {
    '>': ( 0,  1),
    '<': ( 0, -1),
    '^': (-1,  0),
    'v': ( 1,  0),
}
MOVES = ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))


def move_blizzards(blizzards, width, height):
    new_bs = []
    for r, c, dir in blizzards:
        dr, dc = DIRS[dir]
        rr, cc = (r + dr) % height, (c + dc) % width
        new_bs.append((rr, cc, dir))
    return new_bs


@print_function()
def bfs(blizzards, start, end, width, height):
    t = 0
    stack = {start}
    # print_grid(blizzards, start, end, width, height, stack)
    while len(stack) >= 1:
        # print('== Minute {}, stack {} =='.format(t, stack))
        # print_grid(blizzards, start, end, width, height, stack)
        t += 1
        blizzards = move_blizzards(blizzards, width, height)
        # for row, col in stack[:]:
        old_stack = stack
        stack = set()
        for row, col in old_stack:
            # row, col = stack.pop(0)
            for drow, dcol in MOVES:
                nrow, ncol = row + drow, col + dcol
                if (nrow, ncol) == end:
                    return (t, blizzards)
                if 0 <= nrow < height and 0 <= ncol < width or (nrow, ncol) == start:
                    if len([b for b in blizzards if b[0] == nrow and b[1] == ncol]) == 0:
                        stack.add((nrow, ncol))
                        

    

lines = sys.stdin.read().strip().split('\n')
# lines[row][col]
# Blizzards in grid starting at [0][0]
start = (-1, lines[0].index('.') - 1)
end = (len(lines) - 2, lines[-1].index('.') - 1)
width = len(lines[0])-2
height = len(lines) - 2
blizzards = []
for row, line in enumerate(lines[1:-1]):
    for col, char in enumerate(line[1:-1]):
        if char != '.':
            blizzards.append((row, col, char))

t_0, blizzards = bfs(blizzards, start, end, width, height)

t_1, blizzards = bfs(blizzards, end, start, width, height)
t_2, blizzards = bfs(blizzards, start, end, width, height)
print(t_0, t_1, t_2, t_0 + t_1 + t_2)



