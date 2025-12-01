import re
from typing import Tuple, List, Optional

from advent_utils.two_d_utils import Point

regex_a = 'Button A: X\\+(\\d+), Y\\+(\\d+)'
regex_b = 'Button B: X\\+(\\d+), Y\\+(\\d+)'
regex_prize = 'Prize: X=(\\d+), Y=(\\d+)'


def prize_as_AB(a: Point, b: Point, prize: Point) -> Optional[Tuple[int, int]]:
    det = a[1] * b[0] - a[0] * b[1]
    if det == 0:
        return None
    times_a = (b[1] * prize[0] - b[0] * prize[1]) / (b[1] * a[0] - b[0] * a[1])
    times_b = (a[1] * prize[0] - a[0] * prize[1]) / (a[1] * b[0] - a[0] * b[1])
    if not (times_a.is_integer() and times_b.is_integer()):
        return None
    return int(times_a), int(times_b)


def get_cost(a: Point, b: Point, prize: Point) -> Optional[int]:
    solution = prize_as_AB(a, b, prize)
    if not solution:
        return None
    times_a, times_b = solution
    return int(3 * times_a + 1 * times_b)


def parse_machine(input_string: str) -> List[Tuple[int, int]]:
    match = re.search(regex_a, input_string)
    a = (int(match.group(1)), int(match.group(2)))
    match = re.search(regex_b, input_string)
    b = (int(match.group(1)), int(match.group(2)))
    match = re.search(regex_prize, input_string)
    prize = (int(match.group(1)), int(match.group(2)))
    return [a, b, prize]


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        machines = file.read().split('\n\n')
    machines = [parse_machine(m) for m in machines]
    print('part 1')
    total_cost, total_wins = 0, 0
    for i, machine in enumerate(machines):
        a, b, prize = machine
        cost = get_cost(a, b, prize)
        if cost:
            total_cost += cost
            total_wins += 1
    print(total_cost)
    print('part 2')
    total_cost, total_wins = 0, 0
    for i, machine in enumerate(machines):
        a, b, prize = machine
        prize = prize[0] + 10000000000000 , prize[1] + 10000000000000
        cost = get_cost(a, b, prize)
        if cost:
            total_cost += cost
            total_wins += 1
    print(total_cost)

