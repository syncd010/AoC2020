"""
Day 4
"""
from typing import List, Dict
from functools import reduce

def convert(day_input: List[str]) -> List[Dict[str, str]]:
    # Return a Dict for each passport with its attributes
    res: List[Dict[str, str]] = [{}]
    for line in day_input:
        if line == '':
            res.append({})
        else:
            res[-1].update({attr.split(':')[0]: attr.split(':')[1] for attr in line.split()})
    return res

def solve_part_one(day_input: List[str]) -> int:
    passports = convert(day_input)
    attrs = 'byr iyr eyr hgt hcl ecl pid'.split() # ignore cid

    # All present?
    valid = (all(attr in passport for attr in attrs) for passport in passports)
    return sum(valid)

def solve_part_two(day_input: List[str]) -> int:
    def is_valid(attr: str, value: str) -> bool:
        # Ranges for various numeric attrs
        ranges = {'byr': (1920, 2002), 'iyr': (2010, 2020), 'eyr': (2020, 2030), 'hgtcm': (150, 193), 'hgtin': (59, 76)}
        # Transform hgt attr, appending cm or in to it so that it can be treated like the other
        if attr == 'hgt':
            attr += value[-2:]
            value = value[:-2]

        valid: bool = False
        # Rules
        if attr in ranges:
            valid = value.isnumeric() and int(value) >= ranges[attr][0] and int(value) <= ranges[attr][1]
        elif attr == 'hcl':
            hex = '0 1 2 3 4 5 6 7 8 9 a b c d e f'.split()
            valid = value[0] == '#' and all(v in hex for v in value[1:])
        elif attr == 'ecl':
            valid = value in 'amb blu brn gry grn hzl oth'.split()
        elif attr == 'pid':
            valid = len(value) == 9 and value.isnumeric()

        return valid

    passports = convert(day_input)
    attrs = 'byr iyr eyr hgt hcl ecl pid'.split() # less cid
    # All present and valid?
    valid = (all(attr in passport and is_valid(attr, passport[attr]) for attr in attrs) for passport in passports)
    return sum(valid)
