"""
Day 14
"""
from typing import List, Iterator
from common import cat

def solve_part_one(day_input: List[str]) -> int:
    mem = dict()
    for line in day_input:
        # Strategy is to create 2 masks, mask1 with X replaced by 1 and mask2 with X replaced by 0
        # (arg & mask1) | mask2 = arg where mask had X ((arg & 1) | 0 = arg)
        # (arg & mask1) | mask2 = mask where mask didn't have X ((arg & m) | m = m)
        op, arg = line.split(' = ')
        if op == 'mask':
            mask1 = int(arg.replace('X', '1'), 2)
            mask2 = int(arg.replace('X', '0'), 2)
        elif op.startswith('mem'):
            addr = op[4:-1]
            mem[addr] = (int(arg) & mask1) | mask2
    return sum(mem.values())

def solve_part_two(day_input: List[str]) -> int:
    def mask_addresses(mask: str) -> Iterator[int]:
        """Returns all the possible addresses by substituting X by 0 and 1"""
        if mask.find('X') == -1:
            yield int(mask, 2)
        else:
            yield from mask_addresses(mask.replace('X', '0', 1))
            yield from mask_addresses(mask.replace('X', '1', 1))

    mem = dict()
    for line in day_input:
        op, arg = line.split(' = ')
        if op == 'mask':
            # Safeguard, don't accept more than 2^10 addresses to write
            if (arg.count('X') > 10): raise ValueError(f"An input with more than 2^10 possibilities was encountered: \n{line}")
            mask = arg
        elif op.startswith('mem'):
            # Strategy is to:
            # 1. create the address mask doing a manual *or*
            # 2. get all possible addresses and set them
            addr = f"{int(op[4:-1]):036b}"

            new_mask = [a if m == '0' else m for m, a in zip(mask, addr)]
            for m in mask_addresses(cat(new_mask)):
                mem[m] = int(arg)
    return sum(mem.values())
