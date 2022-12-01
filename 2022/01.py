import sys

sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/01.in').read()

calories = []
for elf_calories in puzzle.split('\n\n'):
    calories.append(sum(get_ints(elf_calories)))

calories.sort()
time_print(calories[-1])
time_print(sum(calories[-3:]))
