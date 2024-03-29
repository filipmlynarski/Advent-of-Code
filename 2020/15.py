import sys
sys.dont_write_bytecode = True
from utils import *

def speak(length):
    spoken = {num: idx for idx, num in enumerate(puzzle[:-1])}
    said = puzzle[-1]
    for idx in range(len(puzzle) - 1, length - 1):
        new_said = idx - spoken.get(said, idx)
        spoken[said] = idx
        said = new_said
    return said


puzzle = list(map(int, open('puzzle/15.in').read().split(',')))
time_print(speak(2020))
time_print(speak(30000000))
