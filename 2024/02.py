from utils import *

sys.dont_write_bytecode = True

current_day = __file__.split('/')[-1].split('.')[0]
puzzle = open(f'puzzle/{current_day}.in').read()

lines = puzzle.splitlines()


def is_ok(values: list[int]) -> bool:
    all_increasing = True
    all_decreasing = True
    for left, right in zip(values[:-1], values[1:]):
        diff = right - left
        if diff > 0:
            all_increasing = False
        elif diff < 0:
            all_decreasing = False
        if all_increasing is False and all_decreasing is False:
            return False
        if not (1 <= abs(diff) <= 3):
            return False
    return True


part_1 = 0
part_2 = 0
for line in lines:
    diffs = []
    ints = get_ints(line)
    if is_ok(ints):
        part_1 += 1
        part_2 += 1
    else:
        for idx1 in range(len(ints)):
            new_ints = [val for idx2, val in enumerate(ints) if idx1 != idx2]
            if is_ok(new_ints):
                part_2 += 1
                break


time_print(part_1)
time_print(part_2)
