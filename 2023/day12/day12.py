from itertools import zip_longest
from typing import List


def generate_part_lists(total_amount, parts, current_list=[]):
    result = []
    if parts == 0:
        # If no more parts are left, check if the total amount is zero
        if total_amount == 0 and all(part != 0 for part in current_list):
            result.append(current_list)
        return result

    # Iterate through possible values for the current part
    for i in range(1, total_amount + 1):
        # Recursively call the function with reduced total_amount and parts
        result += generate_part_lists(total_amount - i, parts - 1, current_list + [i])

    return result


def generate_possible_functional_springs(total_length: int, broken_springs: [int]) -> List[List[int]]:
    result = []
    number_of_functional_springs = total_length - sum(broken_springs)
    # 1: broken parts at both ends
    intervals = len(broken_springs) - 1
    functional_springs = generate_part_lists(number_of_functional_springs, intervals)
    result.extend([[0] + s + [0] for s in functional_springs])
    # 2: broken part at start or end (not both!)
    intervals += 1
    functional_springs = generate_part_lists(number_of_functional_springs, intervals)
    result.extend([[0] + s for s in functional_springs])
    result.extend([s + [0] for s in functional_springs])
    # 3: functional springs at both ends
    intervals += 1
    functional_springs = generate_part_lists(number_of_functional_springs, intervals)
    result.extend(functional_springs)

    return result


def generate_sequence(functional_springs: [int], broken_springs: [int]):
    if len(functional_springs) - 1 != len(broken_springs):
        raise Exception("expected functional springs to be 1 element longer than broken springs!")
    sequence = ''
    for f, b in zip_longest(functional_springs, broken_springs):
        sequence += '.' * f
        if b:
            sequence += '#' * b
    return sequence


def pattern_matches_sequence(pattern: str, sequence: str) -> bool:
    if len(pattern) != len(sequence):
        return False
    for i in range(len(pattern)):
        if pattern[i] != '?' and pattern[i] != sequence[i]:
            return False
    return True


def pattern_matches_arrangement(pattern: str, functional_springs: [int], broken_springs: [int]) -> bool:
    actual_sequence = generate_sequence(functional_springs, broken_springs)
    if len(pattern) != len(actual_sequence):
        print(f'ERROR: length of actual sequence doesn\'t match pattern length.'
              f' pattern: {pattern}, seq: {actual_sequence}')
    return pattern_matches_sequence(pattern, actual_sequence)


if __name__ == '__main__':
    print('part 1')
    counts = 0
    with open('input.txt', 'r') as file:
        for line in file:
            pattern, broken_springs = line.strip().split(' ')
            broken_springs = [int(p) for p in broken_springs.split(',')]
            functional_springs_options = generate_possible_functional_springs(len(pattern), broken_springs)
            functional_springs_options = [option for option in functional_springs_options if
                                          pattern_matches_arrangement(pattern, option, broken_springs)]
            # print(
            #     f'pattern: "{pattern}", parts: {broken_springs}, possible functional springs: {len(functional_springs_options)}')
            if len(functional_springs_options) == 0:
                print(f'ERROR: no possible solution for line {line}')
            counts += len(functional_springs_options)
    print(counts)
