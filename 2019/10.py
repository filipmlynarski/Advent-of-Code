import sys
sys.dont_write_bytecode = True
from utils import *
from math import atan2, pi

puzzle = open('puzzle/10.in').read().splitlines()
raw_asteroids = {(x, y)
                 for y in range(len(puzzle))
                 for x in range(len(puzzle[y]))
                 if puzzle[y][x] == '#'}


def scan(cord):
    result = defaultdict(list)
    for asteroid in raw_asteroids - {cord}:
        delta_x = asteroid[0] - cord[0]
        delta_y = cord[1] - asteroid[1]
        # clockwise angle from y axis in radians
        radians = (-atan2(delta_y, delta_x) + pi/2) % (2*pi)
        # no need to calculate euclidean distance
        dist = abs(delta_y) + abs(delta_x)
        result[radians].append((asteroid, dist))

    return cord, result


best_cord, results = max(map(scan, raw_asteroids), key=lambda x: len(x[1]))
time_print(len(results))

# get asteroids sorted by distance from laser and grouped by clockwise angles
grouped_asteroids = [sorted_asteroids for _, sorted_asteroids in sorted(
    (angle, [asteroid for asteroid, _ in sorted(asteroids, key=lambda x: x[1])])
    for angle, asteroids in results.items()
)]
to_vaporize = 200 - 1
while to_vaporize != 0:
    for asteroids in filter(None, grouped_asteroids):
        if to_vaporize == 0:
            time_print(asteroids[0][0] * 100 + asteroids[0][1])
            break
        asteroids.pop(0)
        to_vaporize -= 1
