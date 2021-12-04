import sys
sys.dont_write_bytecode = True
from utils import *

lines = open('puzzle/03.in').read().splitlines()
width = len(lines[0])

common = [[0, 0] for _ in range(width)]
for line in lines:
    for idx, char in enumerate(line):
        common[idx][int(char)] += 1
gamma = int(''.join('0' if val[0] > val[1] else '1' for val in common), 2)
eps = int(''.join('1' if val[0] > val[1] else '0' for val in common), 2)
time_print(gamma * eps)

oxygen_candidates = lines.copy()
co2_candidates = lines.copy()
for idx in range(width):
    if len(oxygen_candidates) != 1:
        common = [0, 0]
        for line in oxygen_candidates:
            common[int(line[idx])] += 1
        bit = '1' if common[0] <= common[1] else '0'
        oxygen_candidates = [line for line in oxygen_candidates if line[idx] == bit]
    if len(co2_candidates) != 1:
        common = [0, 0]
        for line in co2_candidates:
            common[int(line[idx])] += 1
        bit = '0' if common[0] <= common[1] else '1'
        co2_candidates = [line for line in co2_candidates if line[idx] == bit]

oxygen = int(oxygen_candidates[0], 2)
co2 = int(co2_candidates[0], 2)
time_print(oxygen * co2)
