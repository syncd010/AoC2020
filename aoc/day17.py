"""
Day 17
"""
from typing import List, Dict, Tuple
from common import Position, cat

def convert(day_input: List[str]) -> List[Position]:
    """Converts a board into a list of Positions"""
    active = [Position(x, y, 0) \
        for y, line in enumerate(day_input) \
            for x, c in enumerate(line) \
                if c == '#']
    return active

def get_boundaries(active: List[Position]) -> Dict[str, Tuple[int, int]]:
    """Returns the boundaries + 1 of each dimension (min - 1, max + 2 on each dimension)"""
    boundaries = {}
    boundaries['x'] = (min(p.x for p in active) - 1, max(p.x for p in active) + 2)
    boundaries['y'] = (min(p.y for p in active) - 1, max(p.y for p in active) + 2)
    boundaries['z'] = (min(p.z for p in active) - 1, max(p.z for p in active) + 2)
    boundaries['w'] = (min(p.w for p in active) - 1, max(p.w for p in active) + 2)
    return boundaries

def display(board: List[Position]):
    """Displays a board"""
    boundaries = get_boundaries(board)
    for w in range(*boundaries['w']):
        for z in range(*boundaries['z']):
            print(f'z={z}, w={w}')
            for y in range(*boundaries['y']):
                line = ['.'] * (boundaries['x'][1] - boundaries['x'][0])
                for p in board:
                    if p.z == z and p.y == y:
                        line[p.x - boundaries['x'][0]] = '#'
                print(cat(line))

def evolve(active: List[Position], ndims: int = 4) -> List[Position]:
    """Evolves the board for 1 epoch. *ndims* can be 2, 3 or 4"""
    # Update the boundaries to add +2 positions on each dimension
    boundaries = get_boundaries(active)
    # Ignore higher dims than ndims
    if ndims <= 3: boundaries['w'] = (0, 1)
    if ndims <= 2: boundaries['z'] = (0, 1)

    new_active: List[Position] = []
    # Check each position of the board, and on each dimension filter the active elements 
    # to only consider those that within dist 1 on that dimension, therefore
    # significantly reducing the number of active elements to check
    for x in range(*boundaries['x']):
        near_x = [p for p in active if abs(p.x - x) <= 1]
        for y in range(*boundaries['y']):
            near_y = [p for p in near_x if abs(p.y - y) <= 1]
            for z in range(*boundaries['z']):
                near_z = [p for p in near_y if abs(p.z - z) <= 1]
                for w in range(*boundaries['w']):
                    pos = Position(x, y, z, w)
                    is_active = pos in near_z
                    # Filter again on this dim to get the cound of neighbors iin all dims
                    # Subtract 1 if this position is active, as it was also counted 
                    count = len([p for p in near_z if abs(p.w - w) <= 1]) - int(is_active)
                    if (is_active and (count == 2 or count == 3)) or (not is_active and count == 3):
                        new_active.append(pos)
    return new_active

def solve_part_one(day_input: List[str]) -> int:
    active = convert(day_input)
    for _ in range(6):
        active = evolve(active, ndims=3)
    return len(active)

def solve_part_two(day_input: List[str]) -> int:
    active = convert(day_input)
    for _ in range(6):
        active = evolve(active, ndims=4)
    return len(active)

# def solve_part_one(day_input: List[str]) -> int:
#     active = convert(day_input)
#     for _ in range(6):
#         # Update the boundaries to add +2 positions on each dimension
#         boundaries = get_boundaries(active)
#         new_active: List[Position] = []
#         # Check each position of the board
#         for x in range(*boundaries['x']):
#             for y in range(*boundaries['y']):
#                 for z in range(*boundaries['z']):
#                     # Sum all active positions that are within dist 1 of this position, for all dimensions
#                     # Subtract 1 if this position is active, as it was also counted 
#                     pos = Position(x, y, z)
#                     is_active = pos in active
#                     count = sum(1 for a in active \
#                         if abs(pos.x - a.x) <= 1 and abs(pos.y - a.y) <= 1 and abs(pos.z - a.z) <= 1) \
#                             - int(is_active)
#                     # Apply the rules
#                     if (is_active and (count == 2 or count == 3)) or \
#                         (not is_active and count == 3):
#                         new_active.append(pos)
#         # Swap
#         active = new_active
#     return len(active)
