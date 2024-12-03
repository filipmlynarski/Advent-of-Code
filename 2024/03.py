from utils import *

sys.dont_write_bytecode = True

current_day = __file__.split('/')[-1].split('.')[0]
puzzle = open(f'puzzle/{current_day}.in').read()

part_1 = 0
part_2 = 0
do = True
for cmd in re.findall(r"(mul\(\d+,\d+\)|do\(\)|don't\(\))", puzzle):
    match cmd:
        case "don't()":
            do = False
        case "do()":
            do = True
        case _:
            a, b = get_ints(cmd)
            part_1 += a * b
            if do:
                part_2 += a * b

time_print(part_1)
time_print(part_2)
