"""
Day Template
"""
from typing import List
from itertools import accumulate

def solve_part_one(day_input: List[str]) -> int:
    def is_sum(num: int, numbers: List[int]) -> bool:
        """Returns whether `num` is a sum of 2 numbers in the given list"""
        for first in numbers[: -1]:
            for second in numbers[1:]:
                if first + second == num:
                    return True
        return False

    numbers = [int(line) for line in day_input]
    preamble = 25 if len(numbers) > 25 else 5

    # Finds the number in the list which is not a sum of 2 numbers 
    # in the previous `preamble` numbers
    for i in range(preamble, len(numbers)):
        if not is_sum(numbers[i], numbers[i - preamble: i]):
            return numbers[i]
    return -1

def solve_part_two(day_input: List[str]) -> int:
    num = solve_part_one(day_input)
    numbers = [int(line) for line in day_input]

    # Find contiguous numbers that add up to `num`
    for start, _ in enumerate(numbers):
        for end, acc in enumerate(accumulate(numbers[start:])):
            if acc == num:
                return min(numbers[start:start+end+1]) + max(numbers[start:start+end+1])
            elif acc > num:
                # No need to continue, go on to the next start number
                break

    return -1