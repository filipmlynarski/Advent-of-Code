import sys
sys.dont_write_bytecode = True
from utils import *
import typing as t

puzzle = list(map(int, open('puzzle/17.in').read().split(',')))


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


ways = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
turn_right = {('^', '>'), ('>', 'V'), ('V', '<'), ('<', '^')}
art = dict()
main_robot = None
row, col = 0, 0

for val in map(chr, run()):
    if val == '\n':
        row += 1
        col = -1
    elif val != '.':
        if val in ways:
            main_robot = (row, col), val
        art[(row, col)] = set()
        adjacent = [(row + row_delta, col + col_delta)
                    for row_delta, col_delta in ways.values()]
        for adj_cord in adjacent:
            if adj_cord in art:
                art[adj_cord].add((row, col))
                art[(row, col)].add(adj_cord)
    col += 1
time_print(sum(
    row * col for (row, col), neighbours in art.items() if len(neighbours) > 2
))


cord = t.Tuple[int, int]
intersections: t.Dict[cord, t.Set[cord]] = defaultdict(set)
last_cord: t.Optional[cord] = None
temp_robot = main_robot
while True:
    (y, x), way = temp_robot
    robot_neighbours = art[(y, x)]
    delta_y, delta_x = ways[way]
    next_cord = y + delta_y, x + delta_x
    if len(robot_neighbours) == 1:
        if intersections:
            intersections[last_cord].add((y, x))
            finish_cord = y, x
            break  # finish
        last_cord = (y, x)
        next_cord = next(iter(robot_neighbours))  # start
    elif next_cord in robot_neighbours:
        if len(robot_neighbours) > 2:
            intersections[last_cord].add((y, x))
            intersections[(y, x)].add(last_cord)
            last_cord = (y, x)
        temp_robot = next_cord, way
        continue
    else:
        previous_cord = (y - delta_y, x - delta_x)
        next_cord = next(iter(robot_neighbours - {previous_cord}))

    if last_cord and last_cord != (y, x):
        intersections[last_cord].add((y, x))
        intersections[(y, x)].add(last_cord)
    last_cord = (y, x)
    new_way = next(iter(way_char
                        for way_char, way_delta in ways.items()
                        if way_delta == (next_cord[0]-y, next_cord[1]-x)))
    temp_robot = next_cord, new_way


def get_way_and_dist(cord_1, cord_2):
    if cord_2[0] > cord_1[0]:
        return 'V', cord_2[0] - cord_1[0]
    elif cord_2[1] > cord_1[1]:
        return '>', cord_2[1] - cord_1[1]
    elif cord_2[0] < cord_1[0]:
        return '^', cord_1[0] - cord_2[0]
    return '<', cord_1[1] - cord_2[1]


def get_routes(
        robot, path=None, seen_corners=None, seen_intersections=None, tail=None,
        go_straight=True,  # bug made me implement full search which was useless
):
    robot_cord, robot_way = robot
    path = path or list()
    seen_corners = seen_corners or set()
    seen_intersections = seen_intersections or defaultdict(int)

    if len(intersections[robot_cord]) != 4:
        seen_corners.add(robot_cord)
    else:
        seen_intersections[robot_cord] += 1

    seen_inter = {k for k, v in seen_intersections.items() if v > 1}
    possible_inters = (
            intersections[robot_cord] - seen_corners - seen_inter - {tail}
    )
    for next_inter in possible_inters:
        next_way, dist = get_way_and_dist(robot_cord, next_inter)
        if go_straight and len(possible_inters) > 1 and robot_way != next_way:
            continue
        path_ = deepcopy(path)
        if robot_way == next_way:
            path_[-1][-1] += dist
        else:
            turn = 'R' if (robot_way, next_way) in turn_right else 'L'
            path_.append([turn, dist])
        if next_inter == finish_cord:
            seen_total = len(seen_corners) + len(seen_intersections)
            if seen_total == len(intersections):
                yield path_
            break
        yield from get_routes(
            (next_inter, next_way), path_, seen_corners.copy(),
            seen_intersections.copy(), robot_cord,
        )


def get_functions(path, functions=None) -> t.Optional[t.Tuple[list, dict]]:
    functions = functions or dict()

    # discover and try all remaining functions
    if len(functions) < 3:
        for chunk in range(5, 0, -1):
            path_ = path.copy()
            new_function = path[:chunk]

            # there's little chance new function will be same as previous one
            if new_function in functions.values():
                continue
            functions_ = functions.copy()
            functions_[function_names[len(functions)]] = new_function

            # store all functions that match beginning of path (at least one)
            matching_functions = []
            for name, pattern in functions_.items():
                if path_[:len(pattern)] == pattern:
                    if len(path_) == len(pattern):
                        return [name], functions  # answer

                    # consume current pattern and go deeper
                    sub_ans = get_functions(path_[len(pattern):], functions_)
                    if sub_ans:
                        return [name] + sub_ans[0], sub_ans[1]
                    matching_functions.append(([name], len(pattern)))

            # try all combinations of known functions and then go deeper
            while matching_functions:
                matching_functions_ = []
                for names, length in matching_functions:
                    for name, pattern in functions_.items():
                        if path_[length: length+len(pattern)] == pattern:
                            if len(path_) - length == len(pattern):
                                return names + [name], functions  # answer
                            sub_ans = get_functions(
                                path_[length+len(pattern):], functions_)
                            if sub_ans:
                                return names + [name] + sub_ans[0], sub_ans[1]
                            matching_functions_.append(
                                (names + [name], length + len(pattern))
                            )
                matching_functions = matching_functions_.copy()

    # recursively try to apply all possible combinations of known functions
    else:
        for name, pattern in functions.items():
            if path[:len(pattern)] == pattern:
                if len(path) == len(pattern):
                    return [name], functions  # answer
                sub_ans = get_functions(path[len(pattern):], functions)
                if sub_ans:
                    return [name] + sub_ans[0], sub_ans[1]


def parse_func(func_):
    return ','.join(turn + ',' + str(forward) for turn, forward in func_)


function_names = ['A', 'B', 'C']
order, funcs = next(filter(None, map(get_functions, get_routes(main_robot))))
inputs = (','.join(order) + '\n' +
          '\n'.join(map(parse_func, funcs.values())) + '\n' +
          'n' + '\n')

puzzle[0] = 2
program = run(map(ord, inputs).__next__)
time_print(list(program)[-1])
