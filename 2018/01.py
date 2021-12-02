import sys
sys.dont_write_bytecode = True
from utils import *


puzzle = open('puzzle/01.in').read()
frequencies = ints(puzzle)
print(sum(frequencies))

freq = 0
seen = {freq}
part_2 = None
while not part_2:
    for diff in frequencies:
        freq += diff
        if freq in seen:
            part_2 = freq
            break
        seen.add(freq)
print(part_2)
