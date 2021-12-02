import sys
sys.dont_write_bytecode = True
from utils import *


def react(polymer):
    idx = 0
    while idx < len(polymer) - 1:
        char_1, char_2 = polymer[idx], polymer[idx + 1]
        if char_1.swapcase() == char_2:
            polymer.pop(idx)
            polymer.pop(idx)
            if idx > 0:
                idx -= 1
            continue
        idx += 1
    return polymer


puzzle = open('puzzle/05.in').read()
print(len(react(list(puzzle))))

best = None
for char_to_remove in set(puzzle.lower()):
    temp = [char for char in puzzle if char.lower() != char_to_remove]
    length = len(react(temp))
    best = min(length, best) if best else length
print(best)
