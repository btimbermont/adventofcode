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

    def __str__(self):
        return f'Mahine({self.wanted_lights}, {self.joltages})'

    def minimal_button_presses(self):
        for r in range(1, len(self.buttons) + 1):
            for buttons_pressed in combinations(self.buttons, r):
                lights = [0] * len(self.wanted_lights)
                for button in buttons_pressed:
                    lights = xor(lights, button)
                if lights == self.wanted_lights:
                    # print(f'SOLVED! XOR {buttons_pressed} --> {lights}')
                    return r

    def minimum_joltage_presses(self):
        press_ranges = []
        ultra_max = max(self.joltages)
        for button in self.buttons:
            max_presses = ultra_max
            for i in range(len(button)):
                if button[i]:
                    max_presses = min(self.joltages[i], max_presses)
            press_ranges.append([0, max_presses])
            # print(f'button {button} can be pressed max {max_presses} times')
        print(press_ranges)
        joltage_to_button = []
        for i in range(len(self.joltages)):
            connected_buttons = []
            for j in range(len(self.buttons)):
                if self.buttons[j][i]:
                    connected_buttons.append(j)
            joltage_to_button.append(connected_buttons)

        # one loop over joltages
        something_changed = True
        while something_changed:
            something_changed = False
            for j in range(len(self.joltages)):
                required_joltage = self.joltages[j]
                button_indexes = joltage_to_button[j]
                print(f'Checking buttons {button_indexes} for required joltage {required_joltage}.')
                print(f'Current ranges {[press_ranges[i] for i in button_indexes]}')
                for b in button_indexes:
                    print(f'Adjusting button {b} ({self.buttons[b]})')
                    other_presses = press_ranges[:b] + press_ranges[b + 1:]
                    other_min_press = sum([r[0] for r in other_presses])
                    other_max_press = sum([r[1] for r in other_presses])
                    new_min = max(0, required_joltage - other_max_press)
                    new_max = required_joltage - other_min_press
                    new_range = [new_min, new_max]
                    if press_ranges[b] != new_range:
                        print(f'New range for button {b}: {new_range}\n')
                        something_changed = True
                        press_ranges[b] = [new_min, new_max]


class ConnectedButtons:
    def __init__(self, buttons: List[List[int]]):
        l = len(buttons[0])
        for b in buttons:
            if not l == len(b):
                raise ValueError(f'Not all buttons have the same range! {buttons}')


if __name__ == '__main__':
    machines = []
    with open('test_input.txt', 'r') as file:
        for line in file:
            machines.append(Machine(line))
    print('part 1')
    print(sum([m.minimal_button_presses() for m in machines]))

    print('part 2')
    m = machines[0]
    print(m)
    m.minimum_joltage_presses()
