"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 11:39
Part 1  - 12:06
Part 2  - 
Cleanup - 
"""

import sys
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict
import re
from pprint import pprint


input_lines = sys.stdin.read().strip().split('\n')

for line in input_lines:
    print(line)




monkeys = []
for line in input_lines:
    if line.startswith('Monkey'):
        new_monkey = {'inspected': 0}
    elif line.startswith('  Starting items'):
        new_monkey['items'] = list(map(int, re.findall('[0-9]+', line)))
    elif line.startswith('  Operation'):
        new_monkey['operation'] = line[19:]
    elif line.startswith('  Test'):
        new_monkey['test'] = int(re.findall('[0-9]+', line)[0])
    elif line.startswith('    If true'):
        new_monkey['true_target'] = int(re.findall('[0-9]+', line)[0])
    elif line.startswith('    If false'):
        new_monkey['false_target'] = int(re.findall('[0-9]+', line)[0])
        monkeys.append(new_monkey)
print('\nMonkeys:')
pprint(monkeys)


def report_status(monkeys, round):
    print('After round {}, the monkeys are holding items with these worry levels:'.format(round))
    for idx, monkey in enumerate(monkeys):
        print('Monkey {}: {}'.format(idx, ', '.join([str(item) for item in monkey['items']])))
    

report_status(monkeys, 0)
for round in range(20):
    for idx, monkey in enumerate(monkeys):
        # print('Monkey {}:'.format(idx))
        for item in monkey['items']:
            # print('  Monkey inspects an item with a worry level of {}.'.format(item))
            monkey['inspected'] += 1
            item = eval(monkey['operation'].replace('old', 'item'))
            # print('    Worry level is changed ({}) to {}.'.format(monkey['operation'], item))
            item //= 3
            # print('    Monkey gets bored with item. Worry level is divided by 3 to {}.'.format(item))
            target = monkey['true_target'] if item % monkey['test'] == 0 else monkey['false_target']
            monkeys[target]['items'].append(item)
            # print('    Item with worry level {} is thrown to monkey {}.'.format(item, target))
        monkey['items'] = []
    report_status(monkeys, round+1)

inspected_counts = [monkey['inspected'] for monkey in monkeys]
print(inspected_counts)
print('Part 1:', max(inspected_counts) * sorted(inspected_counts)[-2])


