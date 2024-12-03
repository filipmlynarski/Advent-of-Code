from utils import *

sys.dont_write_bytecode = True

current_day = __file__.split('/')[-1].split('.')[0]
puzzle = open(f'puzzle/{current_day}.in').read()

lines = puzzle.splitlines()

cords_of_all_numbers = set()
part_2 = 0
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if not char.isdecimal() and char != '.':
            new_numbers_cords = set()
            for cord, val in get_neighbours_with_cords(lines, y, x, OCT_DELTA).items():
                if val.isdecimal():
                    number_cords = {cord}
                    candidates = [cord]
                    while candidates:
                        candidate = candidates.pop()
                        left_right = get_neighbours_with_cords(lines, *candidate, [(0, -1), (0, 1)])
                        for sub_cord, sub_val in left_right.items():
                            if sub_cord in number_cords:
                                continue
                            if sub_val.isdecimal():
                                number_cords.add(sub_cord)
                                candidates.append(sub_cord)
                    new_numbers_cords.add(frozenset(number_cords))
            cords_of_all_numbers = cords_of_all_numbers.union(new_numbers_cords)

            if char == '*' and len(new_numbers_cords) == 2:
                temp = 1
                for cords in new_numbers_cords:
                    temp *= int("".join(lines[cord[0]][cord[1]] for cord in sorted(cords)))
                part_2 += temp


part_1 = 0
for cords in cords_of_all_numbers:
    part_1 += int("".join(lines[cord[0]][cord[1]] for cord in sorted(cords)))
time_print(part_1)
time_print(part_2)
