from collections import defaultdict

puzzle = (i.split(')') for i in open('puzzle/06.in').read().splitlines())

parent_children = defaultdict(set)
full_mapping = defaultdict(set)
for parent, child in puzzle:
    parent_children[parent].add(child)
    full_mapping[parent].add(child)
    full_mapping[child].add(parent)


def dig(key, depth=0):
    ret = depth
    for planet in parent_children[key]:
        ret += dig(planet, depth + 1)
    return ret


def find(to_check, depth=0):
    _to_check = set()
    for you in to_check:
        for planet in full_mapping[you] - to_check:
            if planet == 'SAN':
                return depth
            _to_check.add(planet)
    return find(_to_check, depth + 1)


print(dig('COM'))
print(find(full_mapping['YOU']))
