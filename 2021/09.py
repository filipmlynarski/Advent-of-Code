import sys
sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/09.in').read()
lines = puzzle.splitlines()
height, width = len(lines), len(lines[0])
grid = {(row, col): int(val) for row, line in enumerate(lines) for col, val in enumerate(line)}

ans = 0
for cord in itertools.product(range(height), range(width)):
    if all(grid[cord] < neigh for neigh in get_dict_neighbours(grid, cord).values()):
        ans += grid[cord] + 1
time_print(ans)

def get_basin(current_basin, seen_, prev=None):
    if prev is None:
        prev = {}
    ret = current_basin.copy()
    for cord_ in ret.keys() - prev.keys():
        neighbours = get_dict_neighbours(grid, cord_)
        for key in set(neighbours.keys()) - seen_:
            if neighbours[key] == 9:
                continue
            ret[key] = neighbours[key]
            seen_.add(key)
    if ret != current_basin:
        return get_basin(ret, seen_, current_basin)
    return ret


basins = []
seen = set()
for cord in itertools.product(range(height), range(width)):
    if cord not in seen and grid[cord] != 9:
        basin = get_basin({cord: grid[cord]}, seen)
        if len(basin) > 1:
            basins.append(basin)
time_print(reduce(lambda x, y: x * y, sorted(lmap(len, basins))[-3:]))
