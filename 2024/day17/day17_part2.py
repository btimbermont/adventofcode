from collections.abc import Callable
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass(frozen=True)
class ProgramState:
    reg_a: int
    reg_b: int
    reg_c: int
    pointer_index: int

    def combo_operand(self, operand: int):
        if 0 <= operand <= 3:
            return operand
        if 4 == operand:
            return self.reg_a
        if 5 == operand:
            return self.reg_b
        if 6 == operand:
            return self.reg_c
        if operand == 7:
            raise ValueError(
                f'Invalid combo operand {operand}.')

    def next_state(self, reg_a: int = None, reg_b: int = None, reg_c: int = None, pointer_index: int = None):
        return ProgramState(self.reg_a if reg_a is None else reg_a,
                            self.reg_b if reg_b is None else reg_b,
                            self.reg_c if reg_c is None else reg_c,
                            self.pointer_index + 2 if pointer_index is None else pointer_index)


def adv(state: ProgramState, operand: int) -> Tuple[ProgramState, Optional[int]]:
    numerator = state.reg_a
    denominator = 2 ** state.combo_operand(operand)
    return state.next_state(reg_a=int(numerator / denominator)), None


def bxl(state: ProgramState, operand: int) -> Tuple[ProgramState, Optional[int]]:
    new_b = state.reg_b ^ operand
    return state.next_state(reg_b=new_b), None


def bst(state: ProgramState, operand: int) -> Tuple[ProgramState, Optional[int]]:
    new_b = state.combo_operand(operand) % 8
    return state.next_state(reg_b=new_b), None


def jnz(state: ProgramState, operand: int) -> Tuple[ProgramState, Optional[int]]:
    if state.reg_a == 0:
        return state.next_state(), None
    return state.next_state(pointer_index=operand), None


def bxc(state: ProgramState, operand: int) -> Tuple[ProgramState, Optional[int]]:
    new_b = state.reg_b ^ state.reg_c
    return state.next_state(reg_b=new_b), None


def out(state: ProgramState, operand: int) -> Tuple[ProgramState, Optional[int]]:
    output = state.combo_operand(operand) % 8
    return state.next_state(), output


def bdv(state: ProgramState, operand: int) -> Tuple[ProgramState, Optional[int]]:
    numerator = state.reg_a
    denominator = 2 ** state.combo_operand(operand)
    return state.next_state(reg_b=int(numerator / denominator)), None


def cdv(state: ProgramState, operand: int) -> Tuple[ProgramState, Optional[int]]:
    numerator = state.reg_a
    denominator = 2 ** state.combo_operand(operand)
    return state.next_state(reg_c=int(numerator / denominator)), None


Instruction = Callable[[ProgramState, int], Tuple[ProgramState, Optional[int]]]
instructions = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]


def decode_opcode(opcode: int) -> Instruction:
    return instructions[opcode]


class Program:
    def __init__(self, instructions: List[int]):
        self.instructions = instructions

    def run_full_program(self, reg_a: int = 0, reg_b: int = 0, reg_c: int = 0) -> List[int]:
        return self.get_output(ProgramState(reg_a, reg_b, reg_c, 0))

    def get_output(self, state: ProgramState) -> List[int]:
        pointer = state.pointer_index
        if not (0 <= pointer < len(self.instructions) - 1):
            return []  # halt program
        opcode, operand = self.instructions[pointer: pointer + 2]
        instruction = decode_opcode(opcode)
        new_state, instruction_output = instruction(state, operand)
        if instruction_output is None:
            return self.get_output(new_state)
        output = self.get_output(new_state)
        output = output.copy()
        output.insert(0, instruction_output)
        return output


class AdventProgram(Program):

    def __init__(self):
        super().__init__([2, 4, 1, 3, 7, 5, 1, 5, 0, 3, 4, 3, 5, 5, 3, 0])

    def do_one_loop(self, a: int):
        state = ProgramState(a, 0, 0, 0)


def octals_to_string(octals: List[int]) -> str:
    return "0o" + ("".join([str(o) for o in octals]))


def octals_to_int(octals: List[int]) -> int:
    return int(octals_to_string(octals), base=8)


def octal_candidates(octals: List[List[int]], pad: int) -> List[str]:
    candidates = ['0o']
    for octal in octals:
        candidates = [f'{c}{possibility}' for c in candidates for possibility in octal]
    return [s.ljust(pad, '0') for s in candidates]


if __name__ == '__main__':
    input_program = [2, 4, 1, 3, 7, 5, 1, 5, 0, 3, 4, 3, 5, 5, 3, 0]
    # what we know of this program:
    #  * only A matters for the output, B and C can be ignored
    #  * to get output of length n, A needs to be within 8^(n-1) - 8^(n)
    # --> want output length 1? A needs to be 0 or higher. Want length 2? A needs to be >=8, etc
    # --> we notice that the rightmost output number is affected by the most significant octal digit
    # so: we try to construct the octals by getting the most significant octal digit first

    p = Program(input_program)
    octals = []
    for i in range(len(input_program)):
        add_candidates = []
        for o in range(8):
            current_try = octals.copy()
            current_try.append([o])
            attempts = [int(v, base=8) for v in octal_candidates(current_try, len(input_program))]
            for attempt in attempts:
                print(f'trying {attempt}')
                output = p.run_full_program(attempt)
                if output[len(input_program) -1- i:] == input_program[len(input_program) -1- i:]:
                    add_candidates.append(o)
        octals.append(add_candidates)

    print(octals)

    # length_map = [1]
    # a = 1
    # p = Program(input_program)
    # while len(length_map) <= len(input_program):
    #     a *= 2
    #     current_length = len(p.run_full_program(reg_a=a))
    #     if current_length > len(length_map):
    #         length_map.append(a)
    # print(length_map)
    # mult_map = [1]
    # for i in range(1, len(length_map)):
    #     mult_map.append(length_map[i] // length_map[i-1])
    # print(mult_map)
