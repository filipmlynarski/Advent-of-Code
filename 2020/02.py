puzzle = open('puzzle/02.in').readlines()
part_1 = part_2 = 0
for range_, (letter, _), passwd in map(str.split, puzzle):
    low, high = map(int, range_.split('-'))
    part_1 += low <= sum(char == letter for char in passwd) <= high
    part_2 += (passwd[low - 1] == letter) ^ (passwd[high - 1] == letter)
print(part_1)
print(part_2)
