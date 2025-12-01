from typing import Tuple

Position = (int, int, int)


def get_neighbors(position: Position) -> [Position]:
    neighbors = []
    for i in [-1, 1]:
        neighbors.append((position[0] + i, position[1], position[2]))
        neighbors.append((position[0], position[1] + i, position[2]))
        neighbors.append((position[0], position[1], position[2] + i))
    return neighbors


def calc_free_sides(position: Position, shape: [Position]):
    adjacent_droplets = [p for p in get_neighbors(position) if p in shape]
    return 6 - len(adjacent_droplets)


def get_outer_bounds(object_scan: [Position]) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
    min_x = min_y = min_z = 1000000
    max_x = max_y = max_z = -1000000
    for p in object_scan:
        min_x = min(min_x, p[0])
        min_y = min(min_y, p[1])
        min_z = min(min_z, p[2])
        max_x = max(max_x, p[0])
        max_y = max(max_y, p[1])
        max_z = max(max_z, p[2])
    return (min_x - 1, max_x + 1), (min_y - 1, max_y + 1), (min_z - 1, max_z + 1)


def is_in_bounds(pos: Position, x_bounds: (int, int), y_bounds: (int, int), z_bounds: (int, int)):
    return x_bounds[0] <= pos[0] <= x_bounds[1] and \
           y_bounds[0] <= pos[1] <= y_bounds[1] and \
           z_bounds[0] <= pos[2] <= z_bounds[1]


def get_outside_air(shape: [Position]) -> [Position]:
    x_bounds, y_bounds, z_bounds = get_outer_bounds(shape)
    # start from one outer bound point and then 'expand' the outer air and see how far we get
    outside_air = set()
    next_round = {(x_bounds[0], y_bounds[0], z_bounds[0])}
    current_round = {}
    while next_round:
        current_round = next_round
        next_round = set()
        for current_pos in current_round:
            outside_air.add(current_pos)
            neighbors = [n for n in get_neighbors(current_pos) if
                         is_in_bounds(n, x_bounds, y_bounds, z_bounds) and n not in outside_air
                         and n not in current_round and n not in shape]
            next_round.update(neighbors)

    return outside_air


def calc_shape_surface(shape: [Position]):
    outside_air = get_outside_air(shape)
    s = 0
    for pos in shape:
        outside_air_neighbors = [n for n in get_neighbors(pos) if n in outside_air]
        s += len(outside_air_neighbors)
    return s


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        scanned_shape = [eval(line) for line in file.read().splitlines()]

    print('PART 1')
    sides = 0
    for droplet in scanned_shape:
        sides += calc_free_sides(droplet, scanned_shape)
    print(f'total free sides: {sides}')

    print('PART 2')
    # scanned_shape = [(1,1,1), (1,1,2), (1,1,3), (1,2,2)]
    print(calc_shape_surface(scanned_shape))
