import math
from itertools import combinations
from typing import Tuple, List, Dict

Point3D = Tuple[int, int, int]
infinity = 10000000000000000000000000000000000000


def euclidean_dist(a: Point3D, b: Point3D):
    x, y, z = math.pow(a[0] - b[0], 2), math.pow(a[1] - b[1], 2), math.pow(a[2] - b[2], 2)
    return math.sqrt(x + y + z)

def get_full_distance_list(points:[List[Point3D]]) -> List[Tuple[Point3D, Point3D, int]]:
    full_distance_list = []
    for a, b in combinations(points, 2):
        full_distance_list.append((a, b, euclidean_dist(a, b)))
    full_distance_list.sort(key=lambda x: x[2])
    return full_distance_list

def get_nearest_neighbor_map(points: List[Point3D]) -> Dict[Point3D, Tuple[Point3D, int]]:
    result = dict()
    for point in points:
        current_min_d = infinity
        current_min_point = None
        for other_point in points:
            if point != other_point:
                dist = euclidean_dist(point, other_point)
                if dist < current_min_d:
                    current_min_d = dist
                    current_min_point = other_point
        result[point] = current_min_point, current_min_d
    return result
