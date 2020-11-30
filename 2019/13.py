from collections import defaultdict

puzzle = list(map(int, open('puzzle/13.in').read().split(',')))


def run(get_inp):

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


def get_move():
    if cords['paddle'][0] < cords['ball'][0]:
        return 1
    elif cords['paddle'][0] > cords['ball'][0]:
        return -1
    return 0


def play(board=None):
    if board is None:
        board = dict()
    program = run(get_move)

    while True:
        try:
            cord = (next(program), next(program))
            tile_id = next(program)
        except StopIteration:
            return board

        if cord == (-1, 0):
            if not any(tile_id == 2 for tile_id in board.values()):
                return tile_id
        else:
            board[cord] = tile_id
            if tile_id == 3:
                cords['paddle'] = cord
            elif tile_id == 4:
                cords['ball'] = cord


cords = {'ball': (0, 0), 'paddle': (0, 0)}
game_board = play()
print(list(game_board.values()).count(2))

puzzle[0] = 2  # insert coin
final_score = play(game_board)
print(final_score)
