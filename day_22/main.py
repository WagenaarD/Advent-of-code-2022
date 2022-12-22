"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 67390
Part 2  - 95291
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

def out_of_bounds(x, y, lines):
    if 0 <= x < len(lines[0]) and 0 <= y < len(lines):
        return lines[y][x] == ' '
    return True
    # if not (0 < y <= len(lines) and 0 < x <= len(lines[0])):
    #     return True
    # else:
    #     return lines[y][x] == ' '

lines = sys.stdin.read().split('\n')

input = re.findall('[0-9]+|[LR]', lines[-1])
lines.pop()
lines.pop()
width = max([len(line) for line in lines])
height = len(lines)
lines = [line + ' ' * (width - len(line)) for line in lines]

# pprint(list(enumerate(lines)))
# print('                1    1    2')
# print('      0    5    0    5    0')
# print('\n'.join(['{:3} - {}'.format(idx, line) for idx, line in enumerate(lines)]))

dir = (1, 0)
x, y = [lines[0].index('.'), 0]

for command_idx, command in enumerate(input[:]):
    print('{}: (pos, dir, command) = {}'.format(command_idx, ((x, y), dir, command)))
    if command in ['R', 'L']:
        dir = rotate(dir, command)
        continue
    for idx in range(int(command)):
        # Move one step at a time
        dx, dy = dir
        next_dir = dir
        next_x, next_y = x + dx, y + dy
        # # Manage wrapping around (Part 1)
        # while lines[(y + dy) % height][(x + dx) % width] == ' ':
        #     dx += dir[0]
        #     dy += dir[1]
        # dx = (x + dx) % width - x
        # dy = (y + dy) % height - y

        if out_of_bounds(next_x, next_y, lines):
            # First find the current face
            face_x = x % 50
            face_y = y % 50
            if x // 50 == 0 and y // 50 == 2:
                # Black
                if dx < 0:
                    next_x, next_y = 50, 49 - face_y
                    next_dir = (1, 0)
                elif dy < 0:
                    next_x, next_y = 50, 50 + face_x
                    next_dir = (1, 0)
                else:
                    raise(Exception('WTF: (x, y) (next_x, next_y) {} {}'.format((x, y), (next_x, next_y))))
            elif x // 50 == 0 and y // 50 == 3:
                # Green
                if dx < 0:
                    next_x, next_y = 50 + face_y, 0
                    next_dir = (0, 1)
                elif dx > 0:
                    next_x, next_y = 50 + face_y, 149
                    next_dir = (0, -1)
                elif dy > 0:
                    next_x, next_y = 100 + face_x, 0
                    next_dir = (0, 1)
                else:
                    raise(Exception('WTF: (x, y) (next_x, next_y) {} {}'.format((x, y), (next_x, next_y))))
            elif x // 50 == 1 and y // 50 == 0:
                # White
                if dx < 0:
                    next_x, next_y = 0, 149 - face_y
                    next_dir = (1, 0)
                elif dy < 0:
                    next_x, next_y = 0, 150 + face_x
                    next_dir = (1, 0)
                else:
                    raise(Exception('WTF: (x, y) (next_x, next_y) {} {}'.format((x, y), (next_x, next_y))))
            elif x // 50 == 1 and y // 50 == 1:
                # Blue
                if dx < 0:
                    next_x, next_y = face_y, 100
                    next_dir = (0, 1)
                elif dx > 0:
                    next_x, next_y = 100 + face_y, 49
                    next_dir = (0, -1)
                else:
                    raise(Exception('WTF: (x, y) (next_x, next_y) {} {}'.format((x, y), (next_x, next_y))))
            elif x // 50 == 1 and y // 50 == 2:
                # Yellow
                if dx > 0:
                    next_x, next_y = 149, 49 - face_y
                    next_dir = (-1, 0)
                elif dy > 0:
                    next_x, next_y = 49, 150 + face_x
                    next_dir = (-1, 0)
                else:
                    raise(Exception('WTF: (x, y) (next_x, next_y) {} {}'.format((x, y), (next_x, next_y))))
            elif x // 50 == 2 and y // 50 == 0:
                # Red
                if dx > 0:
                    next_x, next_y = 99, 149 - face_y
                    next_dir = (-1, 0)
                elif dy < 0:
                    next_x, next_y = face_x, 199
                    next_dir = (0, -1)
                elif dy > 0:
                    next_x, next_y = 99, 50 + face_x
                    next_dir = (-1, 0)
                else:
                    raise(Exception('WTF: (x, y) (next_x, next_y) {} {}'.format((x, y), (next_x, next_y))))
            dx, dy = next_x - x, next_y - y
            print('  Changed cube face: {} -> {}'.format((x, y, dir), (next_x, next_y, next_dir)))
            if (out_of_bounds(next_x, next_y, lines)):
                raise(Exception(('  Out of bounds'))

        # Manage walls
        if lines[next_y][next_x] == '#':
            print('  Brick at {}'.format((next_x, next_y)))
            break
        elif lines[next_y][next_x] == '.':
            x, y, dir = next_x, next_y, next_dir
print('(pos, dir, command) =', ((x, y), dir, 'DONE'))

print('Final score:', 1000 * (y + 1) + 4 * (x + 1) + DIR_SCORE[dir])
    
        

    
