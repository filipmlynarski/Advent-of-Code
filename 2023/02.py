from utils import *

sys.dont_write_bytecode = True

current_day = __file__.split('/')[-1].split('.')[0]
puzzle = open(f'puzzle/{current_day}.in').read()

bag = {'red': 12, 'green': 13, 'blue': 14}
part_1, part_2 = 0, 0
for line in puzzle.splitlines():
    game_id = int(line.split()[1][:-1])
    max_colors = {'red': 0, 'green': 0, 'blue': 0}
    game_possible = True
    for cubes_set in line.split(': ')[1].split('; '):
        for val in cubes_set.split(', '):
            amount, color = val.split()
            amount = int(amount)
            max_colors[color] = max(max_colors[color], amount)
            if bag[color] < amount:
                game_possible = False
    if game_possible:
        part_1 += game_id
    part_2 += max_colors['red'] * max_colors['green'] * max_colors['blue']

time_print(part_1)
time_print(part_2)
