from copy import deepcopy
from typing import Optional

cycles = [dict(x=1)]


def process_instruction(instruction: str):
    if instruction == 'noop':
        cycles.append(deepcopy(cycles[-1]))
        return
    if instruction.startswith('addx'):
        value = int(instruction.split(' ')[1])
        cycles.append(deepcopy(cycles[-1]))  # cycle 1: still busy
        new_state = deepcopy(cycles[-1])
        new_state['x'] += value
        cycles.append(new_state)  # cycle 2: addition complete


def get_signal_strength(cycle: int, register: str = 'x') -> Optional[int]:
    if cycle >= len(cycles):
        return None
    return cycle * cycles[cycle - 1][register]


def get_pixel_for_cycle(cycle: int) -> str:
    sprite_middle = cycles[cycle - 1]['x']
    if abs(((cycle-1) % 40) - sprite_middle) <= 1:
        return '#'
    else:
        return '.'


if __name__ == '__main__':
    print('PART 1')
    with open('input.txt', 'r') as file:
        for line in file.read().splitlines():
            process_instruction(line)
    total_signal_strength = 0
    for i in range(20, 221, 40):
        strength = get_signal_strength(i)
        print(f'{i} signal strength = {strength}')
        total_signal_strength += strength
    print(f'total: {total_signal_strength}')

    print('PART 2')
    line = ''
    for i in range(1, 241):
        line += get_pixel_for_cycle(i)
        if i % 40 == 0:
            print(line)
            line = ''
