import sys
sys.dont_write_bytecode = True
from utils import *

puzzle = list(map(int, open('puzzle/15.in').read().split(',')))


def run(move, puzzle_=None, pointer=0, base=0):
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
            puzzle_[writes_1] = move
        elif opcode == 4:
            return reads_1, puzzle_, pointer, base
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


def bfs(programs, steps=0, part=1):
    programs_ = []
    for program, (x, y) in programs:
        status, puzzle_, pointer, base = program
        board[(x, y)] = status
        if status == 1:
            for move2_id, (x_delta, y_delta) in moves:
                new_x, new_y = x + x_delta, y + y_delta
                if (new_x, new_y) in board:
                    continue
                programs_.append((
                    run(move2_id, puzzle_.copy(), pointer, base),
                    (new_x, new_y),
                ))
        elif status == 2 and part == 1:
            return steps, (program, (x, y))  # part 1
    if not programs_:
        return steps  # part 2
    return bfs(programs_, steps + 1)


moves = list(enumerate([(0, 1), (0, -1), (-1, 0), (1, 0)], 1))
board = {(0, 0): 1}
depth, droid = bfs([(run(move_id), cord) for move_id, cord in moves], steps=1)
time_print(depth)

board.clear()  # clear board and set oxygen location to traversable location
time_print(bfs([((1, *droid[0][1:]), droid[1])], part=2))
