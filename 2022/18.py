from utils import *

sys.dont_write_bytecode = True

current_day = __file__.split('/')[-1].split('.')[0]
puzzle = open(f'puzzle/{current_day}.in').read()

grid = {}  # cord: [0 -> outside air, 1 -> lava, 2 -> inside air]
for line in puzzle.splitlines():
    grid[tuple(get_ints(line))] = 1
min_x, max_x = min_max(lmap(fst, grid))
min_y, max_y = min_max(lmap(snd, grid))
min_z, max_z = min_max(lmap(trd, grid))

deltas = [[-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, 1], [0, 0, -1]]
part_1 = 0
for cord in grid:
    part_1 += sum(1 for i in get_dict_neighbours(grid, cord, deltas, fill=0).values() if i == 0)
time_print(part_1)


def get_air_cords(candidate) -> set | bool:
    x, y, z = candidate
    if x in {min_x-1, max_x+1}:
        return False
    if y in {min_y-1, max_y+1}:
        return False
    if z in {min_z-1, max_z+1}:
        return False

    if grid.get(candidate, 0) != 0 or candidate in seen:
        return set()
    seen.add(candidate)

    ret = {candidate}
    for sub_cord in get_dict_neighbours(grid, candidate, deltas, fill=0):
        sub_air_cords = get_air_cords(sub_cord)
        if sub_air_cords is False:
            return False
        ret |= sub_air_cords
    return ret


for cord, val in list(grid.items()):
    if val != 1:
        continue
    for neigh_cord, neigh_val in get_dict_neighbours(grid, cord, deltas, fill=0).items():
        if neigh_val == 0:
            seen = set()
            _air_cords = get_air_cords(neigh_cord)
            if _air_cords:
                for _air_cord in _air_cords:
                    grid[_air_cord] = 2

part_2 = 0
for cord, value in grid.items():
    if value == 1:
        part_2 += sum(
            1
            for sub_cord, val in get_dict_neighbours(grid, cord, deltas, fill=0).items()
            if val == 0  # wall with outside air
        )
time_print(part_2)
