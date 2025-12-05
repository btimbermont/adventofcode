from typing import Tuple


def in_range(i: int, range: Tuple[int, int]) -> bool:
    return i >= range[0] and i <= range[1]


if __name__ == '__main__':
    fresh_ranges = []
    ids_to_lookup = []
    with open('input.txt', 'r') as file:
        ranges = True
        for line in file:
            line = line.strip()
            if ranges:
                if line:
                    split = line.split('-')
                    fresh_ranges.append(tuple([int(n) for n in split]))
                else:
                    ranges = False
            else:
                ids_to_lookup.append(int(line))

    print('part 1')
    fresh_ids = []
    for id in ids_to_lookup:
        matching_range = next((range for range in fresh_ranges if in_range(id, range)), None)
        if matching_range:
            fresh_ids.append(id)
    print(len(fresh_ids))

    print('part 2')
    fresh_ranges.sort(key=lambda x: x[0])
    max_id = -1
    fresh_ids = 0
    for id_range in fresh_ranges:
        if max_id >= id_range[0]:
            if max_id >= id_range[1]:
                continue
            id_range = (max_id + 1, id_range[1])
        fresh_ids += id_range[1] - id_range[0] + 1
        max_id = id_range[1]
    print(fresh_ids)
