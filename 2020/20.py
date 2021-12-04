import sys
sys.dont_write_bytecode = True
from utils import *


class Tile:
    all_tiles = {}

    def __init__(self, id_, rows, rotated=0, flipped=None):
        self.all_tiles[(id_, rotated, flipped)] = self
        self.id = id_
        self.rows = rows
        self.width = len(self.rows)
        self.even = self.width % 2 == 0
        self.half = self.width // 2
        self.rotated = rotated
        self.flipped = flipped
        self.rows_cache = {}
        self.cols_cache = {}

    def get_line(self, row=None, col=None):
        if row is not None:
            if row in self.rows_cache:
                return self.rows_cache[row]
            (x_start, y_start), (x_end, y_end) = self.row_col_to_x_y(
                row=row % self.width)
        else:
            if col in self.cols_cache:
                return self.cols_cache[col]
            (x_start, y_start), (x_end, y_end) = self.row_col_to_x_y(
                col=col % self.width)

        for _ in range(self.rotated):
            x_start, y_start = -y_start, x_start
            x_end, y_end = -y_end, x_end

        if self.flipped == 'V':
            x_start *= -1
            x_end *= -1
        elif self.flipped == 'H':
            y_start *= -1
            y_end *= -1

        row_start, col_start = self.x_y_to_row_col(x_start, y_start)
        row_end, col_end = self.x_y_to_row_col(x_end, y_end)

        if row_start == row_end and col_start != col_end:
            if col_end > col_start:
                self.rows_cache[row] = self.rows[row_end]
                return self.rows[row_end]
            else:
                self.rows_cache[row] = list(reversed(self.rows[row_end]))
                return self.rows_cache[row]
        elif col_start == col_end and row_start != row_end:
            if row_end < row_start:
                self.cols_cache[col] = [
                    self.rows[~row_][col_end] for row_ in range(self.width)]
                return self.cols_cache[col]
            else:
                self.cols_cache[col] = [
                    self.rows[row_][col_end] for row_ in range(self.width)]
                return self.cols_cache[col]

    def row_col_to_x_y(self, row=None, col=None):
        if row is not None:
            x_start = -self.half
            y_start = self.half - row
            if self.even and y_start <= 0:
                y_start -= 1
            x_end = self.half
            y_end = y_start
        else:
            x_start = col - self.half
            if self.even and x_start >= 0:
                x_start += 1
            y_start = self.half
            x_end = x_start
            y_end = -self.half

        return (x_start, y_start), (x_end, y_end)

    def x_y_to_row_col(self, x, y):
        if self.even:
            if x > 0:
                x -= 1
            if y < 0:
                y += 1
        return (-y + self.half), (x + self.half)

    def __hash__(self):
        return hash((self.id, self.rotated, self.flipped))


@functools.lru_cache(maxsize=None)
def match(tile_1, tile_2, border):
    if border == 'U':
        lines = zip(tile_1.get_line(row=0), tile_2.get_line(row=-1))
    elif border == 'R':
        lines = zip(tile_1.get_line(col=-1), tile_2.get_line(col=0))
    elif border == 'D':
        lines = zip(tile_1.get_line(row=-1), tile_2.get_line(row=0))
    elif border == 'L':
        lines = zip(tile_1.get_line(col=0), tile_2.get_line(col=-1))
    else:
        raise ValueError('border has to be one of U R D L')
    return all(char_1 == char_2 for char_1, char_2 in lines)


@functools.lru_cache(maxsize=None)
def get_possible_tiles(this_tile, side):
    matching_tiles = set()
    for other_tile in Tile.all_tiles.values():
        if other_tile.id != this_tile.id and match(this_tile, other_tile, side):
            matching_tiles.add(other_tile)
    return matching_tiles


def get_image(path, seen):
    if len(path) == len(raw_tiles):
        return path
    row = len(path) // total_width
    col = len(path) % total_width
    tiles_to_right, tiles_below = None, None
    if col != 0:
        left_tile = path[total_width * row + (col - 1)]
        tiles_to_right = get_possible_tiles(left_tile, 'R')
    if row != 0:
        top_tile = path[total_width * (row - 1) + col]
        tiles_below = get_possible_tiles(top_tile, 'D')

    if tiles_to_right and tiles_below:
        new_tiles = tiles_to_right & tiles_below
    else:
        new_tiles = tiles_to_right or tiles_below or set()

    for new_tile in new_tiles - seen:
        sub_path = get_image(path + [new_tile], seen.union({new_tile}))
        if sub_path is not None:
            return sub_path


raw_tiles = open('puzzle/20.in').read().split('\n\n')
total_width = int(len(raw_tiles) ** .5)
for tile_lines in map(str.splitlines, raw_tiles):
    name = int(tile_lines[0].split()[-1][:-1])
    for rotation, flip in itertools.product(range(4), [None, 'V']):
        Tile(name, tile_lines[1:], rotation, flip)

picture = []
for tile in Tile.all_tiles.values():
    full_image = get_image([tile], set())
    if full_image:
        ans = (
                full_image[0].id *
                full_image[total_width-1].id *
                full_image[-total_width].id *
                full_image[-1].id
        )
        time_print(ans)
        for tiles_row in range(total_width):  # show image
            start_idx = tiles_row * total_width
            end_idx = start_idx + total_width
            for pixel_row in range(1, len(full_image[0].rows[0])-1):
                picture.append([])
                # print(*(''.join(tile_.get_line(row=pixel_row))  # show image
                #         for tile_ in full_image[start_idx: end_idx]), sep=' ')
                for tile_ in full_image[start_idx: end_idx]:
                    picture[-1].append(list(tile_.get_line(row=pixel_row))[1:-1])
            # print()
        break


def apply_pattern(pattern, image):
    total = 0
    for row, col in itertools.product(range(len(image) - len(pattern)),
                                      range(len(image[0]) - len(pattern[0]))):
        for sub_row, sub_col in itertools.product(range(len(pattern)),
                                                  range(len(pattern[0]))):
            if pattern[sub_row][sub_col] != '#':
                continue
            if image[row+sub_row][col+sub_col] != '#':
                break
        else:
            total += 1
    return total


picture = [''.join(''.join(i) for i in lines) for lines in picture]
Tile.all_tiles.clear()
dragon_pattern = list(map(list, """\
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """.splitlines()))
pic_hash = sum(line.count('#') for line in picture)
drake_hash = sum(line.count('#') for line in dragon_pattern)
for rotation, flip in itertools.product(range(4), [None, 'V']):
    tile_picture = Tile(0, picture, rotation, flip)
    n_dragons = apply_pattern(
        dragon_pattern,
        [tile_picture.get_line(row=row) for row in range(len(picture))],
    )
    if n_dragons:
        time_print(pic_hash - drake_hash * n_dragons)
        break
