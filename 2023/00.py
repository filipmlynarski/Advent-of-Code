from utils import *

sys.dont_write_bytecode = True

current_day = __file__.split('/')[-1].split('.')[0]
puzzle = open(f'puzzle/{current_day}.in').read()

lines = puzzle.splitlines()
ints = get_ints(puzzle)
words = get_words(puzzle)

ans = 0
for line in lines:
    pass

print(ans)
