import sys
sys.dont_write_bytecode = True
from utils import *


puzzle = open('puzzle/06.in').read().splitlines()
points = [tuple(ints(line)) for line in puzzle]
min_y, max_y = min_max(lmap(fst, points))
min_x, max_x = min_max(lmap(snd, points))

y_range = range(min_y-100, max_y+101)
x_range = range(min_x-100, max_x+101)
grid = dict.fromkeys(cord for cord in itertools.product(y_range, x_range))
for cord in itertools.product(y_range, x_range):
    distances = defaultdict(list)
    for point in points:
        distances[pdist1(cord, point)].append(point)
    min_distance = min(distances)
    if len(distances[min_distance]) == 1:
        grid[cord] = distances[min_distance][0]
infinite = set.union(
    set(grid[(y, 0)] for y in y_range),
    set(grid[(y, max_x)] for y in y_range),
    set(grid[(0, x)] for x in x_range),
    set(grid[(max_y, x)] for x in x_range)
)
counter = Counter(val for val in grid.values() if val not in infinite)
print(*counter.items(), sep='\n')
