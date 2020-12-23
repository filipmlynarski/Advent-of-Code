from functools import lru_cache

raw_rules, lines = open('puzzle/19.in').read().split('\n\n')
rules_map = {}
for name, options in (line.split(': ') for line in raw_rules.splitlines()):
    if options.startswith('"'):
        rules_map[name] = options.strip('"')
    else:
        rules_map[name] = tuple(tuple(i.split()) for i in options.split(' | '))


@lru_cache(maxsize=None)
def match_rule(message, rules_options, part=1):
    if type(rules_options) is tuple:  # nested rules
        ret = []
        for rules in rules_options:  # rules separated by "|"
            possible_messages = [message]
            for idx, rule_idx in enumerate(rules):
                if part == 2 and rule_idx in {'8', '11'}:
                    sub_rules = tuple()
                    new_possible_messages = []
                    while True:  # try all possible repetitions of rules
                        if rule_idx == '8':
                            sub_rules = ('42', *sub_rules)
                        else:
                            sub_rules = ('42', *sub_rules, '31')
                        len_before = len(new_possible_messages)
                        for message_ in possible_messages:
                            matching = match_rule(message_, (sub_rules,))
                            new_possible_messages.extend(matching)
                        if len_before == len(new_possible_messages):
                            break  # until we cannot apply any more
                    possible_messages = new_possible_messages

                else:
                    sub_rules = rules_map[rule_idx]
                    possible_messages = [
                        possible_message
                        for message_ in possible_messages
                        for possible_message in match_rule(message_, sub_rules)
                    ]

                # rules exhausted message before applying all of them
                if idx != len(rules) - 1:
                    possible_messages = list(filter(None, possible_messages))
                if not possible_messages:
                    break
            ret.extend(possible_messages)
        return ret

    # simple one char match
    return [message[1:]] if message[0] == rules_options else []


start = rules_map['0']
print(sum('' in match_rule(raw, start, 1) for raw in lines.splitlines()))
print(sum('' in match_rule(raw, start, 2) for raw in lines.splitlines()))
