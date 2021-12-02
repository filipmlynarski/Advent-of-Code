import sys
sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/02.in').read().splitlines()

horizontal, depth_1, depth_2, aim = 0, 0, 0, 0
for line in puzzle:
    value = int(line.split()[-1])
    if line.startswith('forward'):
        horizontal += value
        depth_2 += aim * value
    elif line.startswith('down'):
        depth_1 += value
        aim += value
    else:
        depth_1 -= value
        aim -= value

print(horizontal * depth_1)
print(horizontal * depth_2)
