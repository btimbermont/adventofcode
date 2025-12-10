import re
from itertools import combinations
from typing import List


def xor(a: List[int], b: List[int]) -> List[int]:
    if len(a) != len(b):
        raise ValueError(f'{a} and {b} do not ahve the same length!')
    return [(a[i] + b[i]) % 2 for i in range(len(a))]


class Machine:
    def __init__(self, line: str):
        match = re.search(r'\[(.*)] (.*) \{(.*)}', line)
        self.wanted_lights, buttons, self.joltages = match.groups()
        self.wanted_lights = [1 if c == '#' else 0 for c in self.wanted_lights]
        self.light = [0] * len(self.wanted_lights)
        self.buttons = []
        for button in buttons.split():
            b = [0] * len(self.wanted_lights)
            for i in [int(c) for c in button[1:-1].split(',')]:
                b[i] = 1
            self.buttons.append(b)
        self.joltages = [int(j) for j in self.joltages.split(',')]

    def minimal_button_presses(self):
        for r in range(1, len(self.buttons)+1):
            for buttons_pressed in combinations(self.buttons, r):
                lights = [0] * len(self.wanted_lights)
                for button in buttons_pressed:
                    lights = xor(lights, button)
                if lights == self.wanted_lights:
                    print(f'SOLVED! XOR {buttons_pressed} --> {lights}')
                    return r



if __name__ == '__main__':
    machines = []
    with open('input.txt', 'r') as file:
        for line in file:
            machines.append(Machine(line))
    print('part 1')
    print(sum([m.minimal_button_presses() for m in machines]))

