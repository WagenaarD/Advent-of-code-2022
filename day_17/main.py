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



def print_chamber():
    for idx, line in enumerate(chamber[::-1]):
        print('{:3} |{}|'.format(len(chamber)-idx-1 if (len(chamber)-idx-1) % 10 == 0 else '', line))
    print('    +{}+\n'.format('-' * 7))



input = sys.stdin.read().strip()

# chamber = ['.' * 7]
chamber = []
print_chamber()



# ####

# .#.
# ###
# .#.

# ..#
# ..#
# ###

# #
# #
# #
# #

# ##
# ##

ELEMENTS = (
    ['..####.'],
    ['...#...', '..###..', '...#...'],
    ['....#..', '....#..', '..###..',],
    ['..#....', '..#....', '..#....', '..#....'],
    ['..##...', '..##...',]
)


# itertools.repeat(ELEMENTS)
# for elem_idx in range(2022):
get_next_jet_push = it.repeat(input)
for elem_idx in range(2):
    elem = ELEMENTS[elem_idx % len(ELEMENTS)]
    chamber += ['.' * 7 for _ in range(3)]
    print_chamber()
    while True
        # first, simulate jet push
        jet_push = get_next_jet_push()
        
    
    print_chamber()
