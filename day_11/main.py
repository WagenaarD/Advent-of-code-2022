"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 11:39
Part 1  - 12:06 - 57838
Part 2  - 12:13 - 15077002392
Cleanup - 
"""

import sys
import re
import numpy
from pprint import pprint


def simulate_monkey_throws(monkeys, test_product = 1, no_rounds = 20, divide = True, log_print = False):
    log = lambda x: print(x) if log_print else None
    for round in range(no_rounds):
        for idx, monkey in enumerate(monkeys):
            log('Monkey {}:'.format(idx))
            for item in monkey['items']:
                log('  Monkey inspects an item with a worry level of {}.'.format(item))
                monkey['inspected'] += 1
                item = eval(monkey['operation'].replace('old', 'item'))
                item = item % test_product
                log('    Worry level is changed ({}) to {}.'.format(monkey['operation'], item))
                if divide:
                    item //= 3
                log('    Monkey gets bored with item. Worry level is divided by 3 to {}.'.format(item))
                target = monkey['true_target'] if item % monkey['test'] == 0 else monkey['false_target']
                monkeys[target]['items'].append(item)
                log('    Item with worry level {} is thrown to monkey {}.'.format(item, target))
            monkey['items'] = []
        log('After round {}, the monkeys are holding items with these worry levels:'.format(round))
        for idx, monkey in enumerate(monkeys):
            log('Monkey {}: {}'.format(idx, ', '.join([str(item) for item in monkey['items']])))
    return monkeys

if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    monkeys = [{
        'inspected': 0,
        'items': list(map(int, re.findall('[0-9]+', line_set[1]))),
        'operation': line_set[2][19:],
        'test': int(re.findall('[0-9]+', line_set[3])[0]),
        'true_target': int(re.findall('[0-9]+', line_set[4])[0]),
        'false_target': int(re.findall('[0-9]+', line_set[5])[0]),
    } for line_set in [lines.split('\n') for lines in sys.stdin.read().strip().split('\n\n')]]
    # pprint(monkeys)

    test_product = numpy.prod([monkey['test'] for monkey in monkeys])
    print('test_product =', test_product)

    monkeys_p1 = simulate_monkey_throws(monkeys, test_product, 20, True)
    inspected_counts = [monkey['inspected'] for monkey in monkeys_p1]
    print('Part 1:', max(inspected_counts) * sorted(inspected_counts)[-2])

    monkeys_p2 = simulate_monkey_throws(monkeys, test_product, int(1E4), False)
    inspected_counts = [monkey['inspected'] for monkey in monkeys_p2]
    print('Part 2:', max(inspected_counts) * sorted(inspected_counts)[-2])



