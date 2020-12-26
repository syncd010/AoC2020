import math
from typing import List

def count_colisions(area_map: List[str], right_cnt: int, down_cnt: int) -> int:
    # Traverse area_map, starting from (0,0) with step (down, right), counting
    # the positions that are marked with #
    height, width = len(area_map), len(area_map[0])
    pos = ((i*down_cnt, i*right_cnt) for i in range(height) if i*down_cnt < height)
    count = sum(area_map[p[0]][p[1]%width] == '#' for p in pos)
    return count

def solve_part_one(day_input: List[str]) -> int:
    return count_colisions(day_input, 3, 1)

def solve_part_two(day_input: List[str]) -> int:
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    counts = (count_colisions(day_input, *slope) for slope in slopes)
    return math.prod(counts)
