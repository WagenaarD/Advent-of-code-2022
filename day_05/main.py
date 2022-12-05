"""
Advent of code challenge 2022
Start 12:27
Part 1: 12:56 - QPJPLMNNR
Part 2: 12:58 - BQDNWJPVJ
"""

__project__   = 'Advent of code 2022'
__author__    = 'D W'

(warehouse_input, moves_input) = open('input.txt').read().split('\n\n')

# Get the warehouse input
warehouse = [[] for _ in range((warehouse_input.find('\n') + 1) // 4)]
for line in warehouse_input.split('\n')[:-1]:
    for idx in range(1, len(line), 4):
        if line[idx] != ' ':
            warehouse[idx // 4].append(line[idx])
print(warehouse)

# Process moves
for move in moves_input.split('\n'):
    (num_to_move, from_stack, to_stack) = [int(num) for num in move.split() if num.isdigit()]
    
    print(num_to_move, from_stack, to_stack)
    # warehouse[to_stack - 1] = list(reversed(warehouse[from_stack - 1][:num_to_move])) + warehouse[to_stack - 1]
    warehouse[to_stack - 1] = warehouse[from_stack - 1][:num_to_move] + warehouse[to_stack - 1]
    print(warehouse)
    del warehouse[from_stack - 1][:num_to_move]
    print(warehouse)

print('Part 1 result: {}'.format(''.join([stack[0] for stack in warehouse])))





