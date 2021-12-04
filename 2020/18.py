import sys
sys.dont_write_bytecode = True
from utils import *


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


lines = open('puzzle/18.in').read().splitlines()
parsed_lines = list(map(parse, lines))
time_print(sum(evaluate(line, 1) for line in parsed_lines))
time_print(sum(evaluate(line, 2) for line in parsed_lines))


# class ReversedInt:
#     def __init__(self, value):
#         self.value = value
#
#     def __add__(self, other):
#         return ReversedInt(self.value + other.value)
#
#     def __radd__(self, other):
#         return ReversedInt(self.value + other).value
#
#     def __sub__(self, other):
#         return ReversedInt(self.value * other.value)
#
#     def __truediv__(self, other):
#         return ReversedInt(self.value + other.value)
#
#
# lines = [re.sub(r'(\d+)', r'ReversedInt(\1)', line.replace('*', '-'))
#          for line in lines]
# print(sum(map(eval, lines)))
# lines = [line.replace('+', '/') for line in lines]
# print(sum(map(eval, lines)))
