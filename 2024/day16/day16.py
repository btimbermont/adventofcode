from dataclasses import dataclass
from typing import List

from advent_utils.two_d_utils import Point, Movement, turn_left, turn_right, String2dMap, MOVEMENTS


@dataclass
class Reindeer:
    location: Point
    direction: Movement
    score: int

    def copy(self) -> 'Reindeer':
        return Reindeer(self.location, self.direction, self.score)

    def advance(self) -> 'Reindeer':
        self.location = self.direction.apply(self.location)
        self.score += 1
        return self

    def turn_left(self) -> 'Reindeer':
        self.direction = turn_left(self.direction)
        self.score += 1000
        return self

    def turn_right(self) -> 'Reindeer':
        self.direction = turn_right(self.direction)
        self.score += 1000
        return self

    def next_possible_steps(self) -> List['Reindeer']:
        return [self.copy().advance(), self.copy().turn_left().advance(), self.copy().turn_right().advance()]


infinity = 100000000000000000000000000000000000


class ReindeerMap(String2dMap):
    def __init__(self, input_file: str):
        super().__init__(path=input_file)
        self.start = self.lookup_content('S')[0]
        self.end = self.lookup_content('E')[0]
        self.walls = self.lookup_content('#')

    def get_shortest_routes(self) -> List[List[Reindeer]]:
        reindeer_start = Reindeer(self.start, MOVEMENTS['>'], 0)
        shortest_distance_map = {}
        current_routes_to_explore = [[reindeer_start]]
        current_best_routes = []
        while current_routes_to_explore:
            next_routes_to_explore = []
            for route in current_routes_to_explore:
                visited_locations = [step.location for step in route]
                next_steps = [step for step in route[-1].next_possible_steps()
                              if step.location not in self.walls  # can't go through walls
                              and step.location not in visited_locations  # can't run in circles
                              and step.score - 1000 <= shortest_distance_map.get(step.location,
                                                                          infinity)  # give up if route isn't the most optimal to current point MINUS 1000 to account for possible turns!
                              and step.score <= shortest_distance_map.get(self.end,
                                                                          infinity)]  # give up if route isn't the most optimal to end
                # store scores
                for step in next_steps:
                    shortest_distance_map[step.location] = min(step.score, shortest_distance_map.get(step.location, infinity))
                    new_route = route.copy()
                    new_route.append(step)
                    if step.location == self.end:
                        current_best_routes = [r for r in current_best_routes if r[-1].score <= step.score]
                        current_best_routes.append(new_route)
                        break
                    else:
                        next_routes_to_explore.append(new_route)
            current_routes_to_explore = next_routes_to_explore
        return current_best_routes

    def print_route(self, route: List[Reindeer]):
        map = str(self)
        map = map.splitlines()
        map = [[cell for cell in line] for line in map]
        for step in route:
            x,y = step.location
            map[y][x] = step.direction.direction
        map[self.start[1]][self.start[0]] = 'S'
        map[self.end[1]][self.end[0]] = 'E'
        print("\n".join(["".join(line) for line in map]))


if __name__ == '__main__':
    map = ReindeerMap('input.txt')
    print('part 1')
    print(map)
    routes = map.get_shortest_routes()
    # for i, route in enumerate(routes):
    #     print(f'ROUTE {i}:')
    #     map.print_route(route)
    #     print("=============")
    print([route[-1].score for route in routes])
    print('part 2')
    all_tiles = {step.location for route in routes for step in route}
    print(len(all_tiles))
