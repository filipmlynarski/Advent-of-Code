from utils import *

sys.dont_write_bytecode = True

current_day = __file__.split('/')[-1].split('.')[0]
puzzle = open(f'puzzle/{current_day}.in').read()

str_numbers = 'one, two, three, four, five, six, seven, eight, nine'.split(', ')
part_1, part_2 = 0, 0
for line in puzzle.splitlines():
    nums_p1, nums_p2 = [], []

    for idx, char in enumerate(line):
        if char.isdigit():
            nums_p1.append(char)
            nums_p2.append(char)
        else:
            for x_idx, x in enumerate(str_numbers):
                if line[idx: idx+len(x)] == x:
                    nums_p2.append(str(x_idx+1))
                    break

    part_1 += int(nums_p1[0] + nums_p1[-1])
    part_2 += int(nums_p2[0] + nums_p2[-1])

time_print(part_1)
time_print(part_2)
