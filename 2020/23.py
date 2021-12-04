import sys
sys.dont_write_bytecode = True
from utils import *

def play(cups, rounds):
    linked_cups = dict(zip(cups, cups[1:] + [cups[0]]))
    current_cup = cups[0]
    for _ in range(rounds):
        stack = [linked_cups[current_cup]]
        for _ in range(2):
            stack.append(linked_cups[stack[-1]])
        next_cup = current_cup - 1 or len(cups)
        while next_cup in stack or next_cup == 0:
            next_cup = (next_cup - 1) or len(cups)
        linked_cups[current_cup] = linked_cups[stack[-1]]
        linked_cups[stack[-1]] = linked_cups[next_cup]
        linked_cups[next_cup] = stack[0]
        current_cup = linked_cups[current_cup]
    return linked_cups


puzzle = list(map(int, open('puzzle/23.in').read()))
game_1_cups = play(puzzle, 100)
ans = [game_1_cups[1]]
for _ in range(7):
    ans.append(game_1_cups[ans[-1]])
time_print(''.join(map(str, ans)))

game_2 = play(puzzle + list(range(10, 1_000_001)), 10_000_000)
time_print(game_2[1] * game_2[game_2[1]])
