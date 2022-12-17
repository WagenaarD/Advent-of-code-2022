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


ELEMENTS = (
    [int('0011110', 2)],
    [int('0001000', 2), int('0011100', 2), int('0001000', 2)],
    [int('0000100', 2), int('0000100', 2), int('0011100', 2)],
    [int('0010000', 2), int('0010000', 2), int('0010000', 2), int('0010000', 2)],
    [int('0011000', 2), int('0011000', 2)]
)


def print_chamber(chamber: list, elem: list = [], drop: int = 0) -> None:
    for idx, line in enumerate(chamber[:-1]):
        output = '{:5}. '.format(idx if idx % 1 == 0 else '')
        output += '|{:07b}|'.format(line).replace('0', '.').replace('1', '■')
        if elem:
            if 0 <= idx - drop < len(elem):
                output += ' <-- |{:07b}|'.format(elem[idx - drop]).replace('0', '.').replace('1', '■')
        print(output)
    print('       +{}+\n'.format('-' * 7))



def drop_one_element(chamber: list, elem_idx: int, jet_input: str):
    pass


@print_function(run_time = True,)
def solve_1(input: str, no_elements: int, log_end: bool = False, log_partial: bool = False) -> int:
    chamber = [int('1111111', 2)]
    jet_push_cycle = it.cycle(input)
    for elem_idx in range(no_elements):
        elem = ELEMENTS[elem_idx % len(ELEMENTS)]
        chamber = [int('0000000', 2) for _ in range(len(elem)+3)] + chamber

        # Simulate element motion
        drop = 0
        while True:
            # first, simulate jet push
            if log_partial >= 2:
                print_chamber(chamber, elem, drop)        
            jet_push = next(jet_push_cycle)
            # print('jet_push:', jet_push, '\n')
            if jet_push == '<':
                wall_hit = any([int('1000000', 2) & el_row for el_row in elem])
                elem_hit = False
                elem_hit = any([(elem[idx] << 1) & chamber[idx + drop] for idx in range(len(elem))])
                if not (elem_hit or wall_hit):
                    elem = [el << 1 for el in elem]
            else:
                wall_hit = any([int('0000001', 2) & el_row for el_row in elem])
                elem_hit = False
                elem_hit = any([(elem[idx] >> 1) & chamber[idx + drop] for idx in range(len(elem))])
                if not (elem_hit or wall_hit):
                    elem = [el >> 1 for el in elem]
            
            # second, simulate downword motion
            # print('drop down: V\n')
            down_hit = any([elem[idx] & chamber[idx + drop + 1] for idx in range(len(elem))])
            if down_hit:
                for idx, el in enumerate(elem):
                    chamber[idx + drop] = chamber[idx + drop] | el
                # print('hit bottom')
                break
            else:
                drop += 1
            if drop > len(chamber):
                raise(Exception('Infinite loop gaurd'))
        while chamber[0] == 0:
            chamber.pop(0)
    if log_end:
        print_chamber(chamber)
    return len(chamber) - 1



input = sys.stdin.read().strip()

solve_1(input, 2, True)


print('Part 1:', solve_1(input, 2022))

# 1_000_000_000_000
for idx in [1_000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000, 1_000_000, 10_000_000, 100_000_000, 1_000_000_000, 10_000_000_000, 100_000_000_000, 1_000_000_000]:
    solve_1(input, idx)
