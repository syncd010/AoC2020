"""
Day 16
"""
from __future__ import annotations
from typing import List, Tuple, Dict, NamedTuple, Callable, Optional
from functools import reduce
from collections import defaultdict
from math import prod
from common import flatten

def convert(day_input: List[str]) -> Tuple[Dict[str, List[range]], List[int], List[List[int]]]:
    """Converts the input into a tuple with:
    1. A dictionary with the fields, where for each field the value is a list
    of the valid ranges, each represented as a tuple with the min and max value
    2. The values for your ticket, a list of ints
    3. A list with the values for the other tickets"""
    iter_in = iter(day_input)
    # Convert fields
    fields = {}
    for line in iter_in:
        if line == '': break
        key, vals = line.split(': ')
        fields[key] = [range(int(v.split('-')[0]), int(v.split('-')[1]) + 1 ) for v in vals.split(' or ')]

    while next(iter_in) != 'your ticket:':
        continue
    our = [int(n) for n in next(iter_in).split(',')]

    while next(iter_in) != 'nearby tickets:':
        continue
    tickets = [[int(n) for n in line.split(',')] for line in iter_in]
    return (fields, our, tickets)

def solve_part_one(day_input: List[str]) -> int:
    fields, _, tickets = convert(day_input)

    # Invalid numbers aren't in any of the ranges
    all_ranges = list(flatten(fields.values()))
    res = (n for n in flatten(tickets) if not any(n in r for r in all_ranges))
    return sum(res)

def solve_part_two(day_input: List[str]) -> int:
    fields, ours, tickets = convert(day_input)

    # Valid tickets have all their numbers in at least one range
    all_ranges = list(flatten(fields.values()))
    valid_tickets = [t for t in tickets if all(any(n in r for r in all_ranges) for n in t)]

    # For each field collect which positions are possible for it
    possible: Dict[str, List[int]] = defaultdict(list)
    for field, ranges in fields.items():
        # This could be done in a single list comprehension but would be unreadable
        for pos in range(len(ours)):
            # if all ticket values in this position are in at least one of the ranges of the field,
            # this position is possible for the field
            vals = [t[pos] for t in valid_tickets]
            if all(any(v in r for r in ranges) for v in vals):
                possible[field].append(pos)

    # Basic constraint propagation, doesn't work in all scenarios, only well behaved ones
    constraints = [field for field, pos in possible.items() if len(pos) == 1]
    while len(constraints) > 0:
        constr = constraints.pop()
        pos = possible[constr][0]
        for k, v in possible.items():
            if k != constr and pos in v:
                v.remove(pos)
                if len(v) == 1:
                    # New constraint
                    constraints.append(k)
    # Assuming that the previous constraint propagation uniquely defined the fields...
    res = (ours[pos] for pos in ([v[0] for k, v in possible.items() if k.startswith("departure")]))
    return prod(res)
