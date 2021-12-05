import sys
sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/24.in').read()
grid = tuple(tuple(line) for line in puzzle.splitlines())
seen = {hash(grid)}


@lru_cache(maxsize=None)
def adj(row_, col_):
    ret = []
    for row_delta, col_delta in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
        new_cord = row_ + row_delta, col_ + col_delta
        if new_cord[0] in range(5) and new_cord[1] in range(5):
            ret.append(new_cord)
    return ret


while True:
    new_grid = []
    for row in range(len(grid)):
        new_grid.append([])
        for col in range(len(grid[row])):
            alive = sum(
                grid[sub_row][sub_col] == '#'
                for sub_row, sub_col in adj(row, col)
            )
            if grid[row][col] == '.':
                new_grid[-1].append('#' if alive in {1, 2} else '.')
            else:
                new_grid[-1].append('#' if alive == 1 else '.')
    new_grid = tuple(tuple(line) for line in new_grid)
    new_hash = hash(new_grid)
    if new_hash in seen:
        flat = [value for line in new_grid for value in line]
        time_print(sum(2 ** idx for idx, value in enumerate(flat) if value == '#'))
        break
    seen.add(new_hash)
    grid = new_grid

# part 2
grid = defaultdict(lambda: defaultdict(lambda: '.'))
for row, line in enumerate(puzzle.splitlines(), -2):
    for col, character in enumerate(line, -2):
        grid[0][(row, col)] = character


def get_alive(grid_, level_, row_, col_):
    ret = 0
    for delta_row, delta_col in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
        new_row, new_col = row_ + delta_row, col_ + delta_col
        if new_row == -3:
            ret += grid_[level_ - 1][(-1, 0)] == '#'
        elif new_col == -3:
            ret += grid_[level_ - 1][(0, -1)] == '#'
        elif new_col == 3:
            ret += grid_[level_ - 1][(0, 1)] == '#'
        elif new_row == 3:
            ret += grid_[level_ - 1][(1, 0)] == '#'
        elif (new_row, new_col) == (0, 0):
            if row_ == -1:
                values = [grid_[level_ + 1][(-2, idx)] for idx in range(-2, 3)]
            elif col_ == -1:
                values = [grid_[level_ + 1][(idx, -2)] for idx in range(-2, 3)]
            elif col_ == 1:
                values = [grid_[level_ + 1][(idx, 2)] for idx in range(-2, 3)]
            elif row_ == 1:
                values = [grid_[level_ + 1][(2, idx)] for idx in range(-2, 3)]
            else:
                raise ValueError(row_, col_)
            ret += values.count('#')
        else:
            ret += grid_[level_][(new_row, new_col)] == '#'
    return ret


for _ in range(200):
    new_grid = defaultdict(lambda: defaultdict(lambda: '.'))
    extra = [
        (min(grid)-1, defaultdict(lambda: defaultdict(lambda: '.'))),
        (max(grid)+1, defaultdict(lambda: defaultdict(lambda: '.'))),
    ]
    for level, temp_grid in [*grid.items(), *extra]:
        for row, col in itertools.product(range(-2, 3), repeat=2):
            if (row, col) == (0, 0):
                continue
            alive = get_alive(grid, level, row, col)
            if grid[level][(row, col)] == '.':
                new_grid[level][(row, col)] = '#' if alive in {1, 2} else '.'
            else:
                new_grid[level][(row, col)] = '#' if alive == 1 else '.'
    grid = new_grid.copy()

time_print(sum(value == '#' for sub_grid in grid.values() for value in sub_grid.values()))
