import sys
sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/03.in').read()
lines = puzzle.splitlines()


def get_value(char: str) -> int:
    if char.isupper():
        return ord(char) - ord('A') + 27
    return ord(char) - ord('a') + 1


part_1 = part_2 = 0
group = []
for idx, line in enumerate(lines):
    common = set(line[:len(line)//2]) & set(line[len(line)//2:])
    part_1 += sum(map(get_value, common))

    group.append(line)
    if len(group) == 3:
        common = set.intersection(*map(set, group))
        part_2 += sum(map(get_value, common))
        group = []

time_print(part_1)
time_print(part_2)
