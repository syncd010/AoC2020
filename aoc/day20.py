"""
Day 20
"""
from typing import List, Dict, Tuple, Optional
from math import prod, sqrt
from enum import Enum
from common import str_replace, cat, flatten, Position

def reverse_int_bits(n: int, n_bits: int = 10) -> int:
    """Reverses the bits of *n*, considering it is padded by *n_bits* first"""
    return int(format(n, '0' + str(n_bits) + 'b')[::-1], 2)

class Tile:
    # Indexes of edge ids
    LEFT, TOP, RIGHT, BOTTOM = 0, 1, 2, 3
    # Operations on tiles
    ROTATE, FLIP = 1, 2

    """Represents a tile, with its key, image and edge ids"""
    def __init__(self, key: str, img: List[str]):
        self.key = key
        self.img = img
        self.stored_ops: List[int] = []

        # Store edge as ids to speed up later matches. Convert to binary, read clockwise
        def edge_to_int(s: str) -> int:
            return int(str_replace(s, ['.', '#'], ['1', '0']), 2)
        top, bottom = img[0], img[-1][::-1]
        right, left = cat([l[-1] for l in img]), cat([l[0] for l in img])[::-1]
        self.edges = [edge_to_int(side) for side in [left, top, right, bottom]]
    
    def __repr__(self):
        # return f"Tile: {self.key} Edges: {self.edges} | {self.edges_reversed()}"
        return f"Tile {self.key}"

    def __eq__(self, other):
        return self.key == other.key

    def edges_reversed(self) -> List[int]:
        """Edges with bits reversed"""
        return [reverse_int_bits(n) for n in self.edges]

    def is_compatible(self, other_left: Optional[int], other_top: Optional[int]) -> Optional[List[int]]:
        """Returns the sequence of operations that make this tile compatible with the
        passed edges (on the left and top). Returns None if it is not compatible"""
        if other_left is None and other_top is None: # No constraints
            return []

        edges_rev = self.edges_reversed()
        def equal(other_edge: Optional[int], edge: int) -> bool:
            return other_edge is None or other_edge == edge

        if equal(other_left, edges_rev[Tile.LEFT]) and equal(other_top, edges_rev[Tile.TOP]):
            return []
        if equal(other_left, edges_rev[Tile.TOP]) and equal(other_top, edges_rev[Tile.RIGHT]):
            return [Tile.ROTATE] * 3
        if equal(other_left, edges_rev[Tile.RIGHT]) and equal(other_top, edges_rev[Tile.BOTTOM]):
            return [Tile.ROTATE] * 2
        if equal(other_left, edges_rev[Tile.BOTTOM]) and equal(other_top, edges_rev[Tile.LEFT]):
            return [Tile.ROTATE]

        if equal(other_left, self.edges[Tile.TOP]) and equal(other_top, self.edges[Tile.LEFT]):
            return [Tile.ROTATE, Tile.FLIP]
        if equal(other_left, self.edges[Tile.RIGHT]) and equal(other_top, self.edges[Tile.TOP]):
            return [Tile.FLIP]
        if equal(other_left, self.edges[Tile.BOTTOM]) and equal(other_top, self.edges[Tile.RIGHT]):
            return [Tile.FLIP, Tile.ROTATE]
        if equal(other_left, self.edges[Tile.LEFT]) and equal(other_top, self.edges[Tile.BOTTOM]):
            return [Tile.FLIP, Tile.ROTATE, Tile.ROTATE]

        return None

    def img_no_border(self):
        return [l[1:-1] for l in self.img[1:-1]]

def convert(day_input: List[str]) -> List[Tile]:
    tiles, key, img = [], '', []
    for line in day_input:
        if line.startswith('Tile'):
            key = str_replace(line, ['Tile ', ':'], None)
        elif line != '':
            img.append(line)
        else: # End of image
            tiles.append(Tile(key, img))
            img = []
    # If no empty line at EOF, last tile wasn't appended
    if img != []:
        tiles.append(Tile(key, img))
    return tiles

def solve_part_one(day_input: List[str]) -> int:
    tiles = convert(day_input)
    # Get all tiles that have 2 edges not compatible with any others
    # This is not a necessary condition for a tile to be in a corner, but it is a sufficient
    # one (a tile with 2 edges not compatible with others must be in a corner)
    corners = []
    for tile in tiles:
        other_edges = list(flatten([other.edges + other.edges_reversed() for other in tiles if other.key != tile.key]))
        found = sum(edge in other_edges for edge in tile.edges)
        if found == 2:
            corners.append(tile)

    return prod(int(t.key) for t in corners)

