from utils import *

sys.dont_write_bytecode = True

current_day = __file__.split('/')[-1].split('.')[0]
puzzle = open(f'puzzle/{current_day}.in').read()


def get_type(hand: str) -> int:
    counter = Counter(hand)
    values = sorted(list(counter.values()))
    if len(values) == 1:
        return 7
    elif values == [1, 4]:
        return 6
    elif values == [2, 3]:
        return 5
    elif values == [1, 1, 3]:
        return 4
    elif values == [1, 2, 2]:
        return 3
    elif values == [1, 1, 1, 2]:
        return 2
    elif len(values) == 5:
        return 1
    raise ValueError("Invalid hand")


def get_compare(order, type_fnc):
    def compare(line_a, line_b):
        hand_a = line_a.split()[0]
        hand_b = line_b.split()[0]
        type_a = type_fnc(hand_a)
        type_b = type_fnc(hand_b)
        if type_a != type_b:
            return 1 if type_a > type_b else -1
        for card_a, card_b in zip(hand_a, hand_b):
            order_a = order.index(card_a)
            order_b = order.index(card_b)
            if order_a != order_b:
                return 1 if order_a < order_b else -1
        raise ValueError("Invalid hand")
    return compare


lines = puzzle.splitlines()
compare_fnc = get_compare(
    order="A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2".split(", "),
    type_fnc=get_type,
)
lines.sort(key=functools.cmp_to_key(compare_fnc))
ans = 0
for idx, line in enumerate(lines, 1):
    ans += idx * int(line.split()[1])
print(ans)


def hand_generator(hand):
    for card in "A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2".split(", "):
        new_hand = hand.replace("J", card)
        if "J" in new_hand:
            yield from hand_generator(new_hand)
        else:
            yield get_type(new_hand)


def get_type_wildcard(hand: str) -> int:
    if "J" in hand:
        # print("a")
        return max(hand_generator(hand))
    return get_type(hand)


# print(get_type_wildcard("QQQJ5"))
# exit()

compare_fnc = get_compare(
    order="A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J".split(", "),
    type_fnc=get_type_wildcard,
)
lines.sort(key=functools.cmp_to_key(compare_fnc))
ans = 0
for idx, line in enumerate(lines, 1):
    ans += idx * int(line.split()[1])
print(ans)
