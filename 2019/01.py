puzzle = list(map(int, open('puzzle/01.in').read().splitlines()))


def f(x):
    return x // 3 - 2


def f2(x):
    x = f(x)
    if x <= 0:
        return 0
    return x + f2(x)


print(sum(map(f, puzzle)))
print(sum(map(f2, puzzle)))
