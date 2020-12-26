"""
Day 11
"""
from typing import List, Tuple, Callable
from itertools import product

def evolve_until_stationary(layout: List[str], change_rule: Callable[[str, int], str], floor_is_empty: bool = True) -> List[str]:
    """Evolves *layout* applying *change_rule* to each position, until no more changes are made. 
    *floor_is_empty* controls wether to consider the flor as an empty position or ignore it"""
    def count_occupied(board: List[List[str]], pos: Tuple[int, int], floor_is_empty: bool) -> int:
        # Assumes that layout has a border around it, and pos is in (1..len(board)-1)
        count = 0
        for y in (-1, 0, 1):
            for x in (-1, 0, 1):
                aux_pos = [y + pos[0], x + pos[1]]
                # If floor isn't considered empty, search the first non-empty 
                # in the direction. Ignore dir (0,0) - shouldn't be necessary but...
                if not floor_is_empty and not (x == 0 and y == 0) :
                    while board[aux_pos[0]][aux_pos[1]] == '.':
                        aux_pos[0] += y
                        aux_pos[1] += x
                count += (board[aux_pos[0]][aux_pos[1]] == '#')
        # We conted our own position, so subtract it here
        return count - (board[pos[0]][pos[1]] == '#')

    # Add a border around the input to ignore index safety later
    board = [['L'] + list(line) + ['L'] for line in layout]
    board.insert(0, ['L'] * (len(layout[0]) + 2))
    board.append(['L'] * (len(layout[0]) + 2))

    new_board = [l[:] for l in board]
    while True:
        changes = 0
        # Loop only over the input, ignoring the border
        for y, line in enumerate(board[1:-1], start=1):
            for x, state in enumerate(line[1:-1], start=1):
                if state == '.': continue
                occupied = count_occupied(board, (y, x), floor_is_empty)
                state = change_rule(state, occupied)
                changes += (state != new_board[y][x])
                new_board[y][x] = state
        # switch
        board, new_board = new_board, board
        if changes == 0: break

    return [''.join(line[1:-1]) for line in board[1:-1]]


def solve_part_one(day_input: List[str]) -> int:
    def rule(state: str, occupied: int) -> str:
        if state == 'L' and occupied == 0:
            state = '#'
        elif state == '#' and occupied >= 4:
            state = 'L'
        return state

    layout = evolve_until_stationary(day_input, rule)
    #print('\n'.join(''.join(line) for line in layout))
    return sum(state == '#' for line in layout for state in line)

def solve_part_two(day_input: List[str]) -> int:
    def rule(state: str, occupied: int) -> str:
        if state == 'L' and occupied == 0:
            state = '#'
        elif state == '#' and occupied >= 5:
            state = 'L'
        return state

    layout = evolve_until_stationary(day_input, rule, False)
    #print('\n'.join(''.join(line) for line in layout))
    return sum(state == '#' for line in layout for state in line)
