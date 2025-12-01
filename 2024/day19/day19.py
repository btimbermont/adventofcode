from functools import cache
from typing import List, Optional

Towel = str


class Towels:
    def __init__(self, available_towels: List[Towel]):
        self.towels = available_towels
        self.towels.sort(key=len)
        self.towels.reverse()

    def make_pattern(self, pattern: str) -> Optional[List[Towel]]:
        if not pattern:
            return []
        candidates = [t for t in self.towels if pattern.startswith(t)]
        for c in candidates:
            sub_pattern = pattern[len(c):]
            sub_solution = self.make_pattern(sub_pattern)
            if sub_solution is not None:
                return [c] + sub_solution
        return None

    @cache
    def count_possible_arrangements(self, pattern: str) -> int:
        if not pattern:
            return 1
        candidates = [t for t in self.towels if pattern.startswith(t)]
        sub_patterns = [pattern[len(c):] for c in candidates]
        return sum([self.count_possible_arrangements(p) for p in sub_patterns])

    def __str__(self):
        return f'Towels({self.towels})'


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        possible_towels, patterns = file.read().split('\n\n')
        possible_towels = [t.strip() for t in possible_towels.split(',')]
        towels = Towels(possible_towels)
        patterns = patterns.splitlines()
    print("Part 1")
    possible = 0
    for pattern in patterns:
        arrangement = towels.make_pattern(pattern)
        if arrangement is None:
            print(f'Pattern {pattern} is IMPOSSIBLE')
        else:
            print(f'Pattern {pattern} is possible: {arrangement}')
            possible += 1
    print(f'Part 1 solution: {possible}')

    print('Part 2')
    amounts = []
    for pattern in patterns:
        solutions = towels.count_possible_arrangements(pattern)
        print(f'pattern {pattern} has {solutions} solutions')
        amounts.append(solutions)
    print(f'Part 2 solution: {sum(amounts)}')
