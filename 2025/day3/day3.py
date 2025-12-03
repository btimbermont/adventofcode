from typing import List

def get_max_joltage(bank: List[int], batteries: int) -> int:
    values = []
    min_idx = 0
    for i in range(batteries):
        slack = batteries - len(values) - 1  # number of digits at end of bank to ignore for this round
        next_digit = max(bank[min_idx:len(bank)-slack])
        values.append(next_digit)
        first_occurrence = min_idx + bank[min_idx:].index(next_digit)
        min_idx = first_occurrence+1
    return int(''.join(map(str, values)))


if __name__ == '__main__':
    banks = []
    with open('input.txt', 'r') as file:
        for line in file:
            banks.append([int(c) for c in line.strip()])

    print("part 1")
    print(sum([get_max_joltage(b, 2) for b in banks]))
    print("part 1")
    print(sum([get_max_joltage(b,12) for b in banks]))
