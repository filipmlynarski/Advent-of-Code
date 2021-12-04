import sys
sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/02.in').readlines()
part_1 = part_2 = 0
for range_, (letter, _), passwd in map(str.split, puzzle):
    low, high = map(int, range_.split('-'))
    part_1 += low <= sum(char == letter for char in passwd) <= high
    part_2 += (passwd[low - 1] == letter) ^ (passwd[high - 1] == letter)
time_print(part_1)
time_print(part_2)
