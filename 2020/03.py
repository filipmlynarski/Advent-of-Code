puzzle = open('puzzle/03.in').read().splitlines()


def count_trees(x_delta, y_delta):
    trees = 0
    x, y = 0, 0
    while y < len(puzzle):
        trees += puzzle[y][x] == '#'
        x = (x + x_delta) % len(puzzle[0])
        y += y_delta
    return trees


print(count_trees(3, 1))

slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
part_2 = count_trees(*slopes.pop(0))
for slope in slopes:
    part_2 *= count_trees(*slope)
print(part_2)
