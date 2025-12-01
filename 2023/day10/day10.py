CHART = {}


def get_connected_tiles(current_pos: (int, int)) -> [(int, int)]:
    return [neighbor for neighbor in CHART[current_pos] if neighbor in CHART.keys() and current_pos in CHART[neighbor]]


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        grid = file.read()
    grid = grid.split()
    # make a chart that tells you where you can go from a given location
    animal_start_pos = None
    for y, line in enumerate(grid):
        for x, cell in enumerate(line.strip()):
            adjacent = []
            if cell in 'S-FL':  # can go right
                adjacent.append((x + 1, y))
            if cell in 'S-7J':  # can go left
                adjacent.append((x - 1, y))
            if cell in 'S|LJ':  # can go up
                adjacent.append((x, y - 1))
            if cell in 'S|7F':  # can go down
                adjacent.append((x, y + 1))
            if cell == 'S':
                animal_start_pos = (x, y)
            CHART[(x, y)] = adjacent

    print('part 1')
    visited = {animal_start_pos: 0}
    current = [animal_start_pos]
    while current:
        next_pipes = []
        for c in current:
            next_distance = 1 + visited[c]
            next_pipes_for_current = [n for n in get_connected_tiles(c) if n not in visited.keys()]
            for p in next_pipes_for_current:
                visited[p] = next_distance
            next_pipes.extend(next_pipes_for_current)
        current = next_pipes
    print(max(visited.values()))

    print('part 2')
    edge = [p for p in visited.keys()]
    inner_pixels = []
    for y in range(len(grid)):
        outside_shape = True
        on_edge = False
        last_corner = None
        for x in range(len(grid[0])):
            current_pixel = (x, y)
            if current_pixel in edge:
                # TODO: S is now hardcoded equal to |, this works for my input, but isn't correct
                if grid[y][x] in '|S':  # always flip state: if we cross this, we go from outside to inside or reverse
                    outside_shape = not outside_shape
                elif grid[y][
                    x] in 'LF':  # we enter a horizontal part of the edge: store this corner to determine later how the bend went
                    last_corner = grid[y][x]
                elif grid[y][x] in '7J':  # we exit a horizontal part of th edge: see how the bend went
                    if grid[y][x] == '7' and last_corner == 'L':  # these two together are like a |
                        outside_shape = not outside_shape
                    if grid[y][x] == 'J' and last_corner == 'F':  # these two together are like a |
                        outside_shape = not outside_shape
                    last_corner = None
            else:
                if not outside_shape:
                    inner_pixels.append(current_pixel)
    print(inner_pixels)
    print(len(inner_pixels))
