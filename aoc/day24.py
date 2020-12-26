"""
Day 24
"""
from __future__ import annotations
from typing import List, Set, NamedTuple, Tuple, Iterable
#from common import Position

# Tuple to represent a position with + and - ops
class Position(NamedTuple):  # pylint: disable=inherit-non-class
    x: int
    y: int

    def __add__(self, other: Position) -> Position: #type: ignore
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Position) -> Position:
        return Position(self.x - other.x, self.y - other.y)

def convert(day_input: List[str]) -> List[List[str]]:
    """Breaks down the input into a list of directions for each tile"""
    def dirs(line: str) -> List[str]:
        dirs, last_c = [], ''
        for c in line:
            if c in ['e', 'w']:
                dirs.append(last_c + c)
                last_c = ''
            else:
                last_c = c
        return dirs

    return [dirs(line) for line in day_input]

# Position changes for each direction
moves = {\
    'e': Position(2, 0), \
    'ne': Position(1, 1), \
    'nw': Position(-1, 1), \
    'w': Position(-2, 0), \
    'sw': Position(-1, -1), \
    'se': Position(1, -1), \
}

def black_tiles(tiles: List[List[str]]) -> Set[Position]:
    """Returns the set of tiles that are black after placing them according to the specs"""
    floor: Set[Position] = set()
    for tile in tiles:
        start = Position(0, 0)
        for step in tile:
            start += moves[step]
        if start in floor:
            floor.remove(start)
        else:
            floor.add(start)
    return floor

def solve_part_one(day_input: List[str]) -> int:
    tiles = convert(day_input)
    return len(black_tiles(tiles))

def solve_part_two(day_input: List[str]) -> int:
    def neighbours(tile: Position) -> Iterable:
        return (tile + moves[move] for move in moves)

    tiles = convert(day_input)
    blacks = black_tiles(tiles)
    for _ in range(100):
        # For black pieces, check which remain black, and at the same time, 
        # keep the set of their white neighbours for the next step
        frontier_whites: Set[Position] = set()
        remain_blacks = set()
        for tile in blacks:
            white_neighbours = [t for t in neighbours(tile) if t not in blacks]
            if len(white_neighbours) == 4 or len(white_neighbours) == 5:
                remain_blacks.add(tile)
            frontier_whites.update(white_neighbours)

        # For the whites near blacks, check which should turn
        fliped_whites = set()
        for tile in frontier_whites:
            black_neighbours = [t for t in neighbours(tile) if t in blacks]
            if len(black_neighbours) == 2:
                fliped_whites.add(tile)
        blacks = remain_blacks | fliped_whites
    return len(blacks)
