import math
from typing import List


def process_problem(problem: List[int]) -> int:
    values, operator = [int(v) for v in problem[:-1]], problem[-1]
    if operator == '+':
        return sum(values)
    elif operator == '*':
        return math.prod(values)
    else:
        raise ValueError(f'Unknown operator: {operator}')


if __name__ == '__main__':
    print('part 1')
    lists = []
    with open('input.txt', 'r') as file:
        for line in file:
            values = line.split()
            while len(lists) < len(values):
                lists.append([])
            for i, value in enumerate(values):
                lists[i].append(value)
    total = 0
    for problem in lists:
        value = process_problem(problem)
        total += value
    print(f'Solution: {total}')

    print('part 1')
    lines = []
    with open('input.txt', 'r') as file:
        for line in file:
            lines.append(line)
    max_length = max([len(l) for l in lines])
    values = []
    solutions = []
    for i in range(max_length - 1, -1, -1):
        values.append('')
        for line in lines:
            if i >= len(line):
                continue
            if line[i] in '+*':
                if line[i] == '+':
                    solutions.append(sum([int(v) for v in values if len(v)]))
                else:
                    solutions.append(math.prod([int(v) for v in values if len(v)]))
                values = []
            elif line[i] in '0123456789':
                values[-1] += line[i]
    print(f'Solution: {sum(solutions)}')