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
    fresh_ranges.sort(key=lambda x: x[0])

    print('part 1')
    fresh_ids = []
    for id in ids_to_lookup:
        matching_range = next((range for range in fresh_ranges if in_range(id, range)), None)
        if matching_range:
            fresh_ids.append(id)
    print(len(fresh_ids))
