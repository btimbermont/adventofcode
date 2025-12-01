from collections import Counter
from pathlib import Path
from typing import List, Tuple


def parse_file(file: Path) -> Tuple[List[int], List[int]]:
    list1 = []
    list2 = []
    with open(file, 'r') as file:
        for line in file:
            i1, i2 = line.split()
            list1.append(int(i1))
            list2.append(int(i2))
    return list1, list2


def calc_distances(l1: List[int], l2: List[int]) -> List[int]:
    l1.sort()
    l2.sort()
    return [abs(a - b) for a, b in zip(l1, l2)]


def similarity_score(l1: List[int], l2: List[int]) -> int:
    d2 = Counter(l2)
    score = 0
    for i in l1:
        if i in d2.keys():
            # print(f'{i}: {i}x{d2[i]}')
            score = score + i*d2[i]
    return score


if __name__ == '__main__':
    l1, l2 = parse_file(Path('input.txt'))
    print("Part 1")
    print(sum(calc_distances(l1, l2)))
    print("Part 2")
    print(similarity_score(l1, l2))
