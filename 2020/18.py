def parse(line):
    mapping = {'(': '[', ')': ']', ' ': ',', '*': '"*"', '+': '"+"'}
    return eval(line.translate(str.maketrans(mapping)))


def evaluate(equation, part):
    flatten = []
    for char in equation:
        if not isinstance(char, list):
            flatten.append(char)
        else:
            flatten.append(evaluate(char, part))

    if part == 1:
        ans = flatten.pop(0)
        while flatten:
            operator = flatten.pop(0)
            char = flatten.pop(0)
            ans = ans + char if operator == '+' else ans * char
        return ans

    for idx in range(len(flatten)-1, 0, -1):
        if flatten[idx] == '+':
            flatten[idx-1: idx+2] = [flatten[idx-1] + flatten[idx+1]]
    ans = flatten.pop(0)
    for char in flatten[1::2]:
        ans *= char
    return ans


lines = list(map(parse, open('puzzle/18.in').read().splitlines()))
print(sum(evaluate(line, 1) for line in lines))
print(sum(evaluate(line, 2) for line in lines))
