from typing import List


def get_max_joltage(bank: List[int]) -> int:
    # get first digit:
    first_digit = max(bank[:-1])
    # first occurrence
    first_occurrence = bank.index(first_digit)
    # second digit
    second_digit = max(bank[first_occurrence+1:])
    return 10 * first_digit + second_digit


if __name__ == '__main__':
    banks = []
    with open('input.txt', 'r') as file:
        for line in file:
            banks.append([int(c) for c in line.strip()])

    print("part 1")
    print(sum([get_max_joltage(b) for b in banks]))
