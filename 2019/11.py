import sys
sys.dont_write_bytecode = True
from utils import *

puzzle = list(map(int, open('puzzle/11.in').read().split(',')))


def run(inp):

    def get_param(offset, mode, writes=False):
        ret = None
        if mode == '0':
            ret = puzzle_[pointer + offset]  # position mode
        elif mode == '1':
            ret = pointer + offset  # immediate mode
        elif mode == '2':
            ret = base + puzzle_[pointer + offset]  # relative mode
        return ret if writes else puzzle_[ret]

    puzzle_ = defaultdict(int, dict(enumerate(puzzle)))
    pointer = 0
    base = 0
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
            puzzle_[writes_1] = inp.pop(0)
        elif opcode == 4:
            inp = yield reads_1
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


def paint(painting=None):
    directions = deque([(0, 1), (1, 0), (0, -1), (-1, 0)])
    cord = (0, 0)
    if painting is None:
        painting = dict()

    program = run([painting.get(cord)])
    color = next(program)

    while True:
        painting[cord] = color
        turn = program.send([painting.get(cord, 0)])
        directions.rotate(-turn * 2 + 1)
        cord = (cord[0] + directions[0][0],
                cord[1] + directions[0][1])
        try:
            color = program.send([painting.get(cord, 0)])
        except StopIteration:
            return painting


time_print(len(paint()))
result = paint({(0, 0): 1})
xs = [x for (x, _), color in result.items() if color]
ys = [y for (_, y), color in result.items() if color]
time_print()
for y in range(max(ys), min(ys)-1, -1):
    for x in range(min(xs), max(xs)+1):
        print([' ', '#'][result.get((x, y), 0)], end='')
    print()
