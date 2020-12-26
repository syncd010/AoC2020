"""
Day 8
"""
from typing import List, NamedTuple
from dataclasses import dataclass

@dataclass
class Instruction:
    op: str
    arg: int

class Console:
    def __init__(self, prog: List[Instruction]):
        self.prog = prog
        self.acc = 0
        self.ip = 0

    def exec_next(self):
        inst = self.prog[self.ip]
        if inst.op == 'acc':
            self.acc += inst.arg
            self.ip += 1
        elif inst.op == 'jmp':
            self.ip += inst.arg
        elif inst.op == 'nop':
            self.ip += 1

def convert(day_input: List[str]) -> List[Instruction]:
    def line_to_inst(line: str) -> Instruction:
        l = line.split()
        return Instruction(l[0], int(l[1]))

    return [line_to_inst(line) for line in day_input]

def solve_part_one(day_input: List[str]) -> int:
    console = Console(convert(day_input))
    exec_count = [0] * len(console.prog)

    # Execute and keep track of which instructions were executed
    while console.ip < len(console.prog) and exec_count[console.ip] == 0:
        exec_count[console.ip] += 1
        console.exec_next()

    return console.acc

def solve_part_two(day_input: List[str]) -> int:
    prog = convert(day_input)

    for inst in prog:
        if inst.op not in ['nop', 'jmp']: continue
        # Switch the instruction
        inst.op = 'nop' if inst.op == 'jmp' else 'jmp'
        # and execute the altered program
        console = Console(prog)
        exec_count = [0] * len(prog)
        while console.ip < len(prog) and exec_count[console.ip] == 0:
            exec_count[console.ip] += 1
            console.exec_next()
        # Reverse the switch
        inst.op = 'nop' if inst.op == 'jmp' else 'jmp'

        # Return if reached the end        
        if console.ip >= len(prog):
            return console.acc

    return -1
