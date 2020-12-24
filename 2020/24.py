import re
from collections import defaultdict

directions = {'e': (2, 0), 'se': (1, -1), 'sw': (-1, -1),
              'w': (-2, 0), 'nw': (-1, 1), 'ne': (1, 1)}
lines = open('puzzle/24.in').read().splitlines()
lines = (re.findall('|'.join(directions), line) for line in lines)
grid = defaultdict(lambda: 1)
for line in lines:
    x, y = 0, 0
    for dir_ in line:
        x_delta, y_delta = directions[dir_]
        x += x_delta
        y += y_delta
    grid[(x, y)] = 0 if grid[(x, y)] == 1 else 1
print(len(grid) - sum(grid.values()))

for _ in range(100):
    min_x, *_, max_x = sorted(x for x, _ in grid)
    min_y, *_, max_y = sorted(y for _, y in grid)
    grid_ = grid.copy()
    for y in range(min_y - 1, max_y + 2):
        for x in range(min_x - 2, max_x + 4):
            adj = [0, 0]
            for x_delta, y_delta in directions.values():
                adj[grid[(x + x_delta, y + y_delta)]] += 1
            if grid[(x, y)] == 0 and (adj[0] == 0 or adj[0] > 2):
                grid_[(x, y)] = 1
            elif grid[(x, y)] == 1 and adj[0] == 2:
                grid_[(x, y)] = 0
    grid = grid_
print(len(grid) - sum(grid.values()))
