"""
Day 2
"""
from typing import List
from functools import reduce

def convert(day_input: List[str]) -> List[List[str]]:
    # Split the string on all separators
    return [line.replace('-', ' ').replace(':', ' ').split() for line in day_input]

def solve_part_one(day_input: List[str]) -> int:
    def reduce_func(c: int, line) -> int:
        count = line[3].count(line[2])
        return c + (count >= int(line[0]) and count <= int(line[1]))

    return reduce(reduce_func, convert(day_input), 0)

def solve_part_two(day_input: List[str]) -> int:
    def reduce_func(c: int, line) -> int:
        count = int(line[3][int(line[0])-1] == line[2]) + int(line[3][int(line[1])-1] == line[2])
        return c + (count == 1)

    return reduce(reduce_func, convert(day_input), 0)
