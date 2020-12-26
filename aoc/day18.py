"""
Day 18
"""
from typing import List, Union
import operator

def convert(day_input: List[str]) -> List[List[str]]:
    """Return each input token in a separate position"""
    return [line.replace('(', '( ').replace(')', ' )').split() for line in day_input]

def eval_infix(expr: List[str]) -> str:
    """Evals expr sequentially, just respecting precedence of *(* and *)*.
    Consumes the evaluated tokens in *expr*, including the final *)* if its the 
    last token of the expression
    
    Note: expects *expr* to be in infix notation but reversed, as it uses 
    pop/append to manipulate *expr*"""
    ops = {'+': operator.add, '*': operator.mul}
    while len(expr) >= 1:
        arg1 = expr.pop()
        if arg1 == '(': arg1 = eval_infix(expr)
        if len(expr) == 0: return arg1
        op = expr.pop()
        if op == ')': return arg1
        arg2 = expr.pop()
        if arg2 == '(': arg2 = eval_infix(expr)
        expr.append(str(ops[op](int(arg1), int(arg2))))
    return expr[0]

list_reverse = lambda l: list(reversed(l))

def solve_part_one(day_input: List[str]) -> int:
    res = [int(eval_infix(list_reverse(line))) for line in convert(day_input)]
    return sum(res)

def solve_part_two(day_input: List[str]) -> int:
    def find_expr_boundary(line: List[str], start_idx: int, step: int, lvl_up: str, lvl_down: str) -> int:
        """Finds the boundary of an expression, starting at *start_idx*, in direction *step*,
        considering that *lvl_up* and *lvl_down* delimit sub-expressions. This makes it usable 
        to find both boundaries to the left or right of a position"""
        lvl, idx = 0, start_idx + step
        while lvl > 0 or line[idx] == lvl_up:
            # Increase or decrease level depending on this position
            lvl = lvl + (line[idx] == lvl_up) - (line[idx] == lvl_down)
            # If reach the boundary break to avoid adding step one more time
            if lvl == 0: break
            idx += step
        return idx

    # Strategy is to add '(' and ')' around all the '+' operators found, so that
    # the eval function can work sequentially, just giving priority to expressions
    # surrounded by '(' ')'
    res = []
    for line in convert(day_input):
        idx = 0
        while idx < len(line):
            if line[idx] == '+':
                at = find_expr_boundary(line, idx, -1, ')', '(')
                line.insert(at, '(')
                at = find_expr_boundary(line, idx + 1, +1, '(', ')')
                line.insert(at + 1, ')')
                idx += 2 # Inserted 2, so advance
            idx += 1
        res.append(int(eval_infix(list_reverse(line))))
    return sum(res)
