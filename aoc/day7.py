"""
Day 7
"""
from typing import List, Dict, Tuple
import re

def convert(day_input: List[str]) -> Dict[str, List[Tuple[int, str]]]:
    """Converts the input to a dict mapping each key to a list of its contents,
    where each content element is represented as a tuple of quantity and element"""
    d: Dict[str, List[Tuple[int, str]]] = dict()
    for line in day_input:
        # Remove all superfluous text and split the spec
        spec_split = re.sub(r" bags?|\.", "", line).split(" contain ")
        key = spec_split[0]
        d[key] = []
        for elem in spec_split[1].split(", "):
            elem_split = elem.split(" ", 1)
            if (elem_split[0].isnumeric()):
                d[key].append((int(elem_split[0]), elem_split[1]))
    return d

def invert_dict(orig: Dict[str, List[Tuple[int, str]]]) -> Dict[str, List[str]]:
    """Inverts the dict returned in convert: values to keys and keys to values.
    The original values is a list of tuples, each of them transformed to a key
    in the result. The key used is the second element of the tuple."""
    dest = dict()
    # For each element in the dictionary, collect all the keys where in
    # which that element is present in the dict values
    for elem in orig:
        dest[elem] = [k for k, v in orig.items() if elem in [tup[1] for tup in v]]
    return dest

def solve_part_one(day_input: List[str]) -> int:
    d = invert_dict(convert(day_input))
    # Traverse the inversed dict from the starting point, collecting the unique nodes seen
    frontier = ["shiny gold"]
    unique = set()
    while len(frontier) > 0:
        new = d[frontier.pop()]
        frontier += new
        unique.update(new)
    return len(unique)

def solve_part_two(day_input: List[str]) -> int:
    d = convert(day_input)
    # Traverse the dict summing up the nodes
    frontier = [(1, "shiny gold")]
    count = 0
    while len(frontier) > 0:
        current = frontier.pop()
        new = d[current[1]]
        frontier += [(current[0] * e[0], e[1]) for e in new]
        count += sum(current[0] * e[0] for e in new)
    return count
