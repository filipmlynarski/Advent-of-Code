import sys
sys.dont_write_bytecode = True
from utils import *
import typing as t
from math import ceil

reaction_map: t.Dict[str, t.Tuple[int, list]] = dict()
for line in open('puzzle/14.in').readlines():
    *left, right = (
        (int(amount), name)
        for amount, name in re.findall('(\d+) ([A-Z]+)', line)
    )
    reaction_map[right[1]] = (right[0], left)


def produce(name: str, amount: int) -> t.Generator[int, None, None]:
    min_amount, ingredients = reaction_map[name]
    dose = ceil(amount / min_amount)
    for ingredient_amount, ingredient_name in ingredients:
        if ingredient_name == 'ORE':
            yield ingredient_amount * dose
            continue

        ingredient_needed = ingredient_amount * dose - total[ingredient_name]
        if ingredient_needed <= 0:
            total[ingredient_name] = -ingredient_needed
            continue

        total[ingredient_name] = 0
        yield from produce(ingredient_name, ingredient_needed)
    total[name] += min_amount * dose - amount


total = defaultdict(int)
time_print(sum(produce('FUEL', 1)))

low = 0
high = total_ore = int(1e12)
while low < high:
    mid = (low + high + 1) // 2
    total.clear()
    if sum(produce('FUEL', mid)) < total_ore:
        low = mid
    else:
        high = mid - 1
time_print(low)
