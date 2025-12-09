import math
from itertools import combinations

from advent_utils.three_d_utils import euclidean_dist, get_full_distance_list

if __name__ == '__main__':
    points = []
    with open('input.txt', 'r') as file:
        for line in file:
            point = tuple([int(a) for a in line.strip().split(',')])
            points.append(point)

    print('part 1')
    connections = 1000
    print('Calculating all distances...')
    full_distance_list = get_full_distance_list(points)
    connected_junctions = dict()
    for junction_a, junction_b, dist in full_distance_list:
        circuit_a = connected_junctions.get(junction_a)
        circuit_b = connected_junctions.get(junction_b)

        if circuit_a is None and circuit_b is None:
            new_circuit = [junction_a, junction_b]
            connected_junctions[junction_a] = new_circuit
            connected_junctions[junction_b] = new_circuit
        elif circuit_a is None:
            circuit_b.append(junction_a)
            connected_junctions[junction_a] = circuit_b
        elif circuit_b is None:
            circuit_a.append(junction_b)
            connected_junctions[junction_b] = circuit_a
        elif circuit_a != circuit_b:
            circuit_a.extend(circuit_b)
            for junction in circuit_b:
                connected_junctions[junction] = circuit_a
        connections -= 1
        if connections == 0:
            break
    all_circuits = list(set([tuple(circuit) for circuit in connected_junctions.values()]))
    all_circuits.sort(key=lambda c: -len(c))
    circuit_sizes = [len(c) for c in all_circuits]
    print(circuit_sizes)
    print(math.prod(circuit_sizes[:3]))

    print('part 2')
    connected_junctions = dict()
    for junction_a, junction_b, dist in full_distance_list:
        circuit_a = connected_junctions.get(junction_a)
        circuit_b = connected_junctions.get(junction_b)

        if circuit_a is None and circuit_b is None:
            new_circuit = [junction_a, junction_b]
            connected_junctions[junction_a] = new_circuit
            connected_junctions[junction_b] = new_circuit
        elif circuit_a is None:
            circuit_b.append(junction_a)
            connected_junctions[junction_a] = circuit_b
        elif circuit_b is None:
            circuit_a.append(junction_b)
            connected_junctions[junction_b] = circuit_a
        elif circuit_a != circuit_b:
            circuit_a.extend(circuit_b)
            for junction in circuit_b:
                connected_junctions[junction] = circuit_a
        if len(connected_junctions[junction_a]) == len(points):
            break
    print(f'last connection = {junction_a, junction_b}')
    print(junction_a[0] * junction_b[0])