import sys
sys.dont_write_bytecode = True
from utils import *

bags = dict()
for line in open('puzzle/07.in').read().splitlines():
    left_bag, right_bags = line.split(' contain ')
    left_bag = tuple(left_bag.split()[:2])
    bags[left_bag] = list()
    if right_bags != 'no other bags.':
        for right_bag in right_bags.split(', '):
            amount, *colors, _ = right_bag.split()
            bags[left_bag].append((int(amount), tuple(colors)))


def part_1(bag_color: tuple) -> bool:
    return any(color == target or part_1(color)
               for _, color in bags[bag_color])


def part_2(bag_color: tuple) -> int:
    return 1 + sum(cnt * part_2(color) for cnt, color in bags[bag_color])


target = 'shiny', 'gold'
time_print(sum(map(part_1, bags)))
time_print(part_2(target) - 1)
