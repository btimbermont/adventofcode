from typing import List, Tuple


class Computer:
    def __init__(self):
        self.registers = [0, 0, 0]
        self.output = []
        self.current_program = None
        self.instruction_pointer = None

    @property
    def reg_a(self):
        return self.registers[0]

    @reg_a.setter
    def reg_a(self, value: int):
        self.registers[0] = value

    @property
    def reg_b(self):
        return self.registers[1]

    @reg_b.setter
    def reg_b(self, value: int):
        self.registers[1] = value

    @property
    def reg_c(self):
        return self.registers[2]

    @reg_c.setter
    def reg_c(self, value: int):
        self.registers[2] = value

    def load_state(self, registers: Tuple[int, int, int]):
        self.registers = list(registers)

    def load_program(self, new_program: List[int]):
        self.current_program = new_program
        self.instruction_pointer = 0

    def execute_full_program(self):
        while self.execute_next_instruction():
            pass

    def execute_next_instruction(self) -> bool:
        if not self.current_program:
            print('no program loaded!')
            return False
        if self.instruction_pointer < 0 or self.instruction_pointer > len(self.current_program) - 2:
            return False
        opcode, operand = self.read_current_instruction()
        self.process_instruction(opcode, operand)
        self.instruction_pointer += 2
        return True

    def read_current_instruction(self) -> Tuple[int, int]:
        return self.current_program[self.instruction_pointer], self.current_program[self.instruction_pointer + 1]

    def process_instruction(self, opcode: int, operand: int):
        if not (0 <= opcode <= 7 and 0 <= operand <= 7):
            raise ValueError(f'invalid instruction: opcode {opcode}, operand {operand}')
        match opcode:
            case 0:
                # adv: reg_a division
                numerator = self.reg_a
                denominator = 2 ** self.combo_operand(operand)
                self.reg_a = int(numerator / denominator)
            case 1:
                # bxl: bitwise XOR or reg_b
                self.reg_b = self.reg_b ^ operand
            case 2:
                # bst: mod8
                self.reg_b = self.combo_operand(operand) % 8
            case 3:
                # jnz: jump if reg_a is not zero:
                if self.reg_a != 0:
                    self.instruction_pointer = operand - 2  # -2 because our code always adds 2 after the instruction
            case 4:
                # bxc: XOR of B and C, store in b
                self.reg_b = self.reg_b ^ self.reg_c
            case 5:
                # out: outputs value mod 8
                val = self.combo_operand(operand) % 8
                self.out(val)
            case 6:
                # bdv: like adv, but store in a
                numerator = self.reg_a
                denominator = 2 ** self.combo_operand(operand)
                self.reg_b = int(numerator / denominator)
            case 7:
                # cdv: like adv, but store in c
                numerator = self.reg_a
                denominator = 2 ** self.combo_operand(operand)
                self.reg_c = int(numerator / denominator)

    def combo_operand(self, operand: int):
        if 0 <= operand <= 3:
            return operand
        if 4 <= operand <= 6:
            return self.registers[operand - 4]
        if operand == 7:
            raise ValueError(
                f'Invalid combo operand {operand}. '
                f'Currently at index {self.instruction_pointer} in program {self.current_program}')

    def out(self, value):
        self.output.append(value)

    def reset_output(self):
        self.output = []

    def __str__(self):
        return f'Computer(A:{self.reg_a}, B:{self.reg_b}, C:{self.reg_c}, output:{self.output})'

    def __repr__(self):
        return str(self)


def test_ops():
    c = Computer()

    c.load_state((0, 0, 9))
    c.load_program([2, 6])
    c.execute_full_program()
    assert c.reg_b == 1

    c.load_state((10, 0, 0))
    c.load_program([5, 0, 5, 1, 5, 4])
    c.execute_full_program()
    assert c.output == [0, 1, 2]
    c.reset_output()

    c.load_state((2024, 0, 0))
    c.load_program([0, 1, 5, 4, 3, 0])
    c.execute_full_program()
    assert c.output == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    assert c.reg_a == 0
    c.reset_output()

    c.load_state((0, 29, 0))
    c.load_program([1, 7])
    c.execute_full_program()
    assert c.reg_b == 26
    c.reset_output()

    c.load_state((0, 2024, 43690))
    c.load_program([4, 0])
    c.execute_full_program()
    assert c.reg_b == 44354
    c.reset_output()


def might_self_replicate(computer: Computer):
    if len(computer.output) > len(computer.current_program):
        return False
    for a, b in zip(computer.output, computer.current_program):
        if a != b:
            return False
    return True


def self_replicated(computer: Computer):
    return computer.output == computer.current_program


def is_good_value(a: int) -> bool:
    c = Computer()
    c.load_state((a, 0, 0))
    c.load_program([0,3,5,4,3,0])  # test input
    # c.load_program([2, 4, 1, 3, 7, 5, 1, 5, 0, 3, 4, 3, 5, 5, 3, 0])
    while c.execute_next_instruction() and might_self_replicate(c):
        pass
    return self_replicated(c)


if __name__ == '__main__':
    # test_ops()
    print("part 1")
    c = Computer()
    # test input
    # c.load_state((729,0,0))
    # c.load_program([0,1,5,4,3,0])
    # real input
    c.load_state((47006051, 0, 0))
    c.load_program([2, 4, 1, 3, 7, 5, 1, 5, 0, 3, 4, 3, 5, 5, 3, 0])
    c.execute_full_program()
    print(",".join([str(v) for v in c.output]))
    print("part 2")
    a = 0
    while True:
        if is_good_value(a):
            break
        a+=1
        if a % 1000000 == 0:
            print(f'attempting A = {a}')
    print(f'program self replicated with A={a}')
