from itertools import combinations

from advent_utils.two_d_utils import Point

def area_between(a:Point, b:Point):
    return abs((a[0]-b[0]+1) * (a[1]-b[1]+1))

if __name__ == '__main__':
    points = []
    with open('input.txt', 'r') as file:
        for line in file:
            points.append(tuple([int(a) for a in line.strip().split(',')]))

    print('part 1')
    pairs = [(a,b, area_between(a,b)) for a,b in combinations(points, 2)]
    max_area = max(pairs, key=lambda i:i[2])
    print(max_area)

    print('part 2')
    red_tiles = points
    green_tiles = []
    for i in range(len(red_tiles)):
        tile1, tile2 = red_tiles[i-1], red_tiles[i]
        if tile1[0] == tile2[0]:
            ...
        elif tile1[0] == tile2[0]:
            ...