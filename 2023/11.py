from utils import *

sys.dont_write_bytecode = True

current_day = __file__.split('/')[-1].split('.')[0]
puzzle = open(f'puzzle/{current_day}.in').read()
lines = puzzle.splitlines()

empty_rows = []
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == '#':
            break
    else:
        empty_rows.append(y)

empty_columns = []
for x in range(len(lines[0])):
    for y in range(len(lines)):
        char = lines[y][x]
        if char == '#':
            break
    else:
        empty_columns.append(x)

galaxies = []
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == '#':
            galaxies.append((y, x))


def get_sum_of_shortest_distances(expand_by: int) -> int:
    total_distance = 0
    for (idx1, galaxy1), (idx2, galaxy2) in itertools.combinations(enumerate(galaxies, 1), 2):
        for y in range(min(galaxy1[0], galaxy2[0])+1, max(galaxy1[0], galaxy2[0])+1):
            if y in empty_rows:
                total_distance += expand_by
            else:
                total_distance += 1
        for x in range(min(galaxy1[1], galaxy2[1])+1, max(galaxy1[1], galaxy2[1])+1):
            if x in empty_columns:
                total_distance += expand_by
            else:
                total_distance += 1
    return total_distance


time_print(get_sum_of_shortest_distances(2))
time_print(get_sum_of_shortest_distances(1_000_000))
