"""
Day 10
"""
from typing import List
from itertools import chain, zip_longest
from functools import reduce
from common import diff

def solve_part_one(day_input: List[str]) -> int:
    # Sort numbers, take the diff and count jumps of 1 and 3 between them
    numbers = [0] + sorted(int(line) for line in day_input)
    d = diff(numbers)
    # Add 1 to to account for the last element which isn't included in the list
    return d.count(1) * (d.count(3) + 1)

def solve_part_two(day_input: List[str]) -> int:
    numbers = sorted(int(line) for line in day_input)

    # For each element in *numbers* count the paths that can lead to it, which are
    # the sum of the paths of the 3 previous elements
    paths = [1] + [0] * numbers[-1]
    for n in numbers:
        paths[n] = sum(paths[max(n-3, 0):n])
    return paths[-1]

    # Complicated version...
    # numbers = [0] + numbers + [numbers[-1] + 3]
    # d1, d2, d3 = diff(numbers, 1), diff(numbers, 2), diff(numbers, 3)
    # max_dist = 3
    # reachable = [(a <= max_dist) + (b <= max_dist) + (c <= max_dist) for a, b, c in zip_longest(d1, d2, d3, fillvalue=max_dist+1)]
    # paths = [1] + [0] * (len(reachable) - 1)
    # for i, v in enumerate(reachable[:-1]):
    #     for j in range(v):
    #         paths[i+j+1] += paths[i]
    # return paths[-1]
