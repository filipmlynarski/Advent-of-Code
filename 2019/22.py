import sys
sys.dont_write_bytecode = True
from utils import *


def shuffle_p1(n_cards, card_id):
    cards = list(range(n_cards))
    for line in lines:
        line = line.split()
        if line[1] == 'with':
            value = int(line[-1])
            new_cards = cards.copy()
            for idx in range(n_cards):
                new_cards[(idx * value) % n_cards] = cards.pop(0)
            cards = new_cards.copy()
        elif line[1] == 'into':
            cards = cards[::-1]
        elif line[0] == 'cut':
            value = int(line[-1])
            cards = cards[value:] + cards[:value]
    return cards.index(card_id)


def shuffle_p2(n_cards, n_shuffles, card_id):  # mcpower answer

    def inv(n):
        # gets the modular inverse of n
        # as cards is prime, use Euler's theorem
        return pow(n, n_cards-2, n_cards)

    increment_mul = 1  # how much things increment per index
    offset_diff = 0  # what's the first number?

    for line in lines:
        line = line.split()
        if line[1] == 'with':
            increment_mul *= inv(int(line[-1]))
            increment_mul %= n_cards
        elif line[1] == 'into':
            increment_mul *= -1
            increment_mul %= n_cards
            offset_diff += increment_mul
            offset_diff %= n_cards
        elif line[0] == 'cut':
            offset_diff += int(line[-1]) * increment_mul
            offset_diff %= n_cards
        else:
            raise ValueError(line)

    def get_sequence(iterations):
        # calculate (increment, offset) for the number of iterations of the process
        # increment = increment_mul^iterations
        inc = pow(increment_mul, iterations, n_cards)
        # offset = 0 + offset_diff * (1 + increment_mul + increment_mul^2 + ... + increment_mul^iterations)
        # use geometric series.
        off = offset_diff * (1 - inc) * inv((1 - increment_mul) % n_cards)
        off %= n_cards
        return inc, off

    increment, offset = get_sequence(n_shuffles)
    return (offset + increment * card_id) % n_cards


lines = open('puzzle/22.in').read().splitlines()
time_print(shuffle_p1(10007, 2019))
time_print(shuffle_p2(119315717514047, 101741582076661, 2020))
