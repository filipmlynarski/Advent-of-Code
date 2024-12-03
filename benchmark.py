#!/usr/bin/python
import argparse
import os
import platform
import re
import subprocess
from datetime import date
from time import time

__author__ = 'Filip Młynarski'


def format_row(row_):
    formatted = []
    for cell, fmt in zip(row_, formatting.values()):
        if isinstance(cell, float):
            cell = f'{round(cell, fmt["round"]):0<{fmt["round"]+2}}s'
            formatted.append(f'{cell:>{fmt["width"]}}')
        elif isinstance(cell, int):
            formatted.append(str(cell).center(fmt['width']))
        else:
            formatted.append(cell.center(fmt['width']))
    return f'|{"|".join(formatted)}|'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This scripts benchmarks Advent of Code solutions')
    parser.add_argument(
        '-y', '--year', help='Year to benchmark (directory name)', default=date.today().year)
    parser.add_argument(
        '-i', '--interpreter', help='Interpreter to use', default='python')
    parser.add_argument(
        '-md', help='Format table in Markdown syntax', action='store_true', default=True)
    args = parser.parse_args()

    print(f'Benchmarking year {args.year} '
          f'[interpreter: {args.interpreter}] '
          f'[CPU: {platform.processor()}]')

    match = re.compile(r'\d{2}.py').match
    os.chdir(str(args.year))
    files = filter(match, os.listdir('.'))

    formatting = {
        'day': {'width': 8},
        'part one': {'width': 10, 'round': 3},
        'part two': {'width': 10, 'round': 3},
        'total time': {'width': 10, 'round': 3},
    }
    stats = dict()
    if os.path.isfile('stats.txt'):
        formatting.update({'place': {'width': 11}})
        stats = {
            day: f'{part_1}/{part_2}'
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
        start = time()

        process = subprocess.Popen([interpreter, file_name], stdout=subprocess.PIPE)
        try:
            time_1, *_ = process.stdout.readline().split()
        except ValueError:
            continue
        part_1_time = float(time_1) - start
        total_time += part_1_time
        part_2_time = ''
        if day != '25':
            time_2, *_ = process.stdout.readline().split()
            part_2_time = float(time_2) - start - part_1_time
            total_time += part_2_time

        row = [day.lstrip('0'), part_1_time, part_2_time, '', stats.get(day, '')]
        print(format_row(row))
        if not args.md:
            print(row_sep)

    print(format_row(['', '', '', total_time, '']))
    if not args.md:
        print(row_sep)
