#!/usr/bin/python
import argparse
import os
import re
import subprocess
import platform
from timeit import default_timer

__author__ = 'Filip Młynarski'

parser = argparse.ArgumentParser(
    description='This scripts benchmarks advent of code solutions')
parser.add_argument('-y', '--year', help='Year to benchmark', default=2019)
parser.add_argument(
    '-i', '--interpreter', help='Interpreter to use', default='python')
args = parser.parse_args()


def format_row(row):
    formatted = []
    for cell, fmt in zip(row, formatting.values()):
        if isinstance(cell, float):
            cell = f'{round(cell, fmt["round"]):0<{fmt["round"]+2}}s'
            formatted.append(f'{cell:>{fmt["width"]}}')
        else:
            formatted.append(cell.center(fmt['width']))
    return f'|{"|".join(formatted)}|'


match = re.compile('\d{2}.py').match
os.chdir(str(args.year))
files = filter(match, os.listdir('.'))

# TODO implement competition place (will do only if I get any :P)
formatting = {
    'day': {'width': 5},
    'part one': {'width': 10, 'round': 3},
    'part two': {'width': 10, 'round': 3},
    'total time': {'width': 10, 'round': 3},
}
separators = ("-" * col_format["width"] for col_format in formatting.values())
row_sep = f'+{"+".join(separators)}+'
print(f'Benchmarking year {args.year} '
      f'[interpreter: {args.interpreter}] '
      f'[CPU: {platform.processor()}]')
print(row_sep)
print(format_row(formatting.keys()))
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

    print(format_row([day.lstrip('0'), part_1_time, part_2_time, '']))
    print(row_sep)

print(format_row(['', '', '', total_time]))
print(row_sep)
