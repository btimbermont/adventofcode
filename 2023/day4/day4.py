from dataclasses import field, dataclass


@dataclass
class Card:
    id: int
    winning_numbers: [int]
    numbers: [int]
    value: int = field(init=False)
    winning_numbers_present: [int] = field(init=False)

    def __post_init__(self):
        self.winning_numbers_present = [n for n in self.numbers if n in self.winning_numbers]
        if len(self.winning_numbers_present) == 0:
            self.value = 0
        else:
            self.value = pow(2, len(self.winning_numbers_present) - 1)


def parse_card(line: str) -> Card:
    id, numbers = line.split(':')
    id = int(id.split(' ')[-1])
    winning, nums = numbers.split('|')
    winning = [int(n) for n in winning.split(' ') if n != '']
    nums = [int(n) for n in nums.split(' ') if n != '']
    return Card(id=id, winning_numbers=winning, numbers=nums)


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        cards = [parse_card(line.strip()) for line in file.readlines()]

    print('part 1')
    print(sum([card.value for card in cards]))

    print('part 2')
    amounts = [1 for card in cards]
    for i, card in enumerate(cards):
        amount = amounts[i]
        wins = len(card.winning_numbers_present)
        for j in range(i + 1, i + 1 + wins):
            amounts[j] += amount
    print(sum(amounts))
