from collections import Counter

puzzle = open('puzzle/08.in').read()
width = 25
height = 6
layer_size = width * height
layers = [puzzle[idx: idx+layer_size]
          for idx in range(0, len(puzzle), layer_size)]

least_zeros = min(map(Counter, layers), key=lambda counter: counter['0'])
print(least_zeros['1'] * least_zeros['2'])

message = [['2' for _ in range(width)] for height in range(height)]
for layer in layers:
    for idx, char in enumerate(layer):
        if message[idx // width][idx % width] == '2':
            message[idx // width][idx % width] = char
print('\n'.join(''.join(i).replace('0', ' ') for i in message))
