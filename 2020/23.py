puzzle = (list(map(int, list(open('puzzle/23.in').read()))) +
          list(range(10, 31)))
sorted_ = list(sorted(puzzle))
linked_cups = dict(zip(sorted_, [sorted_[-1]] + sorted_[:-1]))

for idx_ in range(30):
    current_cup = puzzle.pop(0)
    stack, rest = puzzle[:3], puzzle[3:]
    next_cup = linked_cups[current_cup]
    while next_cup in stack:
        next_cup = linked_cups[next_cup]
    idx = rest.index(next_cup)
    puzzle = [*rest[:idx], next_cup, *stack, *rest[idx+1:], current_cup]
    print(','.join(map(str, puzzle[-(idx_ + 1):] + puzzle[:-(idx_ + 1)])))

one_idx = puzzle.index(1)
# print(*puzzle[one_idx+1:] + puzzle[:one_idx], sep='')
