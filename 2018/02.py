import sys
sys.dont_write_bytecode = True
from utils import *


puzzle = open('puzzle/02.in').read().splitlines()
two, three = 0, 0
for id_ in puzzle:
    counter = invert_dict(Counter(id_))
    two += 2 in counter
    three += 3 in counter
print(two * three)

for id_1, id_2 in itertools.combinations(puzzle, 2):
    result = ''.join(char_1 for char_1, char_2 in zip(id_1, id_2) if char_1 == char_2)
    if len(result) == len(id_1) - 1:
        print(result)
        break
