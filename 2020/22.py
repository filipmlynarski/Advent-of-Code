def play(deck_1, deck_2, part):
    history = set()
    while deck_1 and deck_2:
        if part == 2:
            key = (tuple(deck_1), tuple(deck_2))
            if key in history:
                return deck_1, []
            history.add(key)

        card_1, card_2 = deck_1.pop(0), deck_2.pop(0)
        if part == 2 and len(deck_1) >= card_1 and len(deck_2) >= card_2:
            deck_1_after, _ = play(deck_1[:card_1], deck_2[:card_2],part)
            if len(deck_1_after):
                deck_1.extend([card_1, card_2])
            else:
                deck_2.extend([card_2, card_1])
        elif card_1 > card_2:
            deck_1.extend([card_1, card_2])
        else:
            deck_2.extend([card_2, card_1])

    return deck_1, deck_2


p1, p2 = open('puzzle/22.in').read().split('\n\n')
p1 = list(map(int, p1.splitlines()[1:]))
p2 = list(map(int, p2.splitlines()[1:]))

p1_after, p2_after = play(p1.copy(), p2.copy(), 1)
print(sum(i * j for i, j in enumerate(reversed(p1_after or p2_after), 1)))
p1_after, p2_after = play(p1.copy(), p2.copy(), 2)
print(sum(i * j for i, j in enumerate(reversed(p1_after or p2_after), 1)))
