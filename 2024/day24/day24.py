import abc
import re
from abc import ABC
from typing import Callable, Dict, List, Tuple, Optional


class WireListener(ABC):
    @abc.abstractmethod
    def update_value(self):
        return


class Wire:
    def __init__(self, name: str, initial_value: Optional[bool] = None):
        self.name = name
        self.value = initial_value
        self.listeners = []

    def set_value(self, new_val):
        if new_val != self.value:
            self.value = new_val
            for listener in self.listeners:
                listener.update_value()

    def add_listener(self, listener: WireListener):
        self.listeners.append(listener)

    def __str__(self):
        return f'Wire({self.name}, {self.value})'

    def __repr__(self):
        return str(self)


class Gate(WireListener):
    def __init__(self, name: str, operation: Callable[[bool, bool], bool], input1: Wire, input2: Wire, output: Wire):
        self.name = name
        self.operation = operation
        self.input1 = input1
        self.input2 = input2
        self.output = output
        input1.add_listener(self)
        input2.add_listener(self)
        self.current_output = None
        self.update_value()

    def update_value(self):
        if self.input1.value is None or self.input2.value is None:
            new_output = None
        else:
            new_output = self.operation(self.input1.value, self.input2.value)
        if self.current_output != new_output:
            self.current_output = new_output
            self.output.set_value(new_output)

    def __str__(self):
        return f'Gate({self.input1.name} {self.name} {self.input2.name} -> {self.output.name})'

    def __repr__(self):
        return str(self)


OPERATIONS = {
    'AND': lambda v1, v2: v1 and v2,
    'OR': lambda v1, v2: v1 or v2,
    'XOR': lambda v1, v2: v1 ^ v2
}


def parse_file(path: str) -> Tuple[Dict[str, Wire], List[Gate]]:
    with open(path, 'r') as file:
        wires, gates = file.read().split('\n\n')
    wire_dict = dict()
    for line in wires.splitlines():
        name, value = line.split(': ')
        wire_dict[name] = Wire(name, bool(int(value)))
    gate_list = []
    for line in gates.splitlines():
        match = re.search("(\\w+) (\\w+) (\\w+) -> (\\w+)", line)
        input1, name, input2, output = match.group(1), match.group(2), match.group(3), match.group(4)
        if input1 not in wire_dict:
            wire_dict[input1] = Wire(input1)
        if input2 not in wire_dict:
            wire_dict[input2] = Wire(input2)
        if output not in wire_dict:
            wire_dict[output] = Wire(output)
        operation = OPERATIONS[name]
        gate_list.append(Gate(name, operation, wire_dict[input1], wire_dict[input2], wire_dict[output]))
    return wire_dict, gate_list


class Calculator:
    def __init__(self, wires: Dict[str, Wire], gates: List[Gate]):
        self.all_wires = wires
        self.gates = gates
        self.x_wires = [wire for wire in wires.values() if wire.name.startswith('x')]
        self.x_wires.sort(key=lambda w: w.name)
        self.x_wires.reverse()
        self.y_wires = [wire for wire in wires.values() if wire.name.startswith('y')]
        self.y_wires.sort(key=lambda w: w.name)
        self.y_wires.reverse()
        self.z_wires = [wire for wire in wires.values() if wire.name.startswith('z')]
        self.z_wires.sort(key=lambda w: w.name)
        self.z_wires.reverse()

    def x(self) -> str:
        return "".join(["1" if w.value else "0" for w in self.x_wires])

    def x_int(self) -> int:
        return int(self.x(), base=2)

    def y(self) -> str:
        return "".join(["1" if w.value else "0" for w in self.y_wires])

    def y_int(self) -> int:
        return int(self.y(), base=2)

    def z(self) -> str:
        return "".join(["1" if w.value else "0" for w in self.z_wires])

    def z_int(self) -> int:
        return int(self.z(), base=2)

    def load_x(self, val: int):
        val = bin(val)[2:]
        if len(val) < len(self.x_wires):
            val = val.zfill(len(self.x_wires))
        for bit, wire in zip(val, self.x_wires):
            wire.set_value(bit == '1')

    def load_y(self, val: int):
        val = bin(val)[2:]
        if len(val) < len(self.y_wires):
            val = val.zfill(len(self.y_wires))
        for bit, wire in zip(val, self.y_wires):
            wire.set_value(bit == '1')

    def test(self, x: int, y: int, expected_z: int) -> bool:
        self.load_x(x)
        self.load_y(y)
        z = self.z_int()
        if z != expected_z:
            print(f'expected ({x},{y}) to be {expected_z}, got {z}')
            return False
        return True

    def switch_outputs(self, wire1: Wire, wire2: Wire):
        gate1 = next(g for g in self.gates if g.output == wire1)
        gate2 = next(g for g in self.gates if g.output == wire2)
        gate1.output = wire2
        gate2.output = wire1
        gate1.update_value()
        gate2.update_value()


if __name__ == '__main__':
    print('part 1')
    wires, gates = parse_file('input.txt')
    c = Calculator(wires, gates)
    print(c.z_int())

    print('part 2')
    val = 1
    for i in range(len(c.x_wires)):
        print(f'TESTING {val}\n========')
        c.test(val, 0, val)
        c.test(0, val, val)
        c.test(val, val, 2 * val)
        val *= 2
