"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 3181, ex 3068
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
FULL_ROW = int('1111111', 2)
EMPTY_ROW = int('0000000', 2)


def print_chamber(chamber: list, elem: list = [], drop: int = 0) -> None:
    for idx, line in enumerate(chamber[:-1]):
        output = '{:5}. '.format(idx if idx % 1 == 0 else '')
        output += '|{:07b}|'.format(line).replace('0', '.').replace('1', '■')
        if elem:
            if 0 <= idx - drop < len(elem):
                output += ' <-- |{:07b}|'.format(elem[idx - drop]).replace('0', '.').replace('1', '■')
        print(output)
    print('       +{}+\n'.format('-' * 7))


# @cache
def drop_one_element(chamber_int, elem_idx: int, jet_input: str):
    drop_one_element.calls += 1
    if (chamber_int, elem_idx, jet_input) in drop_one_element.cache:
        return drop_one_element.cache[(chamber_int, elem_idx, jet_input)]
    no_rows = len(format(chamber_int, 'b')) // 7
    chamber = [(chamber_int >> (7 * idx)) & FULL_ROW for idx in range(no_rows)]
    elem = ELEMENTS[elem_idx]
    chamber = [EMPTY_ROW for _ in range(len(elem)+3)] + chamber
    drop = 0
    jet_idx = 0
    # Simulate element motion
    while True:
        # print_chamber(chamber, elem, drop)
        # first, simulate jet push
        jet_push = jet_input[jet_idx]
        jet_idx += 1
        # print('jet_push:', jet_push, '\n')
        if jet_push == '<':
            # if not wall-hit
            if not any([64 & el_row for el_row in elem]): # wall-hit
                if not any([(elem[idx] << 1) & chamber[idx + drop] for idx in range(len(elem))]): # elem-hit
                    elem = [el << 1 for el in elem]    
            # wall_hit = any([int('1000000', 2) & el_row for el_row in elem])
            # elem_hit = any([(elem[idx] << 1) & chamber[idx + drop] for idx in range(len(elem))])
            # if not (elem_hit or wall_hit):
            #     elem = [el << 1 for el in elem]
        else:
            if not any([1 & el_row for el_row in elem]): # wall-hit
                if not any([(elem[idx] >> 1) & chamber[idx + drop] for idx in range(len(elem))]): # elem-hit

                    elem = [el >> 1 for el in elem]
            # wall_hit = any([int('0000001', 2) & el_row for el_row in elem])
            # elem_hit = any([(elem[idx] >> 1) & chamber[idx + drop] for idx in range(len(elem))])
            # if not (elem_hit or wall_hit):
            #     elem = [el >> 1 for el in elem]
        
        # second, simulate downword motion
        # print('drop down: V\n')
        down_hit = any([elem[idx] & chamber[idx + drop + 1] for idx in range(len(elem))])
        if any([elem[idx] & chamber[idx + drop + 1] for idx in range(len(elem))]):
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
    drop_one_element.cache[(chamber_int, elem_idx, jet_input)] = (chamber, jet_idx)
    return (chamber, jet_idx)
drop_one_element.cache = {}
drop_one_element.calls = 0

def reduce_chamber(chamber: int) -> tuple:
    # Add one empty row on top of the chamber
    new_chamber = [FULL_ROW for _ in range(len(chamber))]
    stack = {(0, ~chamber[0] & (int('0000001', 2) << idx)) for idx in range(7)}
    while stack:
        row, col = stack.pop()
        new_chamber[row] -= col
        # To add a cell to the stack, it must:
        #  - not be out of bounds
        #  - be empty on the original chamber
        #  - be filled on the new chamber
        # It will then be cleared in new_chamber in a future loop
        for (dr, dc) in ((0, 1), (0, -1), (1, 0)):
            rr, cc = row + dr, col << dc if dc >0 else col >> -dc
            if not (rr > len(chamber) - 1 or cc == 0 or cc == 1 << 7):
                if ~chamber[rr] & cc:
                    if new_chamber[rr] & cc:
                        stack.add((rr, cc))
    dropped = 0
    while len(new_chamber) >= 2 and new_chamber[-2] == FULL_ROW:
        new_chamber.pop()
        dropped += 1

    return (new_chamber, dropped)
        

@print_function(run_time = True)
def solve_1(input: str, no_elements: int, log_end: bool = False, log_partial: bool = False) -> int:
    chamber = [FULL_ROW]
    double_input = input * 2
    jet_idx = 0
    total_dropped = 0
    for elem_idx in range(no_elements):
        chamber, jet_increment = drop_one_element(
            sum([line << 7 * idx for idx, line in enumerate(chamber)]),
            # chamber, 
            elem_idx % len(ELEMENTS), 
            double_input[jet_idx:jet_idx+33]
        )
        chamber, dropped_increment = reduce_chamber(chamber)
        total_dropped += dropped_increment
        jet_idx = (jet_idx + jet_increment) % len(input)
    if log_end:
        print_chamber(chamber)
    # print('total_dropped', total_dropped, 'len(chamber)', len(chamber))
    return len(chamber) - 1 + total_dropped

        



input = sys.stdin.read().strip()

# solve_1(input, 1, True)


print('Part 1:', solve_1(input, 2022, False))
print('calls:', drop_one_element.calls, 'cached:', len(drop_one_element.cache))
print('Part 1:', solve_1(input, 2022, False))
print('calls:', drop_one_element.calls, 'cached:', len(drop_one_element.cache))

# 1_000_000_000_000
for idx in [1_000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000, 1_000_000, 10_000_000, 100_000_000, 1_000_000_000, 10_000_000_000, 100_000_000_000, 1_000_000_000, 10_000_000_000, 100_000_000_000, 1_000_000_000_000]:
    solve_1(input, idx, False)
    print('calls:', drop_one_element.calls, 'cached:', len(drop_one_element.cache))
