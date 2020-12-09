from itertools import combinations

puzzle = list(map(int, open('puzzle/09.in').read().splitlines()))
part_1 = part_2 = None
for idx in range(25, len(puzzle)):
    if not any(num_1 + num_2 == puzzle[idx]
               for num_1, num_2 in combinations(puzzle[idx-25: idx], 2)):
        part_1 = puzzle[idx]
        break
print(part_1)

for end_idx in range(2, len(puzzle)):
    for start_idx in range(end_idx-2):
        puzzle_slice = puzzle[start_idx: end_idx]
        slice_sum = sum(puzzle_slice)
        if slice_sum < part_1:
            break
        elif slice_sum == part_1:
            part_2 = min(puzzle_slice) + max(puzzle_slice)
    if part_2:
        break
print(part_2)