def edges_after_ops(edges: List[int], ops: List[int]) -> List[int]:
    """Apply rotation and flip *ops* to edge list *edges* returning the result"""
    new_edges = edges[:]
    for op in ops:
        if op == Tile.ROTATE:
            new_edges = new_edges[-1:] + new_edges[:-1]
        elif op == Tile.FLIP:
            new_edges = [reverse_int_bits(e) for e in \
                [new_edges[Tile.RIGHT], new_edges[Tile.TOP], new_edges[Tile.LEFT], new_edges[Tile.BOTTOM]]]
    return new_edges

def img_after_ops(img: List[str], ops: List[int]) -> List[str]:
    """Apply rotation and flip *ops* to image *img* returning the result"""
    new_img = img[:]
    for op in ops:
        if op == Tile.ROTATE:
            new_img = [cat(l)[::-1] for l in zip(*new_img)]
        elif op == Tile.FLIP:
            new_img = [l[::-1] for l in new_img]
    return new_img

def solve_puzzle(puzzle: List[List[Optional[Tile]]], from_pos: Position, remaining: List[Tile]) -> bool:
    """Tries to solve the given *puzzle*, starting from *from_pos*, going left-to-right,
    top-to-bottom, with the *remaining* tiles.
    Modifies *puzzle* to reflect what could be done, as well as *remaining*"""
    if len(remaining) == 0: # The end
        return True

    # Get the left and top tile, and their edge ids that face this tile
    left_tile = puzzle[from_pos.y][from_pos.x - 1] if from_pos.x > 0 else None
    top_tile = puzzle[from_pos.y - 1][from_pos.x] if from_pos.y > 0 else None
    constraint_left = edges_after_ops(left_tile.edges, left_tile.stored_ops)[Tile.RIGHT] \
        if left_tile is not None else None
    constraint_top = edges_after_ops(top_tile.edges, top_tile.stored_ops)[Tile.BOTTOM] \
        if top_tile is not None else None

    # DFS, try each remaining tile, recusively calling us for each possible one
    for tile in remaining:
        ops = tile.is_compatible(constraint_left, constraint_top)
        if ops is not None:
            # Store the necessary ops to make the tile compatible
            tile.stored_ops = ops
            puzzle[from_pos.y][from_pos.x] = tile
            new_pos = Position((from_pos.x + 1) % len(puzzle), from_pos.y +  (from_pos.x + 1) // len(puzzle))

            if solve_puzzle(puzzle, new_pos, [t for t in remaining if t != tile]):
                return True

    return False

def solve_part_two(day_input: List[str]) -> int:
    tiles = convert(day_input)
    # Get first corner that has 2 edges not compatible with others
    corner = tiles[0]
    for tile in tiles:
        other_edges = list(flatten([other.edges + other.edges_reversed() for other in tiles if other.key != tile.key]))
        found = sum(edge in other_edges for edge in tile.edges)
        if found == 2: 
            corner = tile
            break
    # Make it the top left on the puzzle
    idx = [i for i, edge in enumerate(corner.edges) if edge not in other_edges]
    if idx == [0,1]:
        corner.stored_ops = []
    elif idx == [1,2]:
        corner.stored_ops = [Tile.ROTATE] * 3
    elif idx == [2,3]:
        corner.stored_ops = [Tile.ROTATE] * 2
    elif idx == [0,3]:
        corner.stored_ops = [Tile.ROTATE]

    puzzle_sz = int(sqrt(len(tiles)))
    # Create puzzle, put corner on corner and remove it from remaining
    puzzle: List[List[Optional[Tile]]] = [[None for _ in range(puzzle_sz)] for _ in range(puzzle_sz)]
    puzzle[0][0] = corner
    tiles.remove(corner)

    # Solve
    solved = solve_puzzle(puzzle, Position(1, 0), tiles)
    if not solved: return -1

    # Join all images, without border, making sure that ops are applied
    img, i = [], 0
    tile_sz = len(tiles[0].img_no_border())
    for tile_line in puzzle:
        img += [''] * tile_sz
        for tile in tile_line: # type: ignore
            for j, l in enumerate(img_after_ops(tile.img_no_border(), tile.stored_ops)):
                img[i + j] += l
        i += tile_sz

    # Possible ways to rotate and flip the mask    
    possible_ops = [f + r for f in [[], [Tile.FLIP]] for r in [[Tile.ROTATE]*n for n in range(4)]] #type: ignore
    for op in possible_ops:
        mask = img_after_ops(["                  # ","#    ##    ##    ###"," #  #  #  #  #  #   "], op)
        # Convolution, but using the mask coords, getting the start of the mask in img, if exists
        mask_coords = [(y, x) for y, line in enumerate(mask) for x, c in enumerate(line) if c=='#']
        mask_starts = [(y, x) \
            for y in range(len(img) - len(mask)) \
                for x in range(len(img[0]) - len(mask[0])) \
                    if all([img[y + cy][x + cx] == '#' for cy, cx in mask_coords])]
        if len(mask_starts) > 0:
            return sum(l.count('#') for l in img) - len(mask_starts) * sum(l.count('#') for l in mask)
    return -1
