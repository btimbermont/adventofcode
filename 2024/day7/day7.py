from collections.abc import Callable
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Operator:
    name: str
    apply: Callable[[int, int], int]


PLUS = Operator("+", lambda a, b: a + b)
MULT = Operator("*", lambda a, b: a * b)

POSSIBLE_OPERATORS = [PLUS, MULT]


def can_be_solved(solution: int, current_value: Optional[int], values_left: List[int], print_value: str = '') -> bool:
    # start: take first value
    if current_value is None:
        return can_be_solved(solution, values_left[0], values_left[1:], f'{solution} = {values_left[0]}')
    # end: check solution
    if not values_left:
        valid = solution == current_value
        if valid:
            print(print_value)
        return valid
    # mid: we can only make values bigger: return when too large
    if current_value > solution:
        return False
    # not there yet: apply operations
    next_value = values_left[0]
    values_left = values_left[1:]
    return any([can_be_solved(solution, op.apply(current_value, next_value), values_left,
                              f'{print_value} {op.name} {next_value}') for op in POSSIBLE_OPERATORS])


if __name__ == '__main__':
    print('part 1')
    with open('input.txt', 'r') as file:
        result = 0
        for line in file.read().splitlines():
            solution, values = line.split(':')
            solution = int(solution)
            values = [int(v) for v in values.strip().split(' ')]
            if can_be_solved(solution, None, values):
                result += solution
    print(result)
    print('part 2')
    POSSIBLE_OPERATORS.append(Operator('||', lambda a, b: int(f'{a}{b}')))
    with open('input.txt', 'r') as file:
        result = 0
        for line in file.read().splitlines():
            solution, values = line.split(':')
            solution = int(solution)
            values = [int(v) for v in values.strip().split(' ')]
            if can_be_solved(solution, None, values):
                result += solution
    print(result)
