class Assignment:
    def __init__(self, string_repr: str):
        self.start, self.end = [int(s) for s in string_repr.split('-')]

    def fully_contains(self, other: 'Assignment') -> bool:
        return self.start <= other.start and other.end <= self.end

    def partial_overlap(self, other: 'Assignment') -> bool:
        return other.start <= self.end and other.end >= self.start


def parse_pair(line: str) -> (Assignment, Assignment):
    s1, s2 = line.split(',')
    return Assignment(s1), Assignment(s2)


def full_overlap(elf1: Assignment, elf2: Assignment) -> bool:
    return elf1.fully_contains(elf2) or elf2.fully_contains(elf1)


if __name__ == '__main__':
    print('PART 1')
    with open('input.txt', 'r') as file:
        full_overlaps = 0
        for line in file.read().splitlines():
            elf1, elf2 = parse_pair(line)
            if full_overlap(elf1, elf2):
                full_overlaps += 1
    print(f'full overlaps: {full_overlaps}')
    print('PART 2')
    with open('input.txt', 'r') as file:
        partial_overlaps = 0
        for line in file.read().splitlines():
            elf1, elf2 = parse_pair(line)
            if elf1.partial_overlap(elf2):
                partial_overlaps += 1
    print(f'full overlaps: {partial_overlaps}')
