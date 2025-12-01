def split_rucksack(contents: str) -> (str, str):
    half = len(contents) // 2
    return contents[:half], contents[half:]


def get_characters_in_both_strings(s1: str, s2: str) -> str:
    duplicates = ''
    for char in s1:
        if char in s2 and char not in duplicates:
            duplicates += char
    return duplicates


def calc_priority(item: str) -> int:
    if ord(item) in range(ord('a'), ord('z') + 1):
        return ord(item) - 96
    if ord(item) in range(ord('A'), ord('Z') + 1):
        return ord(item) - 38
    raise Exception(f'invalid item: {item}')


def rucksack_value(contents: str) -> int:
    compartment1, compartment2 = split_rucksack(contents)
    duplicate_items = get_characters_in_both_strings(compartment1, compartment2)
    return calc_priority(duplicate_items)


def find_group(elf1: str, elf2: str, elf3: str) -> str:
    group_candidates = get_characters_in_both_strings(elf1, elf2)
    return get_characters_in_both_strings(group_candidates, elf3)


if __name__ == '__main__':
    print('PART 1')
    with open('input.txt', 'r') as file:
        priorities = []
        for line in file.read().splitlines():
            priorities.append(rucksack_value(line))
        print(f'sum of priorities: {sum(priorities)}')
    print('PART 2')
    with open('input.txt', 'r') as file:
        priorities = []
        while True:
            elf1, elf2, elf3 = file.readline().replace('\n', ''), file.readline().replace('\n',
                                                                                          ''), file.readline().replace(
                '\n', '')
            if not elf3:
                break
            group = find_group(elf1, elf2, elf3)
            priorities.append(calc_priority(group))
        print(sum(priorities))
