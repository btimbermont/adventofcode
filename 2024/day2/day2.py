from typing import List


def is_safe(values: List[int]) -> bool:
    diffs = [b - a for a, b in zip(values[:-1], values[1:])]
    return all([a in [1, 2, 3] for a in diffs]) or all([a in [-1, -2, -3] for a in diffs])


def is_safe2(values: List[int], allowed_errors: int = 1) -> bool:
    if is_safe(values):
        return True
    if allowed_errors <= 0:
        return False
    #ugly: brute force,
    for i in range(len(values)):
        popped_one = values.copy()
        popped_one.pop(i)
        if is_safe2(popped_one, allowed_errors - 1):
            return True
    return False


if __name__ == '__main__':
    print("Part 1")
    result = 0
    with open("input.txt") as file:
        for line in file:
            values = [int(a) for a in line.split()]
            # print(values)
            if is_safe(values):
                result += 1
    print(result)
    print("Part 2")
    result = 0
    with open("input.txt") as file:
        for line in file:
            values = [int(a) for a in line.split()]
            # print(values)
            if is_safe2(values):
                result += 1
    print(result)
