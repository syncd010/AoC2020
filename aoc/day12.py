"""
Day 12
"""
from typing import List, Tuple
from common import Position, manhattan_dist

def convert(day_input: List[str]) -> List[Tuple[str, int]]:
    return [(l[0], int(l[1:])) for l in day_input]

def solve_part_one(day_input: List[str]) -> int:
    pos = Position(0,0)
    facing = 'E'
    # Steps to take for each direction
    dirmap = {'N': Position(0, 1), 'S': Position(0, -1), 'E': Position(1, 0), 'W': Position(-1, 0)}
    rotations = ['N', 'E', 'S', 'W']

    for inst in convert(day_input):
        if inst[0] in dirmap: # N,S,E,W
            pos += dirmap[inst[0]] * inst[1]
        elif inst[0] == 'F': # Move in the facing direction
            pos += dirmap[facing] * inst[1]
        else: # Rotate L or R, only works for multiples of 90 degrees
            turns = inst[1] // 90
            d = 1 if inst[0] == 'R' else -1
            # Rotate in the rotation array Left or Right
            facing = rotations[(rotations.index(facing) + d*turns) % len(rotations)]

    return manhattan_dist(pos)

def solve_part_two(day_input: List[str]) -> int:
    pos = Position(0,0)
    waypoint = Position(10, 1)
    dirmap = {'N': Position(0, 1), 'S': Position(0, -1), 'E': Position(1, 0), 'W': Position(-1, 0)}

    for inst in convert(day_input):
        if inst[0] in dirmap: # N,S,E,W, move the waypoint
            waypoint += dirmap[inst[0]] * inst[1]
        elif inst[0] == 'F': # Move in the waypoint direction
            pos += waypoint * inst[1]
        else: # Rotate
            turns = inst[1] // 90
            d = 1 if inst[0] == 'R' else -1
            # Move the waypoint around: R, change (x, y) to (y, -x); L, change (x, y) to (-y, x)
            for _ in range(turns):
                waypoint.x, waypoint.y = d * waypoint.y, -d * waypoint.x

    return manhattan_dist(pos)
