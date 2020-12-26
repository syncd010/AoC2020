"""
Day 13
"""
from typing import List
from math import ceil

def solve_part_one(day_input: List[str]) -> int:
    min_time = int(day_input[0])
    nums = [int(n) for n in day_input[1].split(',') if n != 'x']

    # Just find the min number that is greater than min_time
    times = [ceil(min_time/n) * n for n in nums]
    min_idx = times.index(min(times))
    return (times[min_idx] - min_time) * nums[min_idx]

def solve_part_two(day_input: List[str]) -> int:
    # Use Chinese remainder theorem https://en.wikipedia.org/wiki/Chinese_remainder_theorem
    # Search solution by sieving
    nums = ((i, int(n)) for i, n in enumerate(day_input[1].split(',')) if n != 'x')
    # Calculate the remainder to consider in the first tuple position, and sort by step to make 
    # the search faster
    nums_dsc = sorted((((n - i) % n, n) for i, n in nums), key=lambda x: x[1], reverse=True)
    a1 = nums_dsc[0][0]
    n1 = nums_dsc[0][1]
    for a2, n2 in nums_dsc[1:]:
        i = 0
        while (a1 + n1 * i) % n2 != a2:
            i += 1
        a1 = a1 + n1 * i
        n1 *= n2

    return a1
