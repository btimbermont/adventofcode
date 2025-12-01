from itertools import permutations
from typing import List

from advent_utils.two_d_utils import String2dMap, MOVEMENTS


class KeyPad(String2dMap):
    def __init__(self, layout: str, initial_button: str = 'A'):
        super().__init__(input=layout)
        self.initial_button = initial_button
        self.current_position = self.lookup_content(initial_button)[0]
        self.forbidden = self.lookup_content(' ')[0]

    def reset(self):
        self.current_position = self.lookup_content(self.initial_button)[0]

    def get_routes_to_button(self, button: str) -> List[str]:
        new_pos = self.lookup_content(button)[0]
        if not new_pos or new_pos == self.forbidden:
            raise ValueError(f'Cannot go to button "{button}" at {new_pos}')
        diff_x = new_pos[0] - self.current_position[0]
        diff_y = new_pos[1] - self.current_position[1]
        dir_x = ('>' if diff_x > 0 else '<') * abs(diff_x)
        dir_y = ('v' if diff_y > 0 else '^') * abs(diff_y)
        if self.current_position[0] == self.forbidden[0]:
            fdiff_y = self.forbidden[1] - self.current_position[1]
            forbidden_start = ('v' if fdiff_y > 0 else '^') * abs(fdiff_y)
        elif self.current_position[1] == self.forbidden[1]:
            fdiff_x = self.forbidden[0] - self.current_position[0]
            forbidden_start = ('>' if fdiff_x > 0 else '<') * abs(fdiff_x)
        else:
            forbidden_start = None
        self.current_position = new_pos
        # base_route = f'{dir_x}{dir_y}'
        # possibilities = list(set("".join(p) for p in permutations(base_route)))
        possibilities = list({f'{dir_x}{dir_y}', f'{dir_y}{dir_x}'})
        if forbidden_start is not None:
            possibilities = [p for p in possibilities if not p.startswith(forbidden_start)]
        possibilities.sort(key=number_of_changes)
        return possibilities

    def get_possible_routes_for_sequence(self, sequence: str) -> List[str]:
        routes = ['']
        for button in sequence:
            routes_to_button = self.get_routes_to_button(button)
            routes = [f'{old_route}{new_route}A' for old_route in routes for new_route in routes_to_button]
        routes.sort(key=number_of_changes)
        return routes

    def execute_commands(self, commands: str) -> str:
        output = ''
        for c in commands:
            if c == 'A':
                output += self.get_cell(self.current_position)
            elif c in '<>^v':
                self.current_position = MOVEMENTS[c].apply(self.current_position)
                if self.current_position == self.forbidden:
                    raise ValueError('Currently at empty button, this is an illegal state')
            else:
                raise ValueError(f"Unknown command: {c}")
        return output


def is_valid(s: str) -> bool:
    for part in s.split('A'):
        if number_of_changes(part) % 10000 > 1:
            return False
    return True


def number_of_changes(s: str) -> int:
    return 10000 * len(s) + sum([0 if a == b else 1 for a, b in zip(s[:-1], s[1:])])


numpad = KeyPad('789\n456\n123\n 0A', 'A')
dir_pad_1 = KeyPad(' ^A\n<v>', 'A')
dir_pad_2 = KeyPad(' ^A\n<v>', 'A')


def get_shortest_possible_route(setup: List[KeyPad], door_code: str) -> str:
    routes = [door_code]
    for pad in setup:
        pad.reset()
        new_routes = []
        current_shortest = 10000000000000000000000000000
        for r in routes:
            result = pad.get_possible_routes_for_sequence(r)
            result_length = len(result[0])
            if result_length > current_shortest:
                continue
            if result_length == current_shortest:
                new_routes += result
            if result_length < current_shortest:
                current_shortest = result_length
                new_routes = result
        routes = [r for r in new_routes if is_valid(r)]
    return routes[0]


def calc_score(setup: List[KeyPad], door_code: str) -> int:
    route = get_shortest_possible_route(setup, door_code)
    print(f'{door_code}: {route}')
    numeric_part = int(door_code.replace('A', ''))
    score = len(route) * numeric_part
    print(f'Score = {len(route)} * {numeric_part} = {score}')
    return score


def execute_commands(commands: str) -> str:
    result = commands
    for pad in reversed(setup):
        pad.reset()
        result = pad.execute_commands(result)
    return result


if __name__ == '__main__':
    setup = [numpad, dir_pad_1, dir_pad_2]
    test_input = ['029A', '980A', '179A', '456A', '379A']
    input = ['382A', '463A', '935A', '279A', '480A']
    print('part 1 test')
    result = 0
    for i in test_input:
        result += calc_score(setup, i)
    print(f'Result: {result}')
    print('part 1 real')
    result = 0
    for i in input:
        result += calc_score(setup, i)
    print(f'Result: {result}')

    print('part 2')
    setup2 = [numpad] + [KeyPad(' ^A\n<v>', 'A') for _ in range(25)]
    result = 0
    for i in test_input:
        result += calc_score(setup2, i)
    print(f'Result: {result}')
