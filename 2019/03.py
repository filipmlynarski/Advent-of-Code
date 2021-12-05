import sys
sys.dont_write_bytecode = True
from utils import *

wires = open('puzzle/03.in').read().splitlines()

grid = {}
best_intersection = float('inf')
best_intersection_steps = float('inf')
move_mapping = {
    'U': (0, 1),
    'D': (0, -1),
    'R': (1, 0),
    'L': (-1, 0),
}

for nth_wire, wire in enumerate(wires):
    current_cord = (0, 0)
    steps = 0
    for i in wire.split(','):
        x, y = move_mapping[i[0]]
        n = int(i[1:])

        for _ in range(n):
            steps += 1
            current_cord = (current_cord[0] + x,
                            current_cord[1] + y)
            if nth_wire == 0:
                grid[current_cord] = grid.get(current_cord, steps)
            elif current_cord in grid:
                dist = sum(map(abs, current_cord))
                if dist < best_intersection:
                    best_intersection = dist
                if grid[current_cord] + steps < best_intersection_steps:
                    best_intersection_steps = grid[current_cord] + steps

time_print(best_intersection)
time_print(best_intersection_steps)
