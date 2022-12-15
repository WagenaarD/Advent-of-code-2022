"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 4737443 (ex 26)
Part 2  - 11482462818989 (ex 56000011) (18s)
Cleanup - 
"""


import sys
import re
sys.path.insert(0, '/'.join(__file__.replace('\\', '/').split('/')[:-2]))
from _utils.print_function import print_function

def all_numbers(s): return [int(d) for d in re.findall("(-?\d+)", s)]
def md(p, q): return abs(p[0]-q[0])+abs(p[1]-q[1])

@print_function(run_time = True)
def solve():
    input_data = sys.stdin.read().strip()
    data = [all_numbers(line) for line in input_data.split("\n")]
    radius = {(a,b):md((a,b),(c,d)) for (a,b,c,d) in data}
    scanners = radius.keys()

    acoeffs, bcoeffs = [], []
    for ((x,y), r) in radius.items():
        acoeffs.append(y-x+r+1)
        acoeffs.append(y-x-r-1)
        bcoeffs.append(x+y+r+1)
        bcoeffs.append(x+y-r-1)
    acoeffs = {a for a in acoeffs if acoeffs.count(a) >= 2}
    bcoeffs = {b for b in bcoeffs if bcoeffs.count(b) >= 2}

    bound = 4_000_000 if input_data.count('\n') != 13 else 20
    for a in acoeffs:
        for b in bcoeffs:
            p = ((b-a)//2, (a+b)//2)
            if all(0<c<bound for c in p):
                if all(md(p,t)>radius[t] for t in scanners):
                    print(4_000_000*p[0]+p[1])

solve()
