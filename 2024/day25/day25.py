from typing import Tuple, List

KeyOrLock = Tuple[int, ...]


def parse_block(input: str) -> Tuple[str, KeyOrLock]:
    type = 'key' if input[0] == '.' else 'lock'
    input = input.splitlines()
    input = [list(line) for line in input]
    numbers_of_hashes: KeyOrLock = [-1 for _ in range(len(input[0]))]  # -1 because the base row doesn't count
    for line in input:
        for pin_number, pin_content in enumerate(line):
            if pin_content == '#':
                numbers_of_hashes[pin_number] += 1
    return type, tuple(numbers_of_hashes)


def sum(lock: KeyOrLock, key: KeyOrLock) -> KeyOrLock:
    return tuple((k + l for k, l in zip(key, lock)))


def parse_file(path: str) -> Tuple[List[KeyOrLock], List[KeyOrLock]]:
    with open(path, 'r') as file:
        blocks = file.read().split('\n\n')
    keys = []
    locks = []
    for block in blocks:
        type, key_or_lock = parse_block(block)
        if type == 'key':
            keys.append(key_or_lock)
        else:
            locks.append(key_or_lock)
    return keys, locks


def overlap(lock: KeyOrLock, key: KeyOrLock, print_all: bool = False) -> List[int]:
    overlaps = []
    for i, lock_and_key in enumerate(zip(lock, key)):
        l, k = lock_and_key
        if l + k > 5:
            overlaps.append(i)
    if print_all:
        print(f'Lock {lock} and key {key}: {f"overlap in columns {overlaps}" if overlaps else "all columns fit!"}')
    return overlaps


if __name__ == '__main__':
    keys, locks = parse_file('input.txt')
    print('part 1')
    fits = []
    for lock in locks:
        for key in keys:
            if not overlap(lock, key, print_all=True):
                fits.append((lock, key))
    print(len(fits))

