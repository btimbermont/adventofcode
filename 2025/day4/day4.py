from typing import List

from advent_utils.two_d_utils import String2dMap, Point


def get_accessible_rolls(map: String2dMap) -> List[Point]:
    access_rolls = []
    for roll in map.lookup_content('@'):
        neighbors = map.get_neighbors(roll, include_diagonals=True)
        neighboring_rolls = len([n for n in neighbors if map.get_cell(n) == '@'])
        if neighboring_rolls < 4:
            access_rolls.append(roll)
    return access_rolls


if __name__ == '__main__':
    map = String2dMap('input.txt')
    print("part 1")
    print(len(get_accessible_rolls(map)))

    print("part 2")
    removed_rolls = 0
    rolls_to_remove = get_accessible_rolls(map)
    while rolls_to_remove:
        for roll in rolls_to_remove:
            map.set_cell(roll, 'x')
        removed_rolls += len(rolls_to_remove)
        print(f'removed {len(rolls_to_remove)} rolls')
        print(map)
        for roll in rolls_to_remove:
            map.set_cell(roll, '.')
        rolls_to_remove = get_accessible_rolls(map)
    print(f'Removed {removed_rolls} in total')
