from typing import List, Tuple

def apply_beams(input: List[str]) -> Tuple[List[str], int, List[int]]:
    result = []
    split_count = 0
    timeline_counts = None
    for line in input:
        if timeline_counts is None:
            timeline_counts = [0] * len(line)
            timeline_counts[line.index('S')] = 1
            result.append(line)
            continue
        for i in [i for i, char in enumerate(line) if char == '^']:
            if timeline_counts[i] > 0:
                split_count += 1
                timeline_counts[i - 1] += timeline_counts[i]
                timeline_counts[i + 1] += timeline_counts[i]
                timeline_counts[i] = 0
        new_line = list(line)
        for i, count in enumerate(timeline_counts):
            if count > 0:
                new_line[i] = '|'
        result.append(''.join(new_line))
    return result, split_count, timeline_counts

if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        input = [l.strip() for l in file.readlines()]

    result, split_count, timeline_counts = apply_beams(input)
    print('\n'.join(result))

    print('part 1')
    print(f'splits: {split_count}')
    print('part 2')
    print(f'timeline count: {sum(timeline_counts)}\ttimeline counts: {timeline_counts}')
