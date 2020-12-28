from collections import defaultdict

puzzle = list(map(int, open('puzzle/21.in').read().split(',')))


def run(get_inp=None, puzzle_=None, pointer=0, base=0):
    if puzzle_ is None:
        puzzle_ = defaultdict(int, dict(enumerate(puzzle)))

    def get_param(offset, mode, writes=False):
        ret = None
        if mode == '0':
            ret = puzzle_[pointer + offset]  # position mode
        elif mode == '1':
            ret = pointer + offset  # immediate mode
        elif mode == '2':
            ret = base + puzzle_[pointer + offset]  # relative mode
        return ret if writes else puzzle_[ret]

    while True:
        mode_3, mode_2, mode_1, *opcode = f'{puzzle_[pointer]:0>5}'
        opcode = int(''.join(opcode))
        if opcode == 99:
            return

        reads_1 = get_param(1, mode_1)
        reads_2 = get_param(2, mode_2)
        writes_1 = get_param(1, mode_1, writes=True)
        writes_3 = get_param(3, mode_3, writes=True)
        pointer += [4, 4, 2, 2, 3, 3, 4, 4, 2][opcode-1]

        if opcode == 1:
            puzzle_[writes_3] = reads_1 + reads_2
        elif opcode == 2:
            puzzle_[writes_3] = reads_1 * reads_2
        elif opcode == 3:
            puzzle_[writes_1] = get_inp()
        elif opcode == 4:
            yield reads_1
        elif opcode == 5:
            if reads_1:
                pointer = reads_2
        elif opcode == 6:
            if not reads_1:
                pointer = reads_2
        elif opcode == 7:
            puzzle_[writes_3] = int(reads_1 < reads_2)
        elif opcode == 8:
            puzzle_[writes_3] = int(reads_1 == reads_2)
        elif opcode == 9:
            base += reads_1


input_ = '''\
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
'''
print(list(run(map(ord, input_).__next__))[-1])

input_ = '''\
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
NOT E T
AND H T
OR E T
AND T J
RUN
'''
print(list(run(map(ord, input_).__next__))[-1])
