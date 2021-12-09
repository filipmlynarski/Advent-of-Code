import sys
sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/08.in').read()
lines = [[''.join(sorted(word)) for word in words(line)] for line in puzzle.splitlines()]
time_print(sum(len(val) in {2, 4, 3, 7} for line in lines for val in line[-4:]))

mapping = {
    0: set('abcefg'),
    1: set('cf'),
    2: set('acdeg'),
    3: set('acdfg'),
    4: set('bcdf'),
    5: set('abdfg'),
    6: set('abdefg'),
    7: set('acf'),
    8: set('abcdefg'),
    9: set('abcdfg'),
}
letters = mapping[8]
ans = 0
for items in lines:
    # mapping from destination letter to possible letter sources
    correct = {letter: letters.copy() for letter in letters}
    guess = defaultdict(list)
    for item in set(items):
        for key, value in mapping.items():
            if len(item) == len(value):
                guess[item].append(key)  # guess by length

    while guess:
        for key, values in sorted(guess.copy().items(), reverse=True):
            if len(values) == 1:
                value = guess.pop(key)[0]
                for on in mapping[value]:
                    correct[on] &= set(key)
                for off in letters - mapping[value]:
                    correct[off] -= set(key)
            else:
                new_values = []
                # mapping from possible sources to possible destinations
                correct_inv = invert_dict(correct, False, set)
                for value in values:
                    proper = mapping[value]
                    for sources, destinations in correct_inv.items():
                        if destinations.issubset(proper) and not sources.issubset(set(key)):
                            break
                    else:
                        new_values.append(value)
                guess[key] = new_values.copy()
    temp = ''
    correct = {next(iter(value)): key for key, value in correct.items()}
    for item in items[-4:]:
        mapped = set(correct[letter] for letter in item)
        temp += str(next(key for key, value in mapping.items() if value == mapped))
    ans += int(temp)
time_print(ans)
