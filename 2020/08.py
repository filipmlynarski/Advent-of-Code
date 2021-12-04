import sys
sys.dont_write_bytecode = True
from utils import *

def run(instructions):
    seen = set()
    pointer = 0
    accumulator = 0
    while True:
        if pointer >= len(instructions):
            return None, accumulator  # finishing
        seen.add(pointer)
        opcode, argument = instructions[pointer].split()
        if opcode == 'nop':
            pointer += 1
        elif opcode == 'acc':
            accumulator += int(argument)
            pointer += 1
        else:
            pointer += int(argument)
        if pointer in seen:
            return accumulator, None  # halting


puzzle = open('puzzle/08.in').read().splitlines()
time_print(run(puzzle)[0])

for line_idx, line in enumerate(puzzle):
    if line.startswith('acc'):
        continue
    puzzle_ = puzzle.copy()
    opcode, arg = line.split()
    puzzle_[line_idx] = {'jmp': 'nop', 'nop': 'jmp'}[opcode] + ' ' + arg
    _, finished = run(puzzle_)
    if finished:
        time_print(finished)
        break
