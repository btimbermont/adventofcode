from typing import Optional


def is_possible_mirror_location(line: str, mirror_location: int) -> bool:
    if mirror_location < 1 or mirror_location > len(line) - 1:
        return False
    a = line[:mirror_location][::-1]
    b = line[mirror_location:]
    if len(a) > len(b):
        return a.startswith(b)
    else:
        return b.startswith(a)


def find_vertical_mirror(pattern: [str]) -> Optional[int]:
    possible_mirror_locations = [n for n in range(1, len(pattern[0]))]
    for row in pattern:
        possible_mirror_locations = [l for l in possible_mirror_locations if is_possible_mirror_location(row, l)]
        if not possible_mirror_locations:
            break
    if len(possible_mirror_locations) > 1:
        # mirror could be in multiple places: invalid, no mirror!
        return None
    elif possible_mirror_locations:
        return possible_mirror_locations[0]
    else:
        return None


def find_horizontal_mirror(pattern: [str]) -> Optional[int]:
    inverted_pattern = [''.join(chars) for chars in zip(*pattern)]
    return find_vertical_mirror(inverted_pattern)


def find_mirror(pattern: [str]) -> (str, int):
    h = find_horizontal_mirror(pattern)
    if h is not None:
        return 'horizontal', h
    v = find_vertical_mirror(pattern)
    if v is not None:
        return 'vertical', v
    return None, None


def remove_smudge(pattern: [str], x: int, y: int) -> [str]:
    new_pattern = [line for line in pattern]
    new_pattern[y] = pattern[y][:x] + ('#' if pattern[y][x] == '.' else '.') + pattern[y][x + 1:]
    return new_pattern


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        patterns = file.read().split('\n\n')

    print('part 1')
    score = 0
    for pattern in patterns:
        pattern = pattern.split()
        orientation, mirror_position = find_mirror(pattern)
        if orientation == 'horizontal':
            score += 100 * mirror_position
        elif orientation == 'vertical':
            score += mirror_position
    print(score)

    print('part 2')
    score = 0
    for pattern in patterns:
        pattern = pattern.split()
        orientation, mirror_position = find_mirror(pattern)

        for x, y in [(x, y) for x in range(len(pattern[0])) for y in range(len(pattern))]:
            new_pattern = remove_smudge(pattern, x, y)
            new_orientation, new_mirror = find_mirror(new_pattern)
            if new_orientation is not None and (new_orientation, new_mirror) != (orientation, mirror_position):
                if new_orientation == 'horizontal':
                    score += 100 * new_mirror
                elif new_orientation == 'vertical':
                    score += new_mirror
                break
    print(score)
