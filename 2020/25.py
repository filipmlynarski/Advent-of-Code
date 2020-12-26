card_pub, door_pub = list(map(int, open('puzzle/25.in').read().splitlines()))
modulus = 20201227
subject = loop_size = 1
card_loop = door_loop = None
while not (card_loop or door_loop):
    subject = subject * 7 % modulus
    if subject == card_pub:
        card_loop = loop_size
    if subject == door_pub:
        door_loop = loop_size
    loop_size += 1
print(pow(card_pub if door_loop else door_pub, door_loop or card_loop, modulus))
