import sys
sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/10.in').read()
lines = puzzle.splitlines()

part_1 = 0
part_2 = []
mapping = {'(': ')', '[': ']', '{': '}', '<': '>'}
weights_1 = {')': 3, ']': 57, '}': 1197, '>': 25137}
weights_2 = {'(': 1, '[': 2, '{': 3, '<': 4}
for line in lines:
    stack = []
    for char in line:
        if char in mapping:
            stack.append(char)
        else:
            if char != mapping[stack.pop(-1)]:
                part_1 += weights_1[char]
                break
    else:
        score = 0
        for val in stack[::-1]:
            score *= 5
            score += weights_2[val]
        part_2.append(score)
time_print(part_1)
time_print(sorted(part_2)[len(part_2)//2])
