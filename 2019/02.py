puzzle = list(map(int, open('puzzle/02.in').read().split(',')))


def run(noun, verb):
    _puzzle = puzzle.copy()
    _puzzle[1] = noun
    _puzzle[2] = verb
    for pointer in range(0, len(_puzzle), 4):
        opcode, *params = puzzle[pointer: pointer+4]
        if opcode == 99:
            return _puzzle[0]
        elif opcode == 1:
            _puzzle[params[2]] = _puzzle[params[0]] + _puzzle[params[1]]
        else:
            _puzzle[params[2]] = _puzzle[params[0]] * _puzzle[params[1]]

    return _puzzle[0]


print(run(12, 2))
print(next(100 * noun + verb
           for noun in range(100)
           for verb in range(100)
           if run(noun, verb) == 19690720))
