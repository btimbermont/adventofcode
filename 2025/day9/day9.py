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