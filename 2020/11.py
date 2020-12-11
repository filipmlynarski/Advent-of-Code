from copy import deepcopy
from functools import lru_cache

puzzle = open('puzzle/11.in').read()
plane = list(map(list, puzzle.splitlines()))
deltas = [(temp_row, temp_col)
          for temp_row in range(-1, 2) for temp_col in range(-1, 2)
          if not temp_row == temp_col == 0]
seats_cords = [(row_idx, col_idx)
               for row_idx, row in enumerate(plane)
               for col_idx, seat in enumerate(row)
               if seat != '.']


def get_seats(get_adjacent, empty_rule):
    grid = deepcopy(plane)
    while True:
        grid_ = deepcopy(grid)
        for row, col in seats_cords:
            seat = grid[row][col]
            adjacent = get_adjacent(grid, row, col)
            if seat == 'L' and adjacent == 0:
                grid_[row][col] = '#'
            elif seat == '#' and adjacent >= empty_rule:
                grid_[row][col] = 'L'
        if grid_ == grid:
            return sum(seat == '#' for line in grid for seat in line)
        grid = grid_


def get_adjacent_1(grid, row, col):
    return sum(grid[row_][col_] == '#'
               for row_, col_ in get_neighbours(row, col))


@lru_cache(maxsize=len(plane) * len(plane[0]))
def get_neighbours(row, col):
    ret = []
    for row_delta, col_delta in deltas:
        row_, col_ = row + row_delta, col + col_delta
        if 0 <= row_ < len(plane) and 0 <= col_ < len(plane[0]):
            ret.append((row_, col_))
    return ret


def get_adjacent_2(grid, row, col):
    adj = 0
    for row_delta, col_delta in deltas:
        temp_row, temp_col = row + row_delta, col + col_delta
        while 0 <= temp_row < len(grid) and 0 <= temp_col < len(grid[0]):
            if grid[temp_row][temp_col] == 'L':
                break
            elif grid[temp_row][temp_col] == '#':
                adj += 1
                break
            temp_row += row_delta
            temp_col += col_delta
    return adj


print(get_seats(get_adjacent_1, 4))
print(get_seats(get_adjacent_2, 5))
