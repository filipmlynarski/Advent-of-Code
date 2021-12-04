import sys
sys.dont_write_bytecode = True
from utils import *


def create_rule(parsed_line):
    min_1, max_1, min_2, max_2 = map(int, parsed_line)

    def rule(num):
        return min_1 <= num <= max_1 or min_2 <= num <= max_2
    return rule


raw_rules, my_ticket, nearby_tickets = open('puzzle/16.in').read().split('\n\n')
my_ticket = list(map(int, my_ticket.splitlines()[-1].split(',')))
nearby_tickets = nearby_tickets.splitlines()[1:]

parsed_rules = re.findall(r'(.+): (\d+)-(\d+) or (\d+)-(\d+)', raw_rules)
rules = {name: create_rule(ranges) for name, *ranges in parsed_rules}


def get_first_invalid(ticket_):
    for value in ticket_:
        if not any(rule(value) for rule in rules.values()):
            return value


total_invalid = 0
valid_tickets = [my_ticket]
for ticket in nearby_tickets:
    ticket = list(map(int, ticket.split(',')))
    invalid_value = get_first_invalid(ticket)
    if invalid_value is not None:
        total_invalid += invalid_value
    else:
        valid_tickets.append(ticket)
time_print(total_invalid)


def get_matching_columns(rule):
    return set.intersection(
        *({idx for idx, value in enumerate(valid_ticket) if rule(value)}
          for valid_ticket in valid_tickets)
    )


all_matching_columns = {name: get_matching_columns(rule)
                        for name, rule in rules.items()}
seen = set()
ans = 1
for name, cols in sorted(all_matching_columns.items(), key=lambda x: len(x[1])):
    if name.startswith('departure'):
        ans *= my_ticket[next(iter(cols - seen))]
    seen.update(cols)
time_print(ans)
