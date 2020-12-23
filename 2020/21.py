import re
from collections import Counter, defaultdict

raw_lines = open('puzzle/21.in').read()
allergen_to_foods = defaultdict(list)
foods_counted = Counter()
for ingredients, allergens in re.findall(r'(.+) \(contains (.+)\)', raw_lines):
    foods_counted.update(ingredients.split())
    for allergen in allergens.split(', '):
        allergen_to_foods[allergen].append(set(ingredients.split()))

food_to_allergen = {}
while True:
    for allergen_name, foods_sets in allergen_to_foods.items():
        possible_foods = set.intersection(*foods_sets)
        if len(possible_foods) == 1:
            food_name = next(iter(possible_foods))
            food_to_allergen[food_name] = allergen_name
            for sub_foods_sets in allergen_to_foods.values():
                for sub_foods in sub_foods_sets:
                    sub_foods -= {food_name}
            break
    else:
        break

print(sum(map(foods_counted.get, foods_counted - food_to_allergen.keys())))
print(','.join(sorted(food_to_allergen, key=food_to_allergen.get)))
