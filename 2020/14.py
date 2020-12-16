import re


def get_ints(line_):
    return list(map(int, re.findall(r'-?\d+', line_)))


puzzle = open('puzzle/14.in').read()
lines = puzzle.splitlines()

part_1, part_2, mask = dict(), dict(), dict()
for line in lines:
    if line.startswith('mask'):
        mask = {idx: bit for idx, bit in enumerate(line.split()[-1])}
        continue
    address, value = get_ints(line)
    bin_value = list(bin(value)[2:].zfill(36))
    for key, bit in mask.items():
        if bit != 'X':
            bin_value[key] = bit
    address = bin(address)[2:].zfill(36)
    part_1[address] = int(''.join(bin_value), 2)

    addresses = [list(address)]
    for key, val in mask.items():
        if val == '1':
            for address_ in addresses:
                address_[key] = '1'
        elif val == 'X':
            new_addresses = []
            for address_ in addresses:
                for i in ['0', '1']:
                    address_[key] = i
                    new_addresses.append(address_.copy())
            addresses = new_addresses
    for address_ in addresses:
        part_2[int(''.join(address_), 2)] = value

print(sum(part_1.values()))
print(sum(part_2.values()))
