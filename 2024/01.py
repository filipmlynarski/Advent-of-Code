from utils import *

sys.dont_write_bytecode = True

current_day = __file__.split('/')[-1].split('.')[0]
puzzle = open(f'puzzle/{current_day}.in').read()

lines = puzzle.splitlines()
ints = get_ints(puzzle)
words = get_words(puzzle)

part_1 = 0
list_a, list_b = [], []
for line in lines:
    a, b = map(int, line.split())
    list_a.append(a)
    list_b.append(b)
part_2 = 0
for a, b in zip(sorted(list_a), sorted(list_b)):
    part_1 += abs(b-a)
    part_2 += a * list_b.count(a)

time_print(part_1)
time_print(part_2)
