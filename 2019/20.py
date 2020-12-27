import typing as t
from collections import defaultdict
from functools import lru_cache

Cord = t.Tuple[int, int]

uppercase = {chr(num) for num in range(ord('A'), ord('Z') + 1)}
lines = open('puzzle/20.in').read().splitlines()
n_cols = max(map(len, lines))
lines = [line.ljust(n_cols, ' ') for line in lines]
portals = defaultdict(list)
for row_idx in range(1, len(lines) - 1):
    for col_idx in range(1, len(lines[row_idx]) - 1):
        char = lines[row_idx][col_idx]
        if char not in uppercase:
            continue

        right_char = lines[row_idx][col_idx + 1]
        left_char = lines[row_idx][col_idx - 1]
        top_char = lines[row_idx - 1][col_idx]
        bottom_char = lines[row_idx + 1][col_idx]

        if top_char in uppercase and bottom_char == '.':
            portals[top_char + char].append((row_idx + 1, col_idx))
        elif top_char == '.' and bottom_char in uppercase:
            portals[char + bottom_char].append((row_idx - 1, col_idx))
        elif left_char in uppercase and right_char == '.':
            portals[left_char + char].append((row_idx, col_idx + 1))
        elif left_char == '.' and right_char in uppercase:
            portals[char + right_char].append((row_idx, col_idx - 1))

portals_mapping = {}
start = end = None
outer_rows = {2, len(lines) - 3}
outer_cols = {2, n_cols - 3}
for portal_name, portal_cords in portals.items():
    if portal_name == 'AA':
        start = portal_cords[0]
    elif portal_name == 'ZZ':
        end = portal_cords[0]
    else:
        if portal_cords[1][0] in outer_rows or portal_cords[1][1] in outer_cols:
            inner, outer = portal_cords[0], portal_cords[1]
        else:
            inner, outer = portal_cords[1], portal_cords[0]
        portals_mapping[inner] = outer, 1
        portals_mapping[outer] = inner, -1


@lru_cache(maxsize=None)
def get_neighbours(cord: Cord) -> t.Dict[Cord, int]:
    """
    Given coordinate return list of possible neighbours
    (and whether they are portals).
    """
    ret = {}
    if cord in portals_mapping:
        after_portal, level_delta = portals_mapping[cord]
        ret[after_portal] = level_delta
    for row_delta, col_delta in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        new_row = cord[0] + row_delta
        new_col = cord[1] + col_delta
        if not 0 <= new_row < len(lines) or not 0 <= new_col < n_cols:
            continue
        if lines[new_row][new_col] == '.':
            ret[(new_row, new_col)] = 0

    return ret


@lru_cache(maxsize=None)
def get_paths_to_portals(cord: Cord) -> t.List[t.Tuple[Cord, int, int]]:
    """
    Given portal coordinate return all possible paths to other portals
    (with cord we'll end up after going through, length of that path,
    and whether portal takes us to deeper of higher level,
    if we'll end up on same level (level_delta=0), portal is the end).
    """
    paths, seen = [cord], {cord}
    ret = []
    length = 0
    while paths:
        length += 1
        new_paths = []
        for cord_ in paths:
            for next_cord, level_delta in get_neighbours(cord_).items():
                if next_cord in seen:
                    continue
                if next_cord == end:
                    ret.append((next_cord, length, level_delta))
                elif level_delta != 0 and cord_ != cord:
                    ret.append((cord_, length, level_delta))
                elif level_delta == 0:
                    new_paths.append(next_cord)
                    seen.add(next_cord)
        paths = new_paths

    return ret


def escape(paths: t.List, ans: t.Optional[int] = None, part: int = 1) -> int:
    """
    Given current pathways made of portals recursively explore maze to find
    shortest possible route to the end portal.
    """
    new_paths = []
    for cord, level, total_length in paths:
        for portal_cord, length, level_delta in get_paths_to_portals(cord):
            new_level = level + level_delta
            new_length = total_length + length
            if new_level < 0 or (ans and new_length > ans):
                continue
            if portal_cord == end:
                if new_level == 0 or part == 1:
                    ans = new_length if not ans else min(ans, new_length)
                continue
            after_portal, _ = portals_mapping[portal_cord]
            new_paths.append((after_portal, new_level, new_length))

    return escape(new_paths, ans, part) if new_paths else ans


print(escape([(start, 0, 0)], part=1))
print(escape([(start, 0, 0)], part=2))
