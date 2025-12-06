import math
from typing import List


def process_problem(problem: List[int]) -> int:
    values, operator = [int(v) for v in problem[:-1]] , problem[-1]
    if operator == '+':
        return sum(values)
    elif operator == '*':
        return math.prod(values)
    else:
        raise ValueError(f'Unknown operator: {operator}')


if __name__ == '__main__':
    lists = []
    with open('input.txt', 'r') as file:
        for line in file:
            values = line.split()
            while len(lists) < len(values):
                lists.append([])
            for i, value in enumerate(values):
                lists[i].append(value)

    print('part 1')
    total = 0
    for problem in lists:
        value = process_problem(problem)
        print(f'{problem} = {value}')
        total += value
    print(f'Solution: {total}')
