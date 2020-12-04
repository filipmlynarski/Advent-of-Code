def validate(pair):
    key, value = pair
    if key == 'byr':
        return 1920 <= int(value) <= 2002
    elif key == 'iyr':
        return 2010 <= int(value) <= 2020
    elif key == 'eyr':
        return 2020 <= int(value) <= 2030
    elif key == 'hgt':
        height, unit = int(value[:-2]), value[-2:]
        return 150 <= height <= 193 if unit == 'cm' else 59 <= height <= 76
    elif key == 'hcl':
        try:
            return len(value) == 7 and int(value[1:], 16) is not None
        except ValueError:
            return False
    elif key == 'ecl':
        return value in 'amb blu brn gry grn hzl oth'.split()
    elif key == 'pid':
        return len(value) == 9 and value.isdigit()
    return True


part_1 = part_2 = 0
passport = dict()
req = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
for line in open('puzzle/04.in').read().splitlines() + ['']:
    if line:
        passport.update(dict(k_v.split(':') for k_v in line.split()))
    else:
        if req.issubset(passport.keys()):
            part_1 += 1
            if all(map(validate, passport.items())):
                part_2 += 1
        passport = dict()

print(part_1)
print(part_2)
