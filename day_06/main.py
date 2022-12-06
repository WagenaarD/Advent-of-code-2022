"""
Advent of code challenge 2022
Start  17:37
Part 1 17:39 - 1480
Part 2 17:44 - 2746
"""


input = open('input.txt').read()
for idx in range(len(input)):
    if len(set(input[idx:idx+14])) == 14:
        break
print(idx + 14)