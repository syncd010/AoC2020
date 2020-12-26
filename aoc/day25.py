"""
Day 25
"""
from typing import List

def get_loop_size(key: int, sn:int) -> int:
    i, val = 1, 1
    while True:
        val = (val * sn) % 20201227
        if val == key: break
        i += 1
    return i

def transform(sn: int, loop_size: int) -> int:
    val = 1
    for _ in range(loop_size):
        val = (val * sn) % 20201227
    return val

def solve_part_one(day_input: List[str]) -> int:
    keys = [int(line) for line in day_input]
    return transform(keys[1], get_loop_size(keys[0], 7))

def solve_part_two(day_input: List[str]) -> int:
    return 0
