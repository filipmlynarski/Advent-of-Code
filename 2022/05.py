import sys

sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/05.in').read()

raw_stacks, instructions = puzzle.split('\n\n')
*raw_stacks, indexes = raw_stacks.splitlines()
stacks_1 = {}
for line in raw_stacks:
    for idx, char in zip(indexes, line):
        if idx != ' ' and char != ' ':
            idx = int(idx)
            if idx not in stacks_1:
                stacks_1[idx] = []
            stacks_1[idx].insert(0, char)
stacks_2 = deepcopy(stacks_1)

for instruction in instructions.splitlines():
    n, fr, to = get_ints(instruction)
    stacks_1[to].extend(reversed(stacks_1[fr][-n:]))
    del stacks_1[fr][-n:]
    stacks_2[to].extend(stacks_2[fr][-n:])
    del stacks_2[fr][-n:]

time_print(''.join(v[-1] for _, v in sorted(stacks_1.items()) if v))
time_print(''.join(v[-1] for _, v in sorted(stacks_2.items()) if v))
