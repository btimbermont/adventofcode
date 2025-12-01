import re
from math import prod
from typing import Tuple, List

from advent_utils.two_d_utils import Vector, get_neighbors, Point


class Robot:
    def __init__(self, line: str, bounds: Tuple[int, int]):
        match = re.search("p=(\\d+,\\d+) v=(-?\\d+,-?\\d+)", line)
        self.position = tuple([int(v) for v in match.group(1).split(',')])
        vector_x, vector_y = match.group(2).split(',')
        self.direction = Vector(int(vector_x), int(vector_y))
        self.bound_x, self.bound_y = bounds

    def advance(self, times: int = 1):
        advance_vector = self.direction.scale(times)
        self.position = advance_vector + self.position
        # teleport around bounds
        self.position = (self.position[0] % self.bound_x, self.position[1] % self.bound_y)

    def __str__(self):
        return f'Robot({self.position}, dir:{self.direction})'

    def __repr__(self):
        return str(self)


def print_robots(robots: List[Robot], bounds: Tuple[int, int]):
    output = ''
    for y in range(bounds[1]):
        line = ''
        for x in range(bounds[0]):
            count = len([r for r in robots if r.position == (x, y)])
            line = f'{line}{(count if count > 0 else ".")}'
        output += f'{line}\n'
    print(output)


def safety_factor(robots: List[Robot], bounds: Tuple[int, int]) -> int:
    split_x = bounds[0] // 2
    split_y = bounds[1] // 2
    quadrants = [[0, 0], [0, 0]]
    for robot in robots:
        if robot.position[0] == split_x or robot.position[1] == split_y:
            continue
        qx = round(robot.position[0] / bounds[0])
        qy = round(robot.position[1] / bounds[1])
        quadrants[qx][qy] += 1
    print(f'quadrants: {quadrants}')
    return prod([q for qs in quadrants for q in qs])


def is_closed_in(robot: Robot, robot_positions: List[Point]) -> bool:
    return all([(n in robot_positions) for n in get_neighbors(robot.position)])


if __name__ == '__main__':
    # test
    bounds = 11, 7
    input_file = 'test_input.txt'
    # real input
    bounds = 101, 103
    input_file = 'input.txt'
    with open(input_file, 'r') as file:
        robots = [Robot(line, bounds) for line in file.read().splitlines()]
    print('part 1')
    for r in robots:
        r.advance(100)
    print_robots(robots, bounds)
    print(safety_factor(robots, bounds))
    print('part 2')
    # reload robots
    with open(input_file, 'r') as file:
        robots = [Robot(line, bounds) for line in file.read().splitlines()]
    current_max = 0.0
    iter = 0
    while True:
        for robot in robots:
            robot.advance()
        iter += 1
        if iter % 1000 == 0:
            print(f'iter {iter}...')
        robot_positions = {robot.position for robot in robots}
        closed_in_robots = [r for r in robots if is_closed_in(r, robot_positions)]
        if len(closed_in_robots) > 10:
            print_robots(robots, bounds)
            print(f'iter {iter}, closed in: {len(closed_in_robots)}, map:')
            cont = input('continue? (N to stop)')
            if cont and cont in 'nN':
                break
            else:
                print('continuing...')
    print('Done')
