import sys
sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/13.in').read().splitlines()
depart = int(puzzle[0])
buses = [(int(bus_interval), bus_time % int(bus_interval))
         for bus_time, bus_interval in enumerate(puzzle[1].split(','))
         if bus_interval != 'x']
time_print(int.__mul__(*min(((val, -depart % val) for val, _ in buses),
                            key=lambda x: x[1])))

final_time = buses[0][0] - buses[0][1]
delta = final_time
for bus_interval, bus_time in buses[1:]:
    current_time = final_time
    while -current_time % bus_interval != bus_time:
        current_time += delta
    final_time = current_time
    delta *= bus_interval
time_print(final_time)
