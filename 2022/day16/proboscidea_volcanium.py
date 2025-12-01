import re
from dataclasses import dataclass
from typing import Dict, Optional


class Valve:
    def __init__(self, line: str):
        pattern = "Valve (..).*=(\d+); .*valve.? (.*)"
        groups = re.findall(pattern, line)
        self.name = groups[0][0]
        self.flow_rate = int(groups[0][1])
        connected_to = groups[0][2].split(', ')
        self.distances = {other_valve: 1 for other_valve in connected_to}

    def calculate_all_distances(self, all_valves: Dict[str, 'Valve']):
        current_round = list(self.distances.keys())
        distance = 1
        while current_round:
            next_round = set()
            for valve_name in current_round:
                valve = all_valves[valve_name]
                next_valves = {next_valve for (next_valve, distance) in valve.distances.items() if
                               distance == 1 and next_valve not in self.distances}
                next_round.update(next_valves)
            distance += 1
            for valve in next_round:
                self.distances[valve] = distance
            current_round = next_round

    def distance_to(self, other_valve: 'Valve'):
        return self.distances[other_valve.name]

    def calc_pressure_release(self, time_left: int) -> int:
        return self.flow_rate * time_left

    def __str__(self):
        return f'[Valve {self.name}, flow {self.flow_rate}, distances: {self.distances}]'

    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class Path:
    path: [Valve]
    time_left: int
    pressure_released: int

    @staticmethod
    def for_starting_pos(starting_pos: Valve, available_time: int) -> 'Path':
        path = [starting_pos]
        if starting_pos.flow_rate > 0:
            available_time -= 1
        pressure_released = starting_pos.calc_pressure_release(available_time)
        return Path(path, available_time, pressure_released)

    def extra_time_required(self, next_valve: Valve) -> int:
        travel_time = next_valve.distance_to(self.path[-1])
        if next_valve.flow_rate > 0:
            travel_time += 1
        return travel_time

    def time_left_when_added(self, next_valve: Valve) -> int:
        return self.time_left - self.extra_time_required(next_valve)

    def extra_pressure_released_when_added(self, next_valve: Valve) -> int:
        time_left_if_added = self.time_left_when_added(next_valve)
        return next_valve.calc_pressure_release(time_left_if_added)

    def extend(self, next_valve: Valve) -> Optional['Path']:
        next_time_left = self.time_left_when_added(next_valve)
        if next_time_left < 1:
            # next_valve has no time to release pressure after being opened, this is a useless extension
            return None
        next_path = self.path + [next_valve]
        next_pressure_released = self.pressure_released + next_valve.calc_pressure_release(next_time_left)
        return Path(next_path, next_time_left, next_pressure_released)

    def is_finished(self) -> bool:
        return self.time_left <= 2

    def __str__(self) -> str:
        return f'[Path ({", ".join([v.name for v in self.path])})]'

    def __repr__(self) -> str:
        return self.__str__()


def find_best_path(path: Path, closed_valves: [Valve]) -> Path:
    if path.is_finished():
        return path
    best_path = path
    for next_valve in closed_valves:
        if path.time_left_when_added(next_valve) <= 0:
            continue
        next_path = path.extend(next_valve)
        if next_path is None:
            continue
        next_closed_valves = [v for v in closed_valves if v != next_valve]
        best_next_path = find_best_path(next_path, next_closed_valves)
        if best_next_path.pressure_released > best_path.pressure_released:
            best_path = best_next_path
    return best_path


def pressure_from_paths(paths: (Path, Path)) -> int:
    return paths[0].pressure_released + paths[1].pressure_released


def find_best_paths(path1: Path, path2: Path, closed_valves: [Valve]) -> (Path, Path):
    is_root = (len(path1.path) + len(path2.path)) == 2

    if path1.is_finished() and path2.is_finished():
        return path1, path2
    if path1.is_finished():
        return path1, find_best_path(path2, closed_valves)
    if path2.is_finished():
        return find_best_path(path1, closed_valves), path2
    # extend the path with the most time left
    if path1.time_left >= path2.time_left:
        path_to_extend = path1
        path_to_remain = path2
    else:
        path_to_extend = path2
        path_to_remain = path1
    # extend with one valve
    best_paths = path1, path2
    i = 0
    for next_valve in closed_valves:
        if is_root:
            i += 1
            print(f'Currently in root at valve {i}/{len(closed_valves)}')
        if path_to_extend.time_left_when_added(next_valve) <= 0:
            continue
        next_path = path_to_extend.extend(next_valve)
        if next_path is None:
            continue
        next_closed_valves = [v for v in closed_valves if v != next_valve]
        best_next_paths = find_best_paths(next_path, path_to_remain, next_closed_valves)
        if pressure_from_paths(best_next_paths) > pressure_from_paths(best_paths):
            best_paths = best_next_paths
    return best_paths


if __name__ == '__main__':
    all_valves = {}
    with open('input.txt', 'r') as file:
        for line in file.read().splitlines():
            valve = Valve(line)
            all_valves[valve.name] = valve
    START_POS = all_valves["AA"]
    print('Calculating distances between all valves...')
    for valve in all_valves.values():
        valve.calculate_all_distances(all_valves)
    print('Getting which valves are functioning ...')
    valves_that_work = [valve for valve in all_valves.values() if valve.flow_rate > 0]
    print(f'Valves that actually work: {[valve.name for valve in valves_that_work]}')
    for v in valves_that_work:
        print(v)

    print("PART 1")
    time_left = 30
    starting_path = Path.for_starting_pos(START_POS, time_left)
    best_path = find_best_path(starting_path, valves_that_work)
    print(best_path.pressure_released)

    print("PART 2")
    available_time = 26
    starting_path = Path.for_starting_pos(START_POS, available_time)
    best_paths = find_best_paths(starting_path, starting_path, valves_that_work)
    print(pressure_from_paths(best_paths))
    print(best_paths[0])
    print(best_paths[1])
