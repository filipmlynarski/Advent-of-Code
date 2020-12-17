import sys
from collections import defaultdict
from functools import lru_cache
from itertools import product

sys.setrecursionlimit(5000)


def create_deltas(dims):
    return list(filter(any, product(range(-1, 2), repeat=dims)))


puzzle = open('puzzle/17.in').read().splitlines()
grid_3d = defaultdict(int)
grid_4d = defaultdict(int)
for y, line in enumerate(puzzle):
    for x, value in enumerate(line):
        grid_3d[(x, y, 0)] = [0, 1][value == '#']
        grid_4d[(x, y, 0, 0)] = [0, 1][value == '#']
deltas = {3: create_deltas(3), 4: create_deltas(4)}


@lru_cache(maxsize=None)
def get_neighbours(cord):
    ret = set()
    for cord_deltas in deltas[len(cord)]:
        new_cord = tuple(val + delta_ for val, delta_ in zip(cord, cord_deltas))
        ret.add(new_cord)
    return ret


def update(cord, grid, temp_grid, seen_):
    seen_.add(cord)
    neighbours = get_neighbours(cord)
    active_neighbours = sum(grid.get(cord_, 0) for cord_ in neighbours)
    if grid.get(cord) and active_neighbours not in {2, 3}:
        temp_grid[cord] = 0
    elif not grid.get(cord) and active_neighbours == 3:
        temp_grid[cord] = 1
    if grid.get(cord):
        for neighbour in neighbours - seen_:
            update(neighbour, grid, temp_grid, seen_)


def step(grid, cycles):
    for _ in range(cycles):
        new_grid = grid.copy()
        seen = set()
        for current_cord in grid:
            if current_cord not in seen:
                update(current_cord, grid, new_grid, seen)
        grid = new_grid
    return grid


print(sum(step(grid_3d, 6).values()))
print(sum(step(grid_4d, 6).values()))
