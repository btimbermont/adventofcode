from itertools import combinations

from advent_utils.two_d_utils import Point, Rectangle


def area_between(a: Point, b: Point):
    return abs((a[0] - b[0] + 1) * (a[1] - b[1] + 1))


if __name__ == '__main__':
    points = []
    with open('input.txt', 'r') as file:
        for line in file:
            points.append(tuple([int(a) for a in line.strip().split(',')]))

    print('part 1')
    rectangles = [Rectangle(a,b) for a, b in combinations(points, 2)]
    rectangles.sort(key=lambda r:r.area, reverse=True)
    print(rectangles[0])

    print('part 2')
    for rectangle in rectangles:
        overlaps = False
        for i in range(len(points)):
            p1 = points[i-1]
            p2 = points[i]
            line = Rectangle(p1, p2)
            if rectangle.overlaps(line):
                overlaps = True
                break
        if not overlaps:
            print(f'SOLUTION: {rectangle}')
            break
