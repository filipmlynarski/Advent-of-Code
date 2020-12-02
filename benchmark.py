#!/usr/bin/python
import argparse
import os
import re
import subprocess
import platform
from timeit import default_timer

__author__ = 'Filip Młynarski'

parser = argparse.ArgumentParser(
    description='This scripts benchmarks Advent of Code solutions')
parser.add_argument(
    '-y', '--year', help='Year to benchmark (directory name)', default=2020)
parser.add_argument(
    '-i', '--interpreter', help='Interpreter to use', default='python')
parser.add_argument(
    '-md', help='Format table in Markdown syntax', action='store_true')
args = parser.parse_args()


def format_row(row_):
    formatted = []
    for cell, fmt in zip(row_, formatting.values()):
        if isinstance(cell, float):
            cell = f'{round(cell, fmt["round"]):0<{fmt["round"]+2}}s'
            formatted.append(f'{cell:>{fmt["width"]}}')
        else:
            formatted.append(cell.center(fmt['width']))
    return f'|{"|".join(formatted)}|'


print(f'Benchmarking year {args.year} '
      f'[interpreter: {args.interpreter}] '
      f'[CPU: {platform.processor()}]')

match = re.compile('\d{2}.py').match
os.chdir(str(args.year))
files = filter(match, os.listdir('.'))

formatting = {
    'day': {'width': 5},
    'part one': {'width': 10, 'round': 3},
    'part two': {'width': 10, 'round': 3},
    'total time': {'width': 10, 'round': 3},
}
stats = dict()
if os.path.isfile('stats.txt'):
    formatting.update({'stats': {'width': 11}})
    stats = {
        day: f'#{part_1}/#{part_2}'
        for day, part_1, part_2 in map(str.split, open('stats.txt').readlines())
    }

separators = ('-' * col_format['width'] for col_format in formatting.values())
row_sep = f'+{"+".join(separators)}+'
if not args.md:
    print(row_sep)
print(format_row(formatting.keys()))

if args.md:
    md_separators = []
    for col_format in formatting.values():
        if 'round' in col_format:
            md_separators.append(f'{"-" * (col_format["width"] - 1)}:')
        else:
            md_separators.append(f':{"-" * (col_format["width"] - 2)}:')
    print(f'|{"|".join(md_separators)}|')
else:
    print(row_sep.replace('-', '='))

total_time = 0
interpreter = args.interpreter
for file_name in sorted(files):
    day, _ = file_name.split('.', 1)
    start = default_timer()

    process = subprocess.Popen([interpreter, file_name], stdout=subprocess.PIPE)
    process.stdout.readline()
    part_1_time = default_timer() - start
    process.stdout.read()
    part_2_time = default_timer() - start - part_1_time
    total_time += part_1_time + part_2_time

    row = [day.lstrip('0'), part_1_time, part_2_time, '', stats.get(day, '')]
    print(format_row(row))
    if not args.md:
        print(row_sep)

print(format_row(['', '', '', total_time, '']))
if not args.md:
    print(row_sep)
