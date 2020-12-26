"""
Day 23
"""
from __future__ import annotations
from typing import List, Optional
from common import cat

def solve_part_one(day_input: List[str]) -> str:
    lst = [int(i) for i in day_input[0]]
    M, m = max(lst), min(lst)

    for _ in range(100):
        val = lst[0] - 1 if lst[0] > m else M
        while val in lst[1:4]:
            val = val - 1 if val > m else M
        idx = lst.index(val)
        lst = lst[4:idx+1] + lst[1:4] + lst[idx+1:] + lst[0:1]

    idx = lst.index(1)
    return cat(str(i) for i in lst[idx + 1:] + lst[0:idx])

class Cup:
    def __init__(self, n: int, next_cup: Optional[Cup] = None, prev_cup: Optional[Cup] = None):
        self.n = n
        self.next: Cup = next_cup #type: ignore
        self.prev: Cup = prev_cup #type: ignore
    
    def __repr__(self) -> str:
        return f"{self.n}" + f" -> {self.next.n if self.next is not None else 'null'}"
        # return f"{self.prev.n if self.prev is not None else 'null'} <- " + f"{self.n}" \
        #     f" -> {self.next.n if self.next is not None else 'null'}"
        # return f"{self.n} next: {self.next.n if self.next is not None else 'null'}" + \
        #     f" prev: {self.prev.n if self.prev is not None else 'null'}"

def print_lst(start):
    aux, s = start, ''
    while aux.next != start:
        s += ' ' + str(aux.n)
        aux = aux.next
    print(s + ' ' + str(aux.n))

def solve_part_two(day_input: List[str]) -> int:
    lst = [int(i) for i in day_input[0]]
    # it, n = 100, 9
    it, n = 10000000, 1000000

    # Build a double linked list
    cups = [Cup(i + 1) for i in range(n)]
    for i in range(n): cups[i].next, cups[i].prev = cups[(i + 1) % n], cups[(i - 1) % n]

    # Adjust indexes to make it easier to work, add end element to rotate/continue to next
    # and copy input list to cups list
    lst = [i - 1 for i in lst] + [lst[0] - 1 if n <= len(lst) else len(lst)]
    for i, _ in enumerate(lst[:-1]):
        cups[lst[i]].next = cups[lst[i + 1]]
    if n > len(lst): cups[-1].next = cups[lst[0]]

    # Make moves on the double linked list, slicing the next pointers
    curr = cups[lst[0]]
    for _ in range(it):
        removed = [curr.next, curr.next.next, curr.next.next.next]
        dest = curr.prev
        while dest in removed: dest = dest.prev
        curr.next = removed[-1].next
        removed[-1].next = dest.next
        dest.next = removed[0]
        curr = curr.next

    # print_lst(cups[lst[0]])
    return cups[0].next.n * cups[0].next.next.n
