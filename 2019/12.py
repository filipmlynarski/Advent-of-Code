import sys
sys.dont_write_bytecode = True
from utils import *
from math import gcd

moons_positions = [list(map(int, re.findall('-?\d+', line)))
                   for line in open('puzzle/12.in').readlines()]
n_moons = len(moons_positions)
n_axis = len(moons_positions[0])
moons_velocities = [[0 for _ in range(n_axis)] for _ in range(n_moons)]

start_positions = [[position[axis] for position in moons_positions]
                   for axis in range(n_axis)]
start_velocities = [[velocity[axis] for velocity in moons_velocities]
                    for axis in range(n_axis)]

periods_not_found = list(range(n_axis))
period = 1


def tick():
    global steps, period

    for main_idx, main_moon in enumerate(moons_positions):
        for other_idx, other_moon in enumerate(moons_positions):
            if main_idx == other_idx:
                continue
            for axis in range(n_axis):
                if main_moon[axis] < other_moon[axis]:
                    moons_velocities[main_idx][axis] += 1
                elif main_moon[axis] > other_moon[axis]:
                    moons_velocities[main_idx][axis] -= 1
    for moon_idx in range(n_moons):
        for axis, delta in enumerate(moons_velocities[moon_idx]):
            moons_positions[moon_idx][axis] += delta

    steps += 1

    for axis in reversed(periods_not_found):
        current_position = (position[axis] for position in moons_positions)
        positions_to_compare = zip(start_positions[axis], current_position)
        if all(pos_1 == pos_2 for pos_1, pos_2 in positions_to_compare):
            current_velocity = (velocity[axis] for velocity in moons_velocities)
            velocities_to_compare = zip(start_velocities[axis],
                                        current_velocity)
            if all(vel_1 == vel_2 for vel_1, vel_2 in velocities_to_compare):
                periods_not_found.remove(axis)
                period = period * steps // gcd(period, steps)  # lcm


steps = 0
for _ in range(1000):
    tick()
time_print(sum(sum(map(abs, positions)) * sum(map(abs, velocities))
               for positions, velocities in zip(moons_positions, moons_velocities)))

while periods_not_found:
    tick()
time_print(period)
