"""
Day 6
"""
from typing import List, Set

def solve_part_one(day_input: List[str]) -> int:
    # Split input for each group - delimited by an empty line - and for each
    # group make a set that will contain the unique elements
    answers: List[Set[str]] = [set()]
    for line in day_input:
        if line == '':
            answers.append(set())
        else:
            answers[-1].update(list(line))
    res = sum(len(s) for s in answers)
    return res

def solve_part_two(day_input: List[str]) -> int:
    # Split input for each group - delimited by an empty line - and for each
    # group make a set with the intersection of the elements in each line
    answers: List[Set[str]] = [set()]
    new_group: bool = True
    for line in day_input:
        if line == '':
            new_group = True
        else:
            if new_group:
                answers.append(set(list(line)))
            else:
                answers[-1].intersection_update(list(line))
            new_group = False
    res = sum(len(s) for s in answers)
    return res
