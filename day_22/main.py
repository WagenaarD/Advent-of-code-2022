"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 67390
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

DIR_SCORE = {
    (1, 0): 0,  # >
    (0, 1): 1,  # v
    (-1, 0): 2, # <
    (0, -1): 3, # ^
}
# rotate = lambda dir, lr: (dir[1], -dir[0]) if lr == 'R' else (-dir[1], dir[0])
def rotate(dir, lr):
    """
    Assuming grid that goes like:
    O--------> + x
    |
    |
    |
    V 
    + y
    """
    assert lr in ['R', 'L']
    if lr == 'R':
        return (-dir[1], dir[0])
    else:
        return (dir[1], -dir[0])



lines = sys.stdin.read().split('\n')

input = re.findall('[0-9]+|[LR]', lines[-1])
lines.pop()
lines.pop()
width = max([len(line) for line in lines])
height = len(lines)
lines = [line + ' ' * (width - len(line)) for line in lines]

pprint(list(enumerate(lines)))
print('                1    1    2')
print('      0    5    0    5    0')
print('\n'.join(['{:3} - {}'.format(idx, line) for idx, line in enumerate(lines)]))

dir = (1, 0)
x, y = [lines[0].index('.'), 0]

for command in input:
    print('(pos, dir, command) =', ((x, y), dir, command)) 
    if command in ['R', 'L']:
        dir = rotate(dir, command)
        continue
    for idx in range(int(command)):
        dx, dy = dir
        # Manage wrapping around
        while lines[(y + dy) % height][(x + dx) % width] == ' ':
            dx += dir[0]
            dy += dir[1]
        dx = (x + dx) % width - x
        dy = (y + dy) % height - y

        # Manage walls
        if lines[y + dy][x + dx] == '#':
            break
        elif lines[y + dy][x + dx] == '.':
            x, y = (x + dx, y + dy)
print('(pos, dir, command) =', ((x, y), dir, 'DONE'))

print('Final score:', 1000 * (y + 1) + 4 * (x + 1) + DIR_SCORE[dir])
    
        

    
