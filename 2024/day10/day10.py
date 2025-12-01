from typing import Optional, Tuple, List

Point = Tuple[int, int]
Route = List[Point]


class TopoMap:
    def __init__(self, input: str):
        # parse input
        self.map = [[int(c) for c in line] for line in input.splitlines()]
        self.height_lookup = {}
        for y, line in enumerate(self.map):
            for x, height in enumerate(line):
                points = self.height_lookup.get(height, [])
                points.append((x, y))
                self.height_lookup[height] = points

    def get_height(self, point: Point) -> Optional[int]:
        x, y = point
        if y < 0 or y >= len(self.map) or x < 0 or x >= len(self.map[y]):
            return None
        return self.map[y][x]

    def get_trail_starts(self) -> list[Point]:
        return self.height_lookup[0]

    def get_neighbors(self, point: Point) -> List[Point]:
        x, y = point
        up = x, y - 1
        down = x, y + 1
        left = x - 1, y
        right = x + 1, y
        return [(x, y) for x, y in [up, right, down, left] if 0 <= y < len(self.map) and 0 <= x < len(self.map[y])]

    def get_nextstep(self, current_point: Point) -> List[Point]:
        current_height = self.get_height(current_point)
        return [p for p in self.get_neighbors(current_point) if self.get_height(p) == current_height + 1]

    def extend_route(self, route: Route) -> List[Route]:
        result = []
        for step in self.get_nextstep(route[-1]):
            new_route = route.copy()
            new_route.append(step)
            result.append(new_route)
        return result

    def deduplicate(self, routes: List[Route]) -> List[Route]:
        route_index = {(route[0], route[-1]): route for route in routes}
        return list(route_index.values())

    def get_routes(self, dedup: bool = True):
        # get starting routes
        routes_to_explore = [[p] for p in self.get_trail_starts()]
        finished_routes = []
        while routes_to_explore:
            updated_routes = []
            for route in routes_to_explore:
                if self.get_height(route[-1]) == 9:
                    finished_routes.append(route)
                else:
                    updated_routes += self.extend_route(route)
            if dedup:
                routes_to_explore = self.deduplicate(updated_routes)
            else:
                routes_to_explore = updated_routes
        return finished_routes


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        topo = TopoMap(file.read())
    print('part 1')
    routes = topo.get_routes()
    print(len(routes))
    print('part 2')
    routes = topo.get_routes(dedup=False)
    print(len(routes))
