import time
from copy import deepcopy
from itertools import combinations


def taxi_distance(a: (int, int), b: (int, int)):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def intervals_overlap(a: (int, int), b: (int, int)) -> bool:
    return not (a[0] > b[1] or a[1] < b[0])


def merge_intervals(a: (int, int), b: (int, int)) -> (int, int):
    if not intervals_overlap(a, b):
        raise Exception(f'Cannot merge non-overlapping intervals {a} and {b}')
    return min(a[0], b[0]), max(a[1], b[1])


def merge_intervals_list(intervals: [(int, int)]) -> [(int, int)]:
    intervals_to_merge = sorted(intervals, key=lambda interval: interval[0])
    merged_intervals = [intervals_to_merge[0]]
    for next_interval in intervals_to_merge[1:]:
        if intervals_overlap(next_interval, merged_intervals[-1]):
            merged_intervals[-1] = merge_intervals(next_interval, merged_intervals[-1])
        else:
            merged_intervals.append(next_interval)
    return merged_intervals


class Sensor:
    def __init__(self, line: str):
        sensor, beacon = line.split(':')
        self.sensor = tuple([int(s.split('=')[1]) for s in sensor.split(', ')[-2:]])
        self.beacon = tuple([int(s.split('=')[1]) for s in beacon.split(', ')[-2:]])
        # calc bounds
        self.radius = taxi_distance(self.sensor, self.beacon)
        self.min_x = self.sensor[0] - self.radius
        self.max_x = self.sensor[0] + self.radius
        self.min_y = self.sensor[1] - self.radius
        self.max_y = self.sensor[1] + self.radius

    def pos_is_in_range(self, pos: (int, int)):
        return taxi_distance(pos, self.sensor) <= self.radius

    def range_at_row(self, y: int) -> (int, int):
        if self.min_y <= y <= self.max_y:
            range_at_y = self.radius - abs(self.sensor[1] - y)
            min_x_at_y = self.sensor[0] - range_at_y
            max_x_at_y = self.sensor[0] + range_at_y
            return min_x_at_y, max_x_at_y
        return None


class Map:
    def __init__(self, sensors: [Sensor]):
        self.sensors = sensors
        self.sensor_locations = [sensor.sensor for sensor in sensors]
        self.beacon_locations = set([sensor.beacon for sensor in sensors])
        # calc bounds
        self.min_x = min([sensor.min_x for sensor in sensors])
        self.max_x = max([sensor.max_x for sensor in sensors])
        self.min_y = min([sensor.min_y for sensor in sensors])
        self.max_y = max([sensor.max_y for sensor in sensors])
        print(f'bounds of map: {self.min_x, self.min_y} - {self.max_x, self.max_y}')

    def count_known_beacon_free_positions_new(self, y: int, x_bounds: (int, int) = None) -> int:
        if x_bounds is None:
            x_bounds = self.min_x, self.max_x
        # count scanned positions on this row:
        scanned_positions = self.count_scanned_positions_on_row(y, x_bounds)
        # those can include known beacons, which are always in scanned territory, so subtract those:
        beacons_on_row = [b for b in self.beacon_locations if b[1] == y and b[0] in range(x_bounds[0], x_bounds[1] + 1)]
        return scanned_positions - len(beacons_on_row)

    def count_scanned_positions_on_row(self, y: int, x_bounds: (int, int) = None) -> int:
        if x_bounds is None:
            x_bounds = self.min_x, self.max_x
        scanned_intervals_at_row = self.get_scanned_intervals_at_row(y, x_bounds)
        i = sum([interval[1] - interval[0] + 1 for interval in scanned_intervals_at_row])
        return i

    def get_scanned_intervals_at_row(self, y, x_bounds):
        scanned_intervals_at_row = []
        for sensor in self.sensors:
            scanned_interval = sensor.range_at_row(y)
            if scanned_interval is not None and intervals_overlap(scanned_interval, x_bounds):
                # we should add it to the list, after adjusting its bounds
                scanned_intervals_at_row.append(
                    (max(x_bounds[0], scanned_interval[0]), min(x_bounds[1], scanned_interval[1])))
        # print(f'Scanned íntervals at row {y}: {scanned_intervals_at_row}')
        scanned_intervals_at_row = merge_intervals_list(scanned_intervals_at_row)
        # print(f'Merged íntervals at row {y}: {scanned_intervals_at_row}')
        return scanned_intervals_at_row

    def get_unscanned_intervals_at_row(self, y, x_bounds):
        scanned = self.get_scanned_intervals_at_row(y, x_bounds)
        if len(scanned) == 0:
            return deepcopy(x_bounds);
        unscanned = []
        if x_bounds[0] < scanned[0][0]:
            unscanned.append((x_bounds[0], scanned[0][0]))
        for left_interval, right_interval in combinations(scanned, 2):
            unscanned.append((left_interval[1] + 1, right_interval[0] - 1))
        if scanned[-1][1] < x_bounds[1]:
            unscanned.append((scanned[1][1], x_bounds[1]))
        return unscanned

    def count_unscanned_positions_on_row(self, y: int, x_bounds: (int, int) = None) -> int:
        if x_bounds is None:
            x_bounds = self.min_x, self.max_x
        positions_we_care_about = x_bounds[1] - x_bounds[0] + 1
        return positions_we_care_about - self.count_scanned_positions_on_row(y, x_bounds)

    def find_first_unscanned_position(self, y_bounds: (int, int) = None, x_bounds: (int, int) = None):
        if x_bounds is None:
            x_bounds = self.min_x, self.max_x
        if y_bounds is None:
            y_bounds = self.min_y, self.max_y
        for y in range(y_bounds[0], y_bounds[1] + 1):
            if (y - y_bounds[0]) % 100000 == 0:
                print(f'Currently at row {y}')
            unscanned_intervals = self.get_unscanned_intervals_at_row(y, x_bounds)
            if len(unscanned_intervals) > 0:
                print(f'unscanned area found at row {y}: {unscanned_intervals}')
                first_x = unscanned_intervals[0][0]
                print(f'Tuning frequency of first unscanned position: {first_x * 4000000 + y}')
                return


if __name__ == '__main__':
    print('PART 1')
    # line_to_get = 10
    line_to_get = 2000000
    with open('input.txt', 'r') as file:
        sensors = [Sensor(line) for line in file.read().splitlines()]
    m = Map(sensors)
    tic = time.perf_counter()
    print(
        f'Line {line_to_get} has {m.count_known_beacon_free_positions_new(line_to_get)} positions that we know don\'t have a beacon')
    toc = time.perf_counter()
    print(f'analyzed row in {toc - tic:0.1f} seconds')

    print('PART 2')
    # bounds = 0, 20
    bounds = 0, 4000000
    m.find_first_unscanned_position(bounds, bounds)
