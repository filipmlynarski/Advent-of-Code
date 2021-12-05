import sys
sys.dont_write_bytecode = True
from utils import *
import typing as t

puzzle: t.List[t.List[str]] = list(
    map(list, open('puzzle/18.in').read().splitlines())
)
start_cord = None
total_keys = 0
for row in range(len(puzzle)):
    for col in range(len(puzzle[row])):
        if puzzle[row][col] == '@':
            start_cord = row, col
            puzzle[row][col] = '.'
        elif puzzle[row][col].islower():
            total_keys += 1


@lru_cache(maxsize=len(puzzle)*len(puzzle[0]))
def horizontal_cords(y, x):
    ret = []
    for y_delta, x_delta in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        new_y, new_x = y + y_delta, x + x_delta
        if not (0 <= new_y < len(puzzle) and 0 <= new_x < len(puzzle[0])):
            continue

        val = puzzle[new_y][new_x]
        if val != '#':
            ret.append(((new_y, new_x), val))

    return ret


def explore(cords, keys, seen):
    session = {'cords': [], 'keys': keys, 'seen': seen}
    for cord in cords:
        for next_cord, val in horizontal_cords(*cord):
            if next_cord in seen:
                continue

            if val == '.' or val in keys or val.lower() in keys:
                session['cords'].append(next_cord)
                session['seen'].add(next_cord)
            elif val.islower() and val not in keys:
                yield {
                    'cords': [next_cord],
                    'keys': keys.union({val}),
                    'seen': set(),
                }

    yield session


def explore_2(cords, keys, seen):
    session = {'cords': [], 'keys': keys, 'seen': seen}
    for robots in cords:
        for robot_idx, robot in enumerate(robots):
            for next_cord, val in horizontal_cords(*robot):
                if next_cord in seen:
                    continue

                if val == '.' or val in keys or val.lower() in keys:
                    robots_ = [
                        robot_ if idx != robot_idx else next_cord
                        for idx, robot_ in enumerate(robots)
                    ]
                    session['cords'].append(robots_)
                    session['seen'].add(next_cord)
                elif val.islower() and val not in keys:
                    robots_ = [
                        robot_ if idx != robot_idx else next_cord
                        for idx, robot_ in enumerate(robots)
                    ]
                    yield {
                        'cords': [robots_],
                        'keys': keys.union({val}),
                        'seen': set(),
                    }

    yield session


def solve(func, sessions, trim=30, depth=0):
    sessions_ = list()
    for session in sessions:
        if len(session['keys']) == total_keys:
            return depth
        sessions_.extend(func(**session))
    sessions_ = sorted(sessions_, key=lambda sess: len(sess['keys']))[-trim:]

    return solve(func, sessions_, trim, depth+1)


starting_session = {'cords': [start_cord], 'keys': set(), 'seen': set()}
time_print(solve(explore, [starting_session]))

horizontal_cords.cache_clear()
for (y_cord, x_cord), _ in horizontal_cords(*start_cord):
    puzzle[y_cord][x_cord] = '#'
vertical_cords = [
    (start_cord[0]+y_delta, start_cord[1]+x_delta)
    for y_delta, x_delta in [(-1, -1), (-1, 1), (1, 1), (1, -1)]
]
starting_session = {'cords': [vertical_cords], 'keys': set(), 'seen': set()}
time_print(solve(explore_2, [starting_session]))
