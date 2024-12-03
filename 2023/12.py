from utils import *

sys.dont_write_bytecode = True

current_day = __file__.split('/')[-1].split('.')[0]
puzzle = open(f'puzzle/{current_day}.in').read()

lines = puzzle.splitlines()
ints = get_ints(puzzle)
words = get_words(puzzle)


def count(springs: list[str]) -> list[int]:
    ret = []
    streak = 0
    for idx, char in enumerate(springs):
        if char == '#':
            streak += 1
        else:
            if streak:
                ret.append(streak)
                streak = 0
    if streak:
        ret.append(streak)
    return ret

ans = 0
for line in lines:
    line, correct = line.split()
    correct = list(map(int, correct.split(',')))
    unknown = line.count('?')
    for char in itertools.product('.#', repeat=unknown):
        replacements = list(char)
        temp_line = [val if val != "?" else replacements.pop(0) for val in line]
        ans += count(temp_line) == correct

print(ans)
