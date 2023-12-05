from itertools import cycle

from utils import *

sys.dont_write_bytecode = True

current_day = __file__.split('/')[-1].split('.')[0]
puzzle = open(f'puzzle/{current_day}.in').read()
jet_pattern = cycle(enumerate(puzzle))

raw_rocks = '''\
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
'''
rocks = []
for raw_rock in raw_rocks.split('\n\n'):
    rocks.append([])
    for line in raw_rock.splitlines():
        rocks[-1].append(list(line))
rocks_cycle = cycle(enumerate(rocks))

grid: dict[tuple[int, int], str] = defaultdict(lambda: '.')


# def print_grid_with_rock(_rock, y, x, show_rock=True) -> None:
#     temp_grid = deepcopy(grid)
#     if show_rock:
#         for delta_y, _line in enumerate(_rock):
#             for delta_x, val in enumerate(_line):
#                 if val == '#':
#                     temp_grid[y-delta_y, x+delta_x] = '@'
#
#     max_y = max(map(fst, temp_grid)) + 3
#     max_x = 7
#     for y in range(max_y):
#         print('|', end='')
#         for x in range(max_x):
#             print(temp_grid.get((max_y-y-1, x), '.'), end='')
#         print('|')
#     print('+' + '-' * 7 + '+')
#     print()


def collides(_rock, y, x):
    for dy, _line in enumerate(_rock):
        for dx, char in enumerate(_line):
            if char == '#':
                _y, _x = y-dy, x+dx
                if _x < 0 or _x > 6:
                    return True
                if _y < 0:
                    return True
                if grid[(_y, _x)] != '.':
                    return True
    return False


def top_rows(max_y, depth=30) -> tuple:
    if not grid:
        return ()
    ret = []
    for y in range(max_y-depth, max_y):
        ret.append([])
        for x in range(7):
            ret[-1].append(grid[(y, x)])
    return tuple(tuple(row) for row in ret)


part_1, part_2 = None, None
step = -1
seen = {}
extra_height = None
current_y = -1
while part_1 is None or part_2 is None:
    step += 1

    rock_idx, rock = next(rocks_cycle)
    rock_y = current_y + 3 + len(rock)
    rock_x = 2

    first = True
    while True:
        jet_idx, jet = next(jet_pattern)
        if first and not extra_height:
            key = rock_idx, jet_idx, top_rows(current_y)
            if key in seen and part_1 is not None:
                seen_step, seen_height = seen[key]
                cycle_size = step - seen_step
                height = (current_y + 1) - seen_height
                n = (1000000000000 - cycle_size - step) // cycle_size
                step += cycle_size * n
                extra_height = height * n
            seen[key] = step, current_y + 1

        x_delta = 1 if jet == '>' else -1
        if not collides(rock, rock_y, rock_x + x_delta):
            rock_x += x_delta
        if collides(rock, rock_y-1, rock_x):
            break
        rock_y -= 1

    for delta_y, line in enumerate(rock):
        for delta_x, val in enumerate(line):
            if val == '#':
                new_y, new_x = rock_y-delta_y, rock_x+delta_x
                grid[(new_y, new_x)] = '#'
                current_y = max(current_y, new_y)

    if step == 2022-1:
        part_1 = current_y + 1
        time_print(part_1)
    elif step == 1000000000000-1:
        part_2 = current_y + 1 + extra_height
        time_print(part_2)
