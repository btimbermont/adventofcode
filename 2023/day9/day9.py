def get_diffs(values: [int]) -> [int]:
    return [j - i for i, j in zip(values[:-1], values[1:])]


def get_diff_overview(values: [int]):
    diffs = [values]
    while not all(value == 0 for value in diffs[-1]):
        next_diffs = get_diffs(diffs[-1])
        if len(next_diffs) == 0:
            next_diffs = [0]
        diffs.append(next_diffs)
    return diffs


def get_next_val(values: [int]) -> int:
    diffs = get_diff_overview(values)
    return sum([diff[-1] for diff in diffs if diff])


def get_previous_value(values: [int]) -> int:
    diffs = get_diff_overview(values)
    result = 0
    for i in reversed(range(len(diffs) - 1)):
        result = diffs[i][0] - result
    return result


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        lines = [[int(i) for i in line.strip().split(' ')] for line in file]

    print('part 1')
    print(sum([get_next_val(values) for values in lines]))

    print('part 2')
    print(sum([get_previous_value(values) for values in lines]))
