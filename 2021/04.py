import sys
sys.dont_write_bytecode = True
from utils import *

puzzle = open('puzzle/04.in').read()
numbers = ints(puzzle.splitlines()[0])
raw_boards = puzzle.split('\n\n')[1:]
width = len(raw_boards[0].splitlines())

boards = []
for board in raw_boards:
    boards.append({})
    for row, line in enumerate(board.splitlines()):
        for col, value in enumerate(ints(line)):
            boards[-1][(row, col)] = value

winning_cases = []
for idx in range(width):
    winning_cases.append({(idx, i) for i in range(width)})
    winning_cases.append({(i, idx) for i in range(width)})

board_matches = [set() for _ in boards]
won_boards = set()
for number in numbers:
    for board_idx, board in enumerate(boards):
        if board_idx in won_boards:
            continue
        for (row, col), value in board.items():
            if value == number:
                board_matches[board_idx].add((row, col))
                for winner in winning_cases:
                    if winner.issubset(board_matches[board_idx]):
                        values = 0
                        for cord in set(board) - board_matches[board_idx]:
                            values += board[cord]
                        won_boards.add(board_idx)
                        if len(won_boards) == 1:
                            print(number * values)
                        elif len(won_boards) == len(boards):
                            print(number * values)
                        break
