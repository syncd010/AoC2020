"""
Day 15
"""
from typing import List
from collections import defaultdict

def solve_part_one(day_input: List[str]) -> int:
    numbers = [int(n) for n in day_input[0].split(',')]

    # Brute-force, inneficient version, just search on numbers the last time seen
    start = len(numbers)
    end = 2020
    numbers += [0] * (end - start)
    for i in range(start, end):
        for j in range(i - 2, -1, -1):
            if numbers[j] == numbers[i - 1]:
                numbers[i] = i - j - 1
                break
    return numbers[-1]

def solve_part_two(day_input: List[str]) -> int:
    numbers = [int(n) for n in day_input[0].split(',')]

    # More efficient version, use a dictionary to store the last time seen
    seen = {n : i for i, n in enumerate(numbers[:-1])}
    #end = 2020
    end = 30000000
    last = numbers[-1]
    for i in range(len(numbers) - 1, end - 1):
        seen[last], last = i, i - seen[last] if last in seen else 0

    return last
