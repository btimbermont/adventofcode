from dataclasses import dataclass


@dataclass
class MapPixel:
    x: int
    y: int
    height: int
    is_start: bool
    is_goal: bool
    distance_from_goal: int


class Map:
    def __init__(self, file_path: str):
        self._map: [[MapPixel]] = []
        self.all_pixels: [MapPixel] = []
        with open(file_path) as file:
            y = 0
            for line in file.read().splitlines():
                x = 0
                row = []
                for character in line:

                    is_start, is_goal = False, False
                    distance_from_goal = None
                    if character == 'S':
                        character = 'a'
                        is_start = True
                    elif character == 'E':
                        character = 'z'
                        is_goal = True
                        distance_from_goal = 0
                    height = ord(character) - ord('a')
                    pixel = MapPixel(x, y, height, is_start, is_goal, distance_from_goal)
                    row.append(pixel)
                    self.all_pixels.append(pixel)
                    if is_start:
                        self._start = pixel
                    if is_goal:
                        self._end = pixel
                    x += 1
                self._map.append(row)
                y += 1
        self._y_max = len(self._map) - 1
        self._x_max = len(self._map[0]) - 1

    def get_reachable_neighbors(self, pixel: MapPixel) -> [MapPixel]:
        x, y = pixel.x, pixel.y
        neighbors = []
        if x > 0:
            neighbors.append(self.pixel(x - 1, y))
        if x < self._x_max:
            neighbors.append(self.pixel(x + 1, y))
        if y > 0:
            neighbors.append(self.pixel(x, y - 1))
        if y < self._y_max:
            neighbors.append(self.pixel(x, y + 1))
        return [neighbor for neighbor in neighbors if neighbor.height - pixel.height >= -1]

    def pixel(self, x: int, y: int) -> MapPixel:
        return self._map[y][x]

    def distance_map(self) -> str:
        s = ''
        for y in range(self._y_max + 1):
            row = []
            for x in range(self._x_max + 1):
                pixel = self.pixel(x, y)
                row.append(str(pixel.distance_from_goal).zfill(3) if pixel.distance_from_goal is not None else '...')
            s += f'{" ".join(row)}\n'
        return s

    def calculate_distance_for_all_pixels(self):
        pixels_this_round = [self._end]
        while len(pixels_this_round) > 0:
            pixels_this_round = self._calculate_distance_round(pixels_this_round)

    def _calculate_distance_round(self, pixels_with_distance: [MapPixel] = None) -> [MapPixel]:
        if pixels_with_distance is None:
            pixels_with_distance = [self._end]
        updated_pixels = []
        for pixel in pixels_with_distance:
            neighbors_with_unknown_distance = [neighbor for neighbor in self.get_reachable_neighbors(pixel) if
                                               neighbor.distance_from_goal is None]
            for neighbor in neighbors_with_unknown_distance:
                neighbor.distance_from_goal = pixel.distance_from_goal + 1
                updated_pixels.append(neighbor)
        return updated_pixels

    def __str__(self) -> str:
        return '\n'.join([' '.join([str(pixel.height).zfill(2) for pixel in row]) for row in self._map])


if __name__ == '__main__':
    print('PART 1')
    map = Map('input.txt')
    map.calculate_distance_for_all_pixels()
    print(f'Shortest distance to end point from start: {map._start.distance_from_goal}')

    print('PART 2')
    possible_starting_positions = [pixel for pixel in map.all_pixels if
                                   pixel.height == 0 and pixel.distance_from_goal is not None]
    possible_starting_positions.sort(key=lambda p: p.distance_from_goal)
    print(f'Shortest distance to end point from any point with elevation a: {possible_starting_positions[0]}')
