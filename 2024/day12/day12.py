from typing import List

from advent_utils.two_d_utils import String2dMap, Point, get_neighbors


def split_in_plots(garden: String2dMap) -> List[List[Point]]:
    plots = []
    points_in_plot = []
    for point in garden.all_points():
        if point in points_in_plot:
            continue
        plot_type = garden.get_cell(point)
        plot = [point]
        get_neighbors_from = [point]
        while get_neighbors_from:
            get_neighbors_from = list({n for p in get_neighbors_from
                                       for n in garden.get_neighbors(p)
                                       if garden.get_cell(n) == plot_type and n not in plot})
            plot += get_neighbors_from
        plots.append(plot)
        points_in_plot += plot
    return plots


def calc_plot_cost(plot: List[Point], print_price: bool = False) -> int:
    size = len(plot)
    perimeter = 0
    for point in plot:
        perimeter += len([p for p in get_neighbors(point) if p not in plot])
    if print_price:
        print(f'plot {plot} size {size} perimeter {perimeter} cost {size * perimeter}')
    return size * perimeter


def calc_plot_cost2(plot: List[Point], print_price: bool = False) -> int:
    size = len(plot)
    sides = 0
    min_x = min([p[0] for p in plot])
    max_x = max([p[0] for p in plot])
    min_y = min([p[1] for p in plot])
    max_y = max([p[1] for p in plot])
    # count vertical sides
    for x in range(min_x, max_x + 2):
        l, r = False, False  # left, right: indicate whether left/right cell are part of plot
        for y in range(min_y, max_y + 1):
            left = (x - 1, y) in plot
            right = (x, y) in plot
            if (l, r) == (left, right):
                # nothing changed since last cell
                continue
            # something changed in the state: see if we need a fence between these cells
            edge_now = left != right
            if edge_now:
                sides += 1
            l, r = left, right
    # count horizontal sides, same as above but horizontal
    for y in range(min_y, max_y + 2):
        t, d = False, False  # top, down
        for x in range(min_x, max_x + 1):
            top = (x, y - 1) in plot
            down = (x, y) in plot
            if (t, d) == (top, down):
                continue
            # something changed in the state: see if we need a fence between these cells
            edge_now = top != down
            if edge_now:
                sides += 1
            t, d = top, down
    if print_price:
        print(f'plot {plot} size {size} sides {sides} cost {size * sides}')
    return size * sides


if __name__ == '__main__':
    garden = String2dMap(path='input.txt')
    print('part 1')
    plots = split_in_plots(garden)
    print(sum([calc_plot_cost(plot, print_price=False) for plot in plots]))
    print('part 2')
    plots = split_in_plots(garden)
    print(sum([calc_plot_cost2(plot, print_price=False) for plot in plots]))
