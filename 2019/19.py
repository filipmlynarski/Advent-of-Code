import sys
sys.dont_write_bytecode = True
from utils import *

puzzle = list(map(int, open('puzzle/19.in').read().split(',')))


def run(moves: tuple):
    puzzle_ = defaultdict(int, dict(enumerate(puzzle)))
    pointer = 0
    base = 0
    move_idx = 0

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
            puzzle_[writes_1] = moves[move_idx]
            move_idx += 1
        elif opcode == 4:
            return reads_1
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


min_x, max_x = 0, 0
ans = 0
for y in range(50):
    min_x_ = min_x
    while not run((min_x_, y)):
        min_x_ += 1
        if min_x_ == 50:
            break
    else:
        min_x = min_x_
        max_x = max(min_x, max_x)
        while run((max_x, y)):
            max_x += 1
        ans += max_x - min_x
ratio = min_x / max_x
time_print(ans)


def get_max_x(exact_y):
    lo_x = int(exact_y * ratio)
    hi_x = lo_x + exact_y
    mid_x = lo_x
    while run((hi_x, exact_y)) == 0 or run((hi_x + 1, exact_y)) == 1:
        mid_x = (lo_x + hi_x + 1) // 2
        if run((mid_x, exact_y)) == 1:
            lo_x = mid_x
        else:
            hi_x = mid_x - 1
    return mid_x


lo_y = edge = 100
while run((get_max_x(lo_y) - edge, lo_y + edge - 1)) == 0:
    lo_y += edge
lo_y -= edge
while run((get_max_x(lo_y) - edge, lo_y + edge - 1)) == 0:
    lo_y += edge // 10
y = lo_y - edge // 10
while run((get_max_x(y) - edge, y + edge - 1)) == 0:
    y += 1
time_print((get_max_x(y) - edge) * 10_000 + y)
