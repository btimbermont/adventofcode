from typing import List, Tuple


def apply_beams(input: List[str]) -> Tuple[List[str], int]:
    result = []
    current_beams = set()
    split_count = 0
    for line in input:
        if not current_beams:
            current_beams.add(line.index('S'))
            result.append(line)
            continue
        curr = list(current_beams)
        for beam in curr:
            if line[beam] == '^':
                split_count += 1
                current_beams.remove(beam)
                current_beams.add(beam - 1)
                current_beams.add(beam + 1)
        new_line = list(line)
        for beam in current_beams:
            new_line[beam] = '|'
        result.append(''.join(new_line))
    return result, split_count


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        input = [l.strip() for l in file.readlines()]
    print('part 1')
    result, split_count = apply_beams(input)
    print('\n'.join(result))
    print(split_count)
