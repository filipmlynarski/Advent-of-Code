puzzle = list(map(int, open('puzzle/16.in').read()))

message = puzzle.copy()
for _ in range(100):
    for idx in range(len(message)//2):
        message[idx] = abs(
            sum([1, 0, -1, 0][sub_idx // (idx+1) % 4] * num
                for sub_idx, num in enumerate(message[idx:]))
        ) % 10
    for idx in range(len(message)-2, len(message)//2-1, -1):
        message[idx] = (message[idx] + message[idx+1]) % 10
print(''.join(str(i) for i in message[:8]))

offset = int(''.join(str(i) for i in puzzle[:7]))
message = (puzzle * 10_000)[offset:]
for _ in range(100):
    for idx in range(len(message)-2, -1, -1):
        message[idx] = (message[idx] + message[idx+1]) % 10
print(''.join(str(i) for i in message[:8]))
