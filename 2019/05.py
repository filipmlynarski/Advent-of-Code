puzzle = list(map(int, open('puzzle/05.in').read().split(',')))


def run(inp, part):
    final_output = None
    _puzzle = puzzle.copy()

    pointer = 0
    while True:
        mode_2, mode_1, *opcode = f'{_puzzle[pointer]:0>4}'
        opcode = ''.join(opcode)
        param_1 = _puzzle[pointer + 1]  # immediate mode

        if opcode == '99':
            return final_output

        elif opcode in {'01', '02'}:
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
            _puzzle[param_1] = inp
            pointer += 2
        elif opcode == '04':
            final_output = _puzzle[param_1]
            pointer += 2

        elif part == 2:
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


print(run(1, part=1))
print(run(5, part=2))
