"""
Day 5
"""
from typing import List, Tuple, Iterator

def convert(day_input: List[str]) -> Iterator[Tuple[int, int]]:
    # Converts the input to list of (row, column). Each row has
    # first 7 digits specifying the row in bynary, after substituting B by 1 and F by 0
    # last 3 digits specifying the column in bynary, after substituting R by 1 and L by 0
    return ((int(row[:7].replace('F', '0').replace('B', '1'), 2), int(row[7:].replace('L', '0').replace('R', '1'), 2)) for row in day_input)

def solve_part_one(day_input: List[str]) -> int:
    seats = (r*8 + c for r,c in convert(day_input))
    # Just get the max
    return max(seats)

def solve_part_two(day_input: List[str]) -> int:
    seats = sorted(r*8 + c for r,c in convert(day_input))
    # Find a discontinuity
    for i, s in enumerate(seats[:-1]):
        if (seats[i+1] - s > 1):
            return s+1

    return 0
