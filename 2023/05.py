from utils import *

sys.dont_write_bytecode = True

current_day = __file__.split('/')[-1].split('.')[0]
puzzle = open(f'puzzle/{current_day}.in').read()


def get_part1():
    chunks = puzzle.split('\n\n')
    seeds = get_ints(chunks.pop(0))

    for chunk in chunks:
        ranges = []
        for line in chunk.split('\n')[1:]:
            b, a, c = get_ints(line)
            ranges.append((range(a, a+c), b-a))
        new_seeds = seeds.copy()
        for range_fnc, offset in ranges:
            for idx, seed in enumerate(seeds):
                if seed in range_fnc:
                    new_seeds[idx] += offset
        seeds = new_seeds.copy()

    return min(seeds)


def get_part2():
    chunks = puzzle.split('\n\n')
    seed_ranges = get_ints(chunks.pop(0))
    seeds = []
    for start, length in zip(seed_ranges[::2], seed_ranges[1::2]):
        seeds.append((start, start+length-1))

    for chunk in chunks:
        ranges = []
        for line in chunk.split('\n')[1:]:
            b, a, c = get_ints(line)
            ranges.append(((a, a+c-1), b-a))

        new_seeds = []
        for orig_seed_start, orig_seed_end in seeds:
            seeds_a = [(orig_seed_start, orig_seed_end)]
            seeds_b = []
            for (range_start, range_end), offset in ranges:
                seeds_a_new = []
                for (seed_start, seed_end) in seeds_a:
                    if range_start <= seed_start <= range_end:
                        if seed_end <= range_end:
                            seeds_b.append((seed_start+offset, seed_end+offset))
                        else:
                            seeds_a_new.append((range_end+1, seed_end))
                            seeds_b.append((seed_start+offset, range_end+offset))
                    elif range_start <= seed_end <= range_end:
                        seeds_a_new.append((seed_start, range_start-1))
                        seeds_b.append((range_start+offset, seed_end+offset))
                    else:
                        seeds_a_new.append((seed_start, seed_end))
                seeds_a = seeds_a_new.copy()

            new_seeds.extend(seeds_a)
            new_seeds.extend(seeds_b)

        seeds = new_seeds.copy()

    return min(a for a, _ in seeds)


time_print(get_part1())
time_print(get_part2())
