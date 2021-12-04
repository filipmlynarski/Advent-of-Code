import sys
sys.dont_write_bytecode = True
from utils import *

from collections import deque

puzzle = open('puzzle/12.in').read()
lines = [(line[0], int(line[1:])) for line in puzzle.splitlines()]

y, x = 0, 0
directions = {'E': (0, 1), 'S': (-1, 0), 'W': (0, -1), 'N': (1, 0)}
current_dir = deque(directions.values())
for action, value in lines:
    if action == 'F':
        y += current_dir[0][0] * value
        x += current_dir[0][1] * value
    elif action in directions:
        y += directions[action][0] * value
        x += directions[action][1] * value
    elif action in {'L', 'R'}:
        current_dir.rotate({'L': 1, 'R': -1}[action] * (value // 90))
time_print(abs(y) + abs(x))

y, x = 0, 0
y_way, x_way = 1, 10
for action, value in lines:
    if action == 'F':
        y += y_way * value
        x += x_way * value
    elif action in directions:
        y_way += directions[action][0] * value
        x_way += directions[action][1] * value
    else:
        for _ in range(0, value, 90):
            y_way, x_way = (x_way, -y_way) if action == 'L' else (-x_way, y_way)
time_print(abs(y) + abs(x))
