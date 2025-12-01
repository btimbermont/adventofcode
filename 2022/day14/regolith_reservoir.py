from copy import deepcopy
from typing import Union, Tuple, Optional


def point_between(start: (int, int), end: (int, int)) -> [(int, int)]:
    all_points = []
    if start[0] == end[0]:
        # change y
        for i in range(min(start[1], end[1]) + 1, max(start[1], end[1])):
            all_points.append((start[0], i))
    elif start[1] == end[1]:
        # change x
        for i in range(min(start[0], end[0]) + 1, max(start[0], end[0])):
            all_points.append((i, start[1]))
    else:
        raise Exception(f'Diagonal lines aren\'t supported: {start}, {end}')
    return all_points


class RockFormation:
    def __init__(self, corners: [(int, int)]):
        self.all_rocks = []
        for start, end in zip(corners, corners[1:]):
            self.all_rocks.append(start)
            self.all_rocks += point_between(start, end)
        self.all_rocks.append(corners[-1])


def parse_rock_formation(line: str) -> RockFormation:
    corners = []
    for coordinate in line.split(' -> '):
        x, y = coordinate.split(',')
        corners.append((int(x), int(y)))
    return RockFormation(corners)


class Cave:
    def __init__(self, rock_formations: [RockFormation], generate_floor: bool = False):
        self.sand_source = (500, 0)
        rocks = [rock for formation in rock_formations for rock in formation.all_rocks]
        # find bounds of cave
        self.min_x = min([rock[0] for rock in rocks])
        self.max_x = max([rock[0] for rock in rocks])
        self.min_y = 0
        self.max_y = max([rock[1] for rock in rocks])
        # generate floor
        if generate_floor:
            self.min_x = min(self.min_x, self.sand_source[0] - self.max_y)
            self.max_x = max(self.max_x, self.sand_source[0] + self.max_y)
        # create grid
        self.grid = []
        # add some bounds
        self.min_x -=2
        self.max_x +=2
        self.max_y +=2
        for y in range(self.min_y, self.max_y + 1):
            row = []
            for x in range(self.min_x, self.max_x + 1):
                character = '.'  # default: air
                if (x, y) == self.sand_source:
                    character = '+'
                elif (x, y) in rocks:
                    character = '#'
                elif generate_floor and y == self.max_y:
                    character = '#'
                row.append(character)
            self.grid.append(row)

    def drop_sand(self) -> Optional[Tuple[int, int]]:
        if self.get_content(self.sand_source) != '+':
            print('Sand can no longer drop!')
            return None  # if no sand can be dropped
        path = [deepcopy(self.sand_source)]
        while True:
            next_position = self.position_below(path[-1])
            if next_position is None:
                break
            if next_position == 'Abyss!':
                print('Sand fell into the abyss!')
                # register the abyss path
                for pos in path[1:]:
                    self.set_content(pos, '~')
                return None
            path.append(next_position)
        self.set_content(path[-1], 'o')
        return path[-1]

    def position_below(self, position: (int, int)) -> Union[Tuple[int, int], str, None]:
        x, y = position
        if y == self.max_y:
            return 'Abyss!'
        y += 1
        # directly below
        if self.get_content((x, y)) in '.~':
            return x, y
        # left or right
        if x == self.min_x or x == self.max_x:
            return 'Abyss!'
        # left below first, then right below
        if self.get_content((x - 1, y)) in '.~':
            return x - 1, y
        if self.get_content((x + 1, y)) in '.~':
            return x + 1, y
        return None  # can't drop anymore

    def get_content(self, position: (int, int)) -> str:
        x, y = position
        if self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y:
            x -= self.min_x
            y -= self.min_y
            return self.grid[y][x]
        return None

    def set_content(self, position: (int, int), char: str):
        x, y = position
        x -= self.min_x
        y -= self.min_y
        self.grid[y][x] = char

    def __str__(self):
        rows = []
        for row in self.grid:
            rows.append(''.join(row))
        return '\n'.join(rows)


if __name__ == '__main__':
    print('PART 1')
    with open('test_input.txt') as file:
        print('Parsing rock formations...')
        formations = [parse_rock_formation(line) for line in file.read().splitlines()]
    print('Parsing cave...')
    cave = Cave(formations)
    print('Done!')
    # print(cave)
    while cave.drop_sand() is not None:
        pass
    print(cave)
    sands = 0
    for c in cave.__str__():
        if c == 'o':
            sands += 1
    print(f'sand: {sands}')

    print('PART 2')
    with open('input.txt') as file:
        print('Parsing rock formations...')
        formations = [parse_rock_formation(line) for line in file.read().splitlines()]
    print('Parsing cave...')
    cave = Cave(formations, generate_floor=True)
    while cave.drop_sand() is not None:
        pass
    print(cave)
    sands = 0
    for c in cave.__str__():
        if c == 'o':
            sands += 1
    print(f'sand: {sands}')
