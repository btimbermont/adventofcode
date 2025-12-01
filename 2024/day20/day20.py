from typing import Dict

from advent_utils.two_d_utils import String2dMap, manhattan_dist


def get_cheats(map: String2dMap, cheat_duration: int = 2, minimum_advantage: int = 2) -> Dict[int, int]:
    start = map.lookup_content('S')[0]
    end = map.lookup_content('E')[0]
    route = map.get_shortest_routes(start, end)[0]
    shortest_distance_map = map._get_shortest_distance_map(start, end)
    cheats = dict()
    for i, p in enumerate(route):
        if i % 100 == 0:
            print(f'investigating point {i} of {len(route)}')
        p_dist = shortest_distance_map.get(p, -1000000000)
        advantages_for_this_point = [(x, (shortest_distance_map[x] - p_dist) - (manhattan_dist(p, x))) for x in route
                                     if 2 <= manhattan_dist(p, x) <= cheat_duration
                                     and minimum_advantage <= (shortest_distance_map[x] - p_dist) - (
                                         manhattan_dist(p, x))]
        for destination, advantage in advantages_for_this_point:
            cheats[advantage] = cheats.get(advantage, 0) + 1
    return cheats


if __name__ == '__main__':
    map = String2dMap(path='input.txt')
    start = map.lookup_content('S')[0]
    end = map.lookup_content('E')[0]

    print('part 1')
    cheats = get_cheats(map, minimum_advantage=100)
    for k, v in sorted(cheats.items()):
        print(f'There are {v} cheats that save you {k} ps')
    print(f'solution: {sum(cheats.values())}')

    print('part 2')
    cheats = get_cheats(map, cheat_duration=20, minimum_advantage=100)
    for k, v in sorted(cheats.items()):
        print(f'There are {v} cheats that save you {k} ps')
    print(f'solution: {sum(cheats.values())}')
