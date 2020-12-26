"""
Day 21
"""
from typing import List, Tuple, Set, Dict
from common import flatten, cat

def convert(day_input: List[str]) -> List[Tuple[List[str], List[str]]]:
    res = []
    for line in day_input:
        ingr, alerg = line[:-1].split(' (contains ')
        res.append((ingr.split(), alerg.split(', ')))
    return res

def solve_part_one(day_input: List[str]) -> int:
    lst = convert(day_input)
    # Get all different ingredients and alergens
    ingredients = set(flatten(line[0] for line in lst))
    alergens = set(flatten(line[1] for line in lst))

    # Get ingredients possible for each alergen: for each alergen it's the union of ingredients
    # in which it appears
    alergen_ingredients: Dict[str, Set[str]] = \
        dict(zip(alergens, [set(ingredients) for _ in range(len(alergens))]))
    for line in lst:
        for alerg in line[1]:
            alergen_ingredients[alerg].intersection_update(line[0])

    # Good ingredients don't appear in the alergen list
    good_ingredients = [ingr for ingr in ingredients if ingr not in list(flatten(alergen_ingredients.values()))]
    res = sum(l[0].count(ingr) for l in lst for ingr in good_ingredients)
    return res

def solve_part_two(day_input: List[str]) -> str:
    lst = convert(day_input)
    # Same as part one, until getting the list of alergen possible ingredients
    ingredients = set(flatten(line[0] for line in lst))
    alergens = set(flatten(line[1] for line in lst))
    alergen_ingredients: Dict[str, Set[str]] = \
        dict(zip(alergens, [set(ingredients) for _ in range(len(alergens))]))

    for line in lst:
        for alerg in line[1]:
            alergen_ingredients[alerg].intersection_update(line[0])

    # Basic constraint propagation, again
    constraints = [alerg for alerg, ingr_lst in alergen_ingredients.items() if len(ingr_lst) == 1]
    while (len(constraints) > 0):
        alerg = constraints.pop()
        ingr = next(iter(alergen_ingredients[alerg]))
        for k, v in alergen_ingredients.items():
            if k != alerg and ingr in v:
                v.remove(ingr)
                if len(v) == 1: # New constraint
                    constraints.append(k)
    # Join the result. Lots of manipulations because the structure is somewhat complex
    return ','.join([next(iter(v)) for _, v in sorted(alergen_ingredients.items())])
