"""
Day 19
"""
from typing import List, Tuple, Dict

Rules = Dict[str, List[List[str]]]
def convert(day_input: List[str]) -> Tuple[Rules, List[str]]:
    """Returns a dict with the rules, and the message list.
    dict[rule] is a List containing the alternatives for the rule
    dict[rule][idx] is one of the sequences allowed for the rule
    """
    iter_in = iter(day_input)
    rules = {}
    for line in iter_in:
        if line == '': break
        key, vals = line.split(': ')
        rules[key] = [[k.replace('"', '') for k in r.split()] for r in vals.split(' | ')]
    messages = list(iter_in)
    return (rules, messages)

def match(rules: Rules, rule_id: str, message: str) -> List[int]:
    """Returns how many characters are possible to match in *message* starting from *rule_id*.
    If none can be matched, returns the empty list, otherwise, returns a list of possibilities, 
    as there can be several alternatives."""
    rule = rules[rule_id]

    # Final token, check if its an 'a' or a 'b' and return [1] or []
    if len(rule) == 1 and len(rule[0]) == 1 and rule[0][0] in ['a', 'b']:
        return [1] if rule[0][0] == message[0] else []

    # Alternative, match each one individually and return how many were matched on each. 
    # Each sub-rule is separately put on the dict rules to facilitate reusing the *match* function
    if len(rule) > 1:
        matched = []
        for i, sub_rule in enumerate(rule):
            sub_id = f'{rule_id}_{i}'
            rules[sub_id] = [sub_rule]
            matched += match(rules, sub_id, message)
        return matched
    
    # Sequence, match each token sequentially, keeping track of how many characters were matched
    # on each match, accumulating them as we apply the rules. 
    # Care must be taken because each `match` can return more than one possibility.
    if len(rule) == 1:
        matched = [0]
        for r in rule[0]:
            # Matching a new rule, discard matches that have matched the whole string already
            valid_matched = filter(lambda i: i < len(message), matched)
            matched = [i + j for i in valid_matched for j in match(rules, r, message[i:]) ]
        return matched
    return []

def solve_part_one(day_input: List[str]) -> int:
    rules, messages = convert(day_input)

    count = 0
    for m in messages:
        matched = match(rules, '0', m)
        if len(matched) > 0 and matched[0] == len(m):
            count += 1

    return count

def solve_part_two(day_input: List[str]) -> int:
    rules, messages = convert(day_input)
    rules['8'] = [['42'], ['42', '8']]
    rules['11'] = [['42', '31'], ['42', '11', '31']]
    count = 0
    for m in messages:
        matched = match(rules, '0', m)
        if len(matched) > 0 and matched[0] == len(m):
            count += 1

    return count
