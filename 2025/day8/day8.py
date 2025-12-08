from typing import List, Set

from advent_utils.three_d_utils import get_nearest_neighbor_map

if __name__ == '__main__':
    points = []
    with open('test_input.txt', 'r') as file:
        for line in file:
            point = tuple([int(a) for a in line.strip().split(',')])
            points.append(point)

    print('part 1')
    connections = 10

    nearest_neighbor_map = get_nearest_neighbor_map(points)
    distance_map = dict()
    for key, value in nearest_neighbor_map.items():
        point_a = key
        point_b, dist = value
        distance_map[dist] = point_a, point_b
    shortest_distances = list(sorted(distance_map.keys()))[:connections]
    circuits: List[Set] = []
    for d in shortest_distances:
        junction_a, junction_b = distance_map[d]
        existing_circuit = None
        for circuit in circuits:
            if junction_a in circuit or junction_b in circuit:
                existing_circuit = circuit
        if existing_circuit:
            existing_circuit.add(junction_a)
            existing_circuit.add(junction_b)
        else:
            new_circuit = set()
            new_circuit.add(junction_a)
            new_circuit.add(junction_b)
            circuits.append(new_circuit)
    print([len(c) for c in circuits])  # still wrong
