from itertools import permutations

puzzle = list(map(int, open('puzzle/07.in').read().split(',')))


def run(inp, _puzzle=None, pointer=0, part=1):
    output = None
    if _puzzle is None:
        _puzzle = puzzle.copy()

    while True:
        mode_2, mode_1, *opcode = f'{_puzzle[pointer]:0>4}'
        opcode = ''.join(opcode)
        if opcode == '99':
            return output if part == 1 else None

        param_1 = _puzzle[pointer + 1]  # immediate mode
        if opcode in {'01', '02'}:
            if mode_1 == '0':
                param_1 = _puzzle[param_1]  # position mode
            param_2 = (
                _puzzle[pointer + 2]  # immediate mode
                if mode_2 == '1' else
                _puzzle[_puzzle[pointer + 2]]  # position mode
            )
            param_3 = _puzzle[pointer + 3]
            _puzzle[param_3] = (
                param_1 + param_2
                if opcode == '01' else
                param_1 * param_2
            )
            pointer += 4

        elif opcode == '03':
            _puzzle[param_1] = inp.pop() if inp else 0
            pointer += 2
        elif opcode == '04':
            output = _puzzle[param_1]
            pointer += 2
            if part == 2:
                return output, _puzzle, pointer

        else:
            if mode_1 == '0':
                param_1 = _puzzle[param_1]  # position mode
            param_2 = (
                _puzzle[pointer + 2]  # immediate mode
                if mode_2 == '1' else
                _puzzle[_puzzle[pointer + 2]]  # position mode
            )

            if opcode == '05':
                if param_1:
                    pointer = param_2
                else:
                    pointer += 3
            elif opcode == '06':
                if not param_1:
                    pointer = param_2
                else:
                    pointer += 3

            elif opcode in {'07', '08'}:
                param_3 = _puzzle[pointer + 3]
                _puzzle[param_3] = (
                    int(param_1 < param_2)
                    if opcode == '07' else
                    int(param_1 == param_2)
                )
                pointer += 4


def check(combination, part=1):
    out = 0
    if part == 1:
        for comb in combination:
            out = run([out, comb])
        return out

    puzzle_list = []
    pointer_list = []
    for comb in combination:
        out, _puzzle, pointer = run([out, comb], part=2)
        puzzle_list.append(_puzzle)
        pointer_list.append(pointer)

    while True:
        amp_e = out
        for idx in range(len(puzzle_list)):
            result = run([out], puzzle_list[idx], pointer_list[idx], part=2)
            if result is None:
                return amp_e
            out, _puzzle, pointer = result
            puzzle_list[idx] = _puzzle
            pointer_list[idx] = pointer


perms = (map(int, perm) for perm in permutations(map(str, range(10)), 5))
print(max(map(check, perms)))

perms = (map(int, perm) for perm in permutations(map(str, range(5, 10))))
print(max(check(perm, part=2) for perm in perms))
