"""
Day 22
"""
from typing import List

def convert(day_input: List[str]) -> List[List[int]]:
    res: List[List[int]] = [[], []]
    player = 0
    for line in day_input:
        if line == 'Player 1:': player = 0
        elif line == 'Player 2:': player = 1
        elif line == '': continue
        else: res[player].append(int(line))
    return res

def solve_part_one(day_input: List[str]) -> int:
    hands = convert(day_input)
    while (len(hands[0]) > 0 and len(hands[1]) > 0):
        # Popping from the front of a list is inneficient, but these are small
        p1, p2 = hands[0].pop(0), hands[1].pop(0)
        if p1 > p2:
            hands[0].extend([p1, p2])
        else:
            hands[1].extend([p2, p1])
    return sum((i + 1) * n for hand in hands if hand != [] for i, n in enumerate(reversed(hand)))

def play(hands: List[List[int]]) -> List[List[int]]:
    seen = set()
    while (len(hands[0]) > 0 and len(hands[1]) > 0):
        # Simple hash of the hands list, to check if it has been played
        h = tuple(sum(i * n for i, n in enumerate(hand)) for hand in hands)
        if h in seen: return [hands[0], []]
        seen.add(h)

        p1, p2 = hands[0].pop(0), hands[1].pop(0)
        if p1 <= len(hands[0]) and p2 <= len(hands[1]):
            # recurse to sub-game
            sub_hands = play([hands[0][:p1], hands[1][:p2]])
            winner = (len(sub_hands[0]) == 0)
        else:
            winner = (p1 < p2)
        hands[winner].extend([p1, p2] if winner == 0 else [p2, p1])
    return hands

def solve_part_two(day_input: List[str]) -> int:
    hands = play(convert(day_input))
    return sum((i + 1) * n for hand in hands if hand != [] for i, n in enumerate(reversed(hand)))
