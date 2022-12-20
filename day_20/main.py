"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 9945
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


lines = sys.stdin.read().strip().split('\n')

if len(lines) < 10: print(list(map(int, lines)))

input = list(enumerate(map(int, lines)))
print('len(input) =', len(input))

if len(lines) < 10: print('\nInitial arrangement')
if len(lines) < 10: print(', '.join([str(num[1]) for num in input]))
output = input[:]
for idx, num in input[:]:
    # print([out[1] for out in output])
    # print(idx, num)
    
    # Find the index of the current item
    pos = output.index((idx, num))

    new_pos = (pos + num)
    while new_pos < 0:
        new_pos += (len(output) - 1)
    while new_pos >= len(output):
        new_pos -= (len(output) - 1)
    output.remove((idx, num))
    output.insert(new_pos, (idx, num))

    if len(lines) < 10: print('\n{} moves between {} and {}:'.format(num, output[new_pos - 1][1], output[(new_pos + 1) % len(output)][1]))
    if len(lines) < 10: print(', '.join([str(num[1]) for num in output]))

numbers_output = [num[1] for num in output]
pos_0 = numbers_output.index(0)
print('pos_0 =', pos_0)
values = []
for idx in [1000, 2000, 3000]:
    value = numbers_output[(pos_0 + idx) % len(numbers_output)]
    values.append(value)
    print(idx, value)
print('Part 1:', sum(values))



    # break