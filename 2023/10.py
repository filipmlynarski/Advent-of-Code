from utils import *

sys.dont_write_bytecode = True

current_day = __file__.split('/')[-1].split('.')[0]
puzzle = open(f'puzzle/{current_day}.in').read()

lines = puzzle.splitlines()

start = None
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == 'S':
            start = y, x

pipe_to_delta = {
    "|": ((-1, 0), (1, 0)),
    "-": ((0, -1), (0, 1)),
    "L": ((-1, 0), (0, 1)),
    "J": ((-1, 0), (0, -1)),
    "7": ((1, 0), (0, -1)),
    "F": ((1, 0), (0, 1)),
}
pipe_to_delta["S"] = pipe_to_delta["|"]

path = [start]
seen = {start}
while True:
    val = lines[path[-1][0]][path[-1][1]]
    for cord, _ in get_neighbours_with_cords(lines, *path[-1], pipe_to_delta[val]).items():
        if cord in seen:
            continue
        seen.add(cord)
        path.append(cord)
        break
    else:
        break
assert len(path) // 2 == 6714
print(len(path) // 2)


def is_point_inside_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False

    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]

        # Check if the ray crosses the edge
        if min(y1, y2) < y <= max(y1, y2):
            # Compute the x-intersection
            x_intersection = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x_intersection > x:
                inside = not inside  # Toggle the inside flag

    return inside


part_2 = 0
dot_fields = set()
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        cord = y, x
        if cord not in seen:
            part_2 += is_point_inside_polygon(cord, path)
print(part_2)
assert part_2 == 429
