"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - Forgot
Part 1  - Forgot - 391
Part 2  - Forgot - 386
Cleanup - Forgot
"""

import sys


def find_steps_between_points(start_positions, end_pos, lines):
    steps = 0
    visited = start_positions
    stack = start_positions[:]
    while not end_pos in visited and len(stack) > 0:
        for pos in stack[:]:
            for dir in ((1,0), (-1,0), (0,1), (0,-1)):
                new_pos = (pos[0] + dir[0], pos[1] + dir[1])
                if (0 <= new_pos[0] < len(lines) and 0 <= new_pos[1] < len(lines[0])) and \
                    (not new_pos in visited) and \
                    ord(lines[new_pos[0]][new_pos[1]]) - ord(lines[pos[0]][pos[1]]) <= 1:
                        visited.append(new_pos)
                        stack.append(new_pos)
            stack.remove(pos)
        steps += 1
    return steps


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""

    lines = sys.stdin.read().strip().split('\n')

    for row, line in enumerate(lines):
        if 'S' in line:
            start_pos = (row, line.index('S'))
        if 'E' in line:
            end_pos = (row, line.index('E'))
        lines[row] = lines[row].replace('E', 'z').replace('S', 's')

    print('Part 1:', find_steps_between_points([start_pos], end_pos, lines))
    a_positions = [(row, col) for row in range(len(lines)) for col in range(len(lines[0])) \
        if lines[row][col] == 'a']
    print('Part 2:', find_steps_between_points(a_positions, end_pos, lines))