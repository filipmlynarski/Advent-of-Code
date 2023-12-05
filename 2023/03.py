from utils import *

sys.dont_write_bytecode = True

current_day = __file__.split('/')[-1].split('.')[0]
puzzle = open(f'puzzle/{current_day}.in').read()

lines = puzzle.splitlines()
ints = get_ints(puzzle)
words = get_words(puzzle)

ans = 0
for y, line in enumerate(lines):
    x = 0
    while x < len(line):
        val = line[x]
        if val.isdecimal():
            total = val
            for idx in range(x+1, len(line)):
                if line[idx].isdecimal():
                    total += line[idx]
                else:
                    break
            good = False
            print('trying', total)
            for delta in range(len(total)+1):
                new_y, new_x = y, x + delta
                print(lines[new_y][x])
                print(f'{lines[new_y][new_x] = }')
                for neigh in get_neighbours(lines, new_y, new_x, GRID_DELTA):
                    print('neigh = ', neigh)
                    if not neigh.isdecimal() and neigh != '.':
                        good = True
            if good:
                print(total)
                ans += int(total)
            x = idx
        x += 1

print(ans)
