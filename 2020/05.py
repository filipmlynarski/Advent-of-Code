import sys
sys.dont_write_bytecode = True
from utils import *

def get_id(line):
    line = line.translate(str.maketrans('FBLR', '0101'))
    row, col = int(line[:-3], 2), int(line[-3:], 2)
    return row * 8 + col


inp = open('puzzle/05.in').read().splitlines()
seat_ids = set(map(get_id, inp))
time_print(max(seat_ids))

for seat_id in seat_ids:
    if seat_id - 1 not in seat_ids and seat_id - 2 in seat_ids:
        time_print(seat_id - 1)
