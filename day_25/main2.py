"""
A 12 line solution. Possible by not converting to and from ints but staying in SNAFU format.
"""

import sys, collections
SNAFU_DIGIT_LUT = {'2': 2, '1': 1, '0': 0, '-': -1, '=':  -2}
DIGIT_SNAFU_LUT = {val: key for key, val in SNAFU_DIGIT_LUT.items()}
lines = sys.stdin.read().strip().split('\n')
digits = collections.defaultdict(int)
for line in lines:
    for idx, char in enumerate(line[::-1]):
        digits[idx] += SNAFU_DIGIT_LUT[char]
for idx in range(len(digits) - 1):
    digits[idx + 1] += (digits[idx] + 12) // 5 - 2
    digits[idx] = (digits[idx] + 2) % 5 - 2
print(''.join([DIGIT_SNAFU_LUT[digits[idx]] for idx in range(max(digits) + 1)][::-1]).lstrip('0'))