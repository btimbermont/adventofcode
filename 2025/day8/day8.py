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
    shortest_distances = list(sorted(distance_map.keys()))
    connected_junctions = dict()
    for d in shortest_distances:
        junction_a, junction_b = distance_map[d]
        circuit_a, circuit_b = None, None

        junction_a_circuit = connected_junctions.get(junction_a)
        junction_b_circuit = connected_junctions.get(junction_b)

        if junction_a_circuit is None and junction_b_circuit is None:
            new_circuit = [junction_a, junction_b]
            connected_junctions[junction_a] = new_circuit
            connected_junctions[junction_b] = new_circuit
        elif junction_a_circuit is None:
            junction_b_circuit.append(junction_a)
            connected_junctions[junction_a] = junction_b_circuit
        elif junction_b_circuit is None:
            junction_a_circuit.append(junction_b)
            connected_junctions[junction_b] = junction_a_circuit
        elif junction_a_circuit == junction_b_circuit:
            continue
        else:
            # merge two circuits
            junction_a_circuit.append(junction_b_circuit)
            for j in junction_b_circuit:
                connected_junctions[j] = junction_a_circuit
        connections -=1
        if connections == 0:
            break
    for k,v in connected_junctions.items():
        print(f'{k}:\t{v}')  # still wrong :(