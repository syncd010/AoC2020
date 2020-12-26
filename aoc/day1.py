from typing import List

def convert(day_input: List[str]) -> List[int]:
    return list(map(int, day_input))

def solve_part_one(day_input: List[str]) -> int:
    numbers = convert(day_input)

    for i, a in enumerate(numbers):
        for b in numbers[i:]:
            if a+b == 2020:
                return a*b

    return -1

def solve_part_two(day_input: List[str]) -> int:
    numbers = convert(day_input)

    for i, a in enumerate(numbers):
        for j, b in enumerate(numbers[i:]):
            for c in numbers[j:]:
                if a+b+c == 2020:
                    return a*b*c

    return -1
