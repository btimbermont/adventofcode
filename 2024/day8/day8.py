from dataclasses import dataclass
from itertools import combinations
from typing import Tuple, List


@dataclass
class Antenna():
    frequency: str
    x: int
    y: int

    @property
    def coordinates(self) -> Tuple[int, int]:
        return self.x, self.y

    def antinodes(self, other: 'Antenna') -> List[Tuple[int, int]]:
        if other.frequency != self.frequency or self == other:
            return []
        diffx, diffy = other.x - self.x, other.y - self.y
        return [(self.x - diffx, self.y - diffy), (other.x + diffx, other.y + diffy)]

    def antinodes2(self, other: 'Antenna', max_x: int, max_y: int) -> List[Tuple[int, int]]:
        if other.frequency != self.frequency or self == other:
            return []
        diffx, diffy = other.x - self.x, other.y - self.y
        result = []
        curr_x, curr_y = self.x, self.y
        while in_bounds((curr_x, curr_y), max_x, max_y):
            result.append((curr_x, curr_y))
            curr_x, curr_y = curr_x - diffx, curr_y - diffy
        curr_x, curr_y = other.x, other.y
        while in_bounds((curr_x, curr_y), max_x, max_y):
            result.append((curr_x, curr_y))
            curr_x, curr_y = curr_x + diffx, curr_y + diffy
        return result


def print_map(antennas: List[Antenna], antinodes: List[Tuple[int, int]] = [], max_x: int = None, max_y=None):
    # get bounds
    if not max_x or not max_y:
        min_x = min([0] + [a.x for a in antennas] + [a[0] for a in antinodes])
        min_y = min([0] + [a.y for a in antennas] + [a[1] for a in antinodes])
        max_x = 1 + max([0] + [a.x for a in antennas] + [a[0] for a in antinodes])
        max_y = 1 + max([0] + [a.y for a in antennas] + [a[1] for a in antinodes])
    else:
        min_x, min_y = 0, 0
    # draw map
    map = [['.' for x in range(min_x, max_x)] for y in range(min_y, max_y)]
    for antinode in [_ for _ in antinodes if in_bounds(_, min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y)]:
        map[antinode[1] - min_y][antinode[0] - min_x] = '#'
    for antenna in antennas:
        map[antenna.y - min_y][antenna.x - min_x] = antenna.frequency
    # print
    print("\n".join(["".join([cell for cell in line]) for line in map]))


def parse_input(path: str) -> Tuple[int, int, List[Antenna]]:
    antennas = []
    with open(path, 'r') as file:
        lines = file.read().splitlines()
    for y, line in enumerate(lines):
        for x, cell in enumerate(line):
            if cell != '.':
                antennas.append(Antenna(cell, x, y))
    return len(lines[0]), len(lines), antennas


def get_antinodes(antennas: List[Antenna]) -> List[Tuple[int, int]]:
    antinodes = set()
    for a1, a2 in combinations(antennas, 2):
        antinodes |= set(a1.antinodes(a2))
    return list(antinodes)


def get_antinodes2(antennas: List[Antenna], max_x: int, max_y: int) -> List[Tuple[int, int]]:
    antinodes = set()
    for a1, a2 in combinations(antennas, 2):
        antinodes |= set(a1.antinodes2(a2, max_x, max_y))
    return list({a for a in antinodes})


def in_bounds(coordinates: Tuple[int, int], max_x: int, max_y: int, min_x: int = 0, min_y: int = 0) -> bool:
    return min_x <= coordinates[0] < max_x and min_y <= coordinates[1] < max_y


if __name__ == '__main__':
    max_x, max_y, antennas = parse_input('input.txt')
    print('part 1')
    l = get_antinodes(antennas)
    l = [a for a in l if in_bounds(a, max_x, max_y)]
    print_map(antennas, antinodes=l, max_x=max_x, max_y=max_y)
    print(len(l))

    print('part 2')
    l = get_antinodes2(antennas, max_x, max_y)
    print_map(antennas, antinodes=l, max_x=max_x, max_y=max_y)
    print(len(l))
