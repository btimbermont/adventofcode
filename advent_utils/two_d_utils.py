from dataclasses import dataclass
from typing import Tuple, Optional, List, Callable, Dict


def read_file(path: str):
    with open(path, 'r') as file:
        return file.read()


Point = Tuple[int, int]
Route = List[Point]
infinity = 1000000000000000000000000000000000000000000000


def get_neighbors(point: Point, include_diagonals:bool=False) -> List[Point]:
    x, y = point
    up = x, y - 1
    right = x + 1, y
    down = x, y + 1
    left = x - 1, y
    neighbors = [up, right, down, left]
    if include_diagonals:
        tl = x-1, y-1
        tr = x+1, y-1
        bl = x-1, y+1
        br = x+1, y+1
        neighbors += [tl, tr, bl, br]
    return neighbors


def manhattan_dist(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


@dataclass
class Movement:
    direction: str
    name: str
    apply: Callable[[Point], Point]


MOVEMENTS = {
    '^': Movement('^', 'up', lambda p: (p[0], p[1] - 1)),
    '>': Movement('>', 'right', lambda p: (p[0] + 1, p[1])),
    'v': Movement('v', 'down', lambda p: (p[0], p[1] + 1)),
    '<': Movement('<', 'left', lambda p: (p[0] - 1, p[1]))
}
directions = '^>v<'


def turn_right(movement: Movement) -> Movement:
    i = directions.index(movement.direction)
    return MOVEMENTS[directions[(i + 1) % 4]]


def turn_left(movement: Movement) -> Movement:
    i = directions.index(movement.direction)
    return MOVEMENTS[directions[(i - 1) % 4]]


class String2dMap:
    def __init__(self, path: str = None, input: str = None, wall_characters: str = '#'):
        if not (path or input):
            raise ValueError("Map needs some input!")
        if not input:
            input = read_file(path)
        self.map = [[c for c in line] for line in input.splitlines()]
        self.max_y = len(self.map)
        self.max_x = len(self.map[0])
        self.lookup = dict()
        self.wall_characters = wall_characters
        for y, line in enumerate(self.map):
            for x, content in enumerate(line):
                points = self.lookup.get(content, set())
                points.add((x, y))
                self.lookup[content] = points

    def copy(self):
        return String2dMap(input = str(self), wall_characters=self.wall_characters)

    def get_cell(self, point: Point) -> Optional[str]:
        x, y = point
        if y < 0 or y >= len(self.map) or x < 0 or x >= len(self.map[y]):
            return None
        return self.map[y][x]

    def set_cell(self, point: Point, new_content: str):
        old_cell = self.get_cell(point)
        if not old_cell:
            return
        x, y = point
        self.map[y][x] = new_content
        self.lookup[old_cell].remove(point)
        points = self.lookup.get(new_content, set())
        points.add(point)
        self.lookup[new_content] = points

    def lookup_content(self, cell: str) -> List[Point]:
        return list(self.lookup.get(cell))

    def get_neighbors(self, point: Point, filter_outside: bool = True, include_diagonals: bool = False) -> List[Point]:
        neighbors = [(x, y) for x, y in get_neighbors(point, include_diagonals) if
                     not filter_outside or (0 <= y < self.max_y and 0 <= x < self.max_x)]
        return neighbors

    def set_wall(self, wall_characters: str):
        self.wall_characters = wall_characters

    def is_wall(self, point: Point):
        return self.get_cell(point) and self.get_cell(point) in self.wall_characters

    def _get_shortest_distance_map(self, start: Point, end: Point) -> Dict[Point, int]:
        shortest_distance_map = {start: 0}
        added_points = {start}
        distance = 0
        while added_points:
            next_points = {neighbor for point in added_points for neighbor in get_neighbors(point)
                           if neighbor not in shortest_distance_map.keys()
                           and 0 <= neighbor[0] < self.max_x
                           and 0 <= neighbor[1] < self.max_y
                           and not self.is_wall(neighbor)}
            next_points = list(next_points)
            distance += 1
            for p in next_points:
                shortest_distance_map[p] = distance
                if p == end:
                    break
            added_points = next_points
        return shortest_distance_map

    def get_shortest_distance(self, start: Point, end: Point) -> Optional[int]:
        return self._get_shortest_distance_map(start, end).get(end, None)

    def get_shortest_routes(self, start: Point, end: Point) -> List[Route]:
        distance_map = self._get_shortest_distance_map(start, end)
        routes = [[end]]
        current_distance = distance_map.get(end)
        while current_distance > 0:
            current_distance -= 1
            new_routes = []
            for r in routes:
                next_points = [p for p in get_neighbors(r[0])
                               if not self.is_wall(p)
                               and distance_map[p] == current_distance]
                new_routes = new_routes + [[p] + r for p in next_points]
            routes = new_routes
        return routes

    def all_points(self) -> List[Point]:
        return [(x, y) for y in range(self.max_y) for x in range(self.max_x)]

    def __str__(self):
        return "\n".join(["".join(line) for line in self.map])

    def print_route(self, route: Route) -> str:
        return self.print_with_override({p: 'O' for p in route})

    def print_with_override(self, overrides: Dict[Point, str]):
        output = [[cell for cell in line] for line in str(self).splitlines()]
        for p, v in overrides.items():
            x, y = p
            output[y][x] = v
        return "\n".join(["".join(line) for line in output])


class Vector(Tuple[int, int]):
    def __new__(cls, x: int, y: int):
        return tuple.__new__(Vector, (x, y))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    def __add__(self, other):
        if not isinstance(other, Tuple):
            raise ValueError("cannot add vector to something that isn't another vector or tuple")
        return Vector(self.x + other[0], self.y + other[1])

    def scale(self, scale: int) -> 'Vector':
        return Vector(scale * self.x, scale * self.y)


if __name__ == '__main__':
    print(get_neighbors((0,0)))
    print(get_neighbors((0,0), True))
