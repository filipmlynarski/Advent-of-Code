puzzle = list(map(int, open('puzzle/01.in').readlines()))
print(next(num_1 * num_2 for idx_1, num_1 in enumerate(puzzle)
           for num_2 in puzzle[idx_1 + 1:] if num_1 + num_2 == 2020))
print(next(
    num_1 * num_2 * num_3
    for idx_1, num_1 in enumerate(puzzle)
    for idx_2, num_2 in enumerate(puzzle[idx_1 + 1:])
    for num_3 in puzzle[idx_2 + 1:]
    if num_1 + num_2 + num_3 == 2020
))
