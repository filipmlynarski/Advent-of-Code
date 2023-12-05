from utils import *

sys.dont_write_bytecode = True

current_day = __file__.split('/')[-1].split('.')[0]
puzzle = open(f'puzzle/{current_day}.in').read()

lines = puzzle.splitlines()
valves = {}
for line in lines:
    words = line.split()
    key = words[1]
    pressure = int(words[4].split('=')[1][:-1])
    tunnels = [word.strip(',') for word in words[9:]]
    valves[key] = (pressure, tunnels)


def get_part_1():
    paths = [('AA', 2, set(), 0)]  # -1 - not opening, 0 - opening, 1 - opened
    for minute in range(30):
        new_paths: list[tuple[str, int, set, int]] = []
        for valve, open_status, open_valves, total_pressure in paths:
            total_pressure += sum(valves[valve][0] for valve in open_valves)
            if open_status != 0:
                for new_valve in valves[valve][1]:
                    if new_valve not in open_valves:
                        new_paths.append((new_valve, -1, open_valves, total_pressure))
                        new_paths.append((new_valve, 0, open_valves, total_pressure))
                    else:
                        new_paths.append((new_valve, 2, open_valves, total_pressure))
            else:
                new_paths.append((valve, 1, {*open_valves, valve}, total_pressure))
        paths = new_paths.copy()
        paths.sort(key=lambda x: -x[-1])
        paths = paths[:30_000]

    return max(map(lambda x: x[-1], paths))


def get_new_steps(valve, open_status, open_valves):
    ret = []
    if open_status != 0:
        for new_valve in valves[valve][1]:
            if new_valve not in open_valves:
                ret.append((new_valve, -1, set()))
                ret.append((new_valve, 0, set()))
            else:
                ret.append((new_valve, 2, set()))
    else:
        ret.append((valve, 1, {valve}))
    return ret


def get_part_2():
    paths = [(('AA', 2), ('AA', 2), set(), 0)]  # -1 - not opening, 0 - opening, 1 - opened
    for minute in range(26):
        new_paths: list[tuple[tuple[str, int], tuple[str, int], set, int]] = []
        for (valve_1, open_status_1), (valve_2, open_status_2), open_valves, total_pressure in paths:
            total_pressure += sum(valves[valve][0] for valve in open_valves)
            for new_valve_1, new_open_status_1, opened_1 in get_new_steps(valve_1, open_status_1, open_valves):
                for new_valve_2, new_open_status_2, opened_2 in get_new_steps(valve_2, open_status_2, open_valves):
                    new_paths.append((
                        (new_valve_1, new_open_status_1),
                        (new_valve_2, new_open_status_2),
                        {*open_valves, *opened_1, *opened_2},
                        total_pressure,
                    ))

        paths = new_paths.copy()
        paths.sort(key=lambda x: -x[-1])
        paths = paths[:100_000]

    return max(map(lambda x: x[-1], paths))


time_print(get_part_1())
time_print(get_part_2())
