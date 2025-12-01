from dataclasses import dataclass
from itertools import combinations


@dataclass
class Galaxy:
    i: int
    x: int
    y: int


def dist(a: Galaxy, b: Galaxy) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def expand_universe(galaxies: [Galaxy], expansion: int = 2):
    min_x, max_x = min([g.x for g in galaxies]), max([g.x for g in galaxies])
    min_y, max_y = min([g.y for g in galaxies]), max([g.y for g in galaxies])
    print(f'Expanding universe, bounds: {(min_x, min_y)}, {(max_x, max_y)}')
    # step 1: x
    for x in range(max_x, min_x - 1, -1):
        if x not in [g.x for g in galaxies]:
            # print(f'no galaxy with x = {x}, expanding that column')
            for galaxy in galaxies:
                if galaxy.x > x:
                    galaxy.x += expansion - 1
    # step 2: y
    for y in range(max_y, min_y - 1, -1):
        if y not in [g.y for g in galaxies]:
            # print(f'no galaxy with y = {y}, expanding that row')
            for galaxy in galaxies:
                if galaxy.y > y:
                    galaxy.y += expansion - 1


if __name__ == '__main__':
    print('part 1')
    galaxies = []
    i = 1
    with open('input.txt', 'r') as file:
        for y, line in enumerate(file):
            for x, c in enumerate(line):
                if c == '#':
                    galaxies.append(Galaxy(i, x, y))
                    i += 1
    expand_universe(galaxies)
    result = 0
    for g1, g2 in combinations(galaxies, 2):
        result += dist(g1, g2)
    print(result)

    print('part 2')
    galaxies = []
    i = 1
    with open('input.txt', 'r') as file:
        for y, line in enumerate(file):
            for x, c in enumerate(line):
                if c == '#':
                    galaxies.append(Galaxy(i, x, y))
                    i += 1
    expand_universe(galaxies, expansion=1000000)
    result = 0
    for g1, g2 in combinations(galaxies, 2):
        result += dist(g1, g2)
    print(result)
