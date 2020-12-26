from __future__ import annotations
import time
import math
import functools
import itertools as it
from typing import Iterable, Any, Callable, List, Sequence, Dict, Optional, ClassVar, \
    NamedTuple, Optional
from dataclasses import dataclass

"""String join"""
cat = ''.join

"""List of lists flattening"""
flatten = it.chain.from_iterable

def str_replace(s: str, old: List[str], new: Optional[List[str]] = None) -> str:
    """Replaces occurences of all strings in *old* by the corresponding ones in *new*.
    If None is passed in new, *old* are simply removed fromm *s*"""
    if new is None: new = [''] * len(old)
    for o, n in zip(old, new):
        s = s.replace(o, n)
    return s

class TimedValue(NamedTuple):  # pylint: disable=inherit-non-class
    value: Any
    elapsed_time: float

def timed(func):
    """Timer decorator to time a function.

    Wraps the return value in a ``NamedTuple`` with the return value in *value* and 
    the elapsed time in *elapsed_time*"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        return TimedValue(value, toc - tic)

    return wrapper

# Copied and adapted from more_itertools
def split_at(it: Iterable[Any], pred: Callable[[Any], bool]) -> Iterable[Any]:
    """Yield lists of items from *iterable*, where each list is delimited by
    an item where callable *pred* returns ``True``.

        >>> list(split_at('abcdcba', lambda x: x == 'b'))
        [['a'], ['c', 'd', 'c'], ['a']]

        >>> list(split_at(range(10), lambda n: n % 2 == 1))
        [[0], [2], [4], [6], [8], []]
    """
    buf: List[Any] = []
    for item in iter(it):
        if pred(item):
            yield buf
            buf = []
        else:
            buf.append(item)
    if len(buf) > 0:
        yield buf

# def diff(iterable: Iterable[int]) -> Iterable[int]:
#     """Yields the difference of the elements in *iterable*"""
#     it = iter(iterable)
#     a = next(it)
#     for b in it:
#         yield b - a
#         a = b

def diff(seq: Sequence[int], n: int = 1) -> Sequence[int]:
    """Returns the difference between the *nth* elements of *seq*"""
    if len(seq) <= n:
        raise ValueError(f"Sequence length must be more than {n}")
    
    return [b - a for a, b in zip(seq[:-n], seq[n:])]

@dataclass
class Position:
    """Represents a position in 1D, 2D, 3D or 4D space"""
    x: int
    y: int = 0
    z: int = 0
    w: int = 0

    def __add__(self, other: Position) -> Position:
        return Position(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def __iadd__(self, other: Position) -> Position:
        self.x += other.x
        self.y += other.y
        self.z += other.z
        self.w += other.w
        return self

    def __sub__(self, other: Position) -> Position:
        return Position(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)

    def __isub__(self, other: Position) -> Position:
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        self.w -= other.w
        return self

    def __mul__(self, other: int) -> Position:
        return Position(self.x * other, self.y * other, self.z * other, self.w * other)

    def __imul__(self, other: int) -> Position:
        self.x *= other
        self.y *= other
        self.z *= other
        self.w *= other
        return self

def manhattan_dist(pos1: Position, pos2: Position = Position(0, 0, 0, 0)) -> int:
    """Manhattan distance between *pos1* and *pos2*"""
    return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y) + abs(pos1.z - pos2.z) + abs(pos1.w - pos2.w)
