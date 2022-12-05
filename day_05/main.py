"""
Advent of code challenge 2022
Start:  12:27
Part 1: 12:56 - QPJPLMNNR
Part 2: 12:58 - BQDNWJPVJ
"""

__project__   = 'Advent of code 2022'
__author__    = 'D W'

import copy

(warehouse_input, moves_input) = open('input.txt').read().split('\n\n')

# Process the warehouse input. warehouse_1 is for part_1, warehouse_2 for part_2
warehouse_1 = [[] for _ in range((warehouse_input.find('\n') + 1) // 4)]
for line in warehouse_input.split('\n')[:-1]:
    for idx in range(1, len(line), 4):
        if line[idx] != ' ':
            warehouse_1[idx // 4].append(line[idx])
warehouse_2 = copy.deepcopy(warehouse_1)

# Process moves
for move in moves_input.split('\n'):
    (num_to_move, from_stack, to_stack) = [int(num) for num in move.split() if num.isdigit()]
    warehouse_1[to_stack - 1] = list(reversed(warehouse_1[from_stack - 1][:num_to_move])) \
        + warehouse_1[to_stack - 1]
    warehouse_2[to_stack - 1] = warehouse_2[from_stack - 1][:num_to_move] \
        + warehouse_2[to_stack - 1]
    del warehouse_1[from_stack - 1][:num_to_move]
    del warehouse_2[from_stack - 1][:num_to_move]

# Return result
print('Part 1 result: {}'.format(''.join([stack[0] for stack in warehouse_1])))
print('Part 2 result: {}'.format(''.join([stack[0] for stack in warehouse_2])))





