import time
from typing import List


def step1(secret_number: int) -> int:
    new_val = secret_number * 64
    new_val = mix(secret_number, new_val)
    return prune(new_val)


def step2(secret_number: int) -> int:
    new_val = secret_number // 32
    new_val = mix(secret_number, new_val)
    return prune(new_val)


def step3(secret_number: int) -> int:
    new_val = secret_number * 2048
    new_val = mix(secret_number, new_val)
    return prune(new_val)


def next_secret(secret_number: int) -> int:
    return step3(step2(step1(secret_number)))


def mix(secret_number: int, value: int) -> int:
    return secret_number ^ value


def prune(secret_number) -> int:
    return secret_number % 16777216


class Buyer:
    def __init__(self, initial_secret):
        self.initial_secret = initial_secret
        self.current_secret = initial_secret
        self.secret_index = 0

    def next_secret(self, count: int = 1) -> int:
        for i in range(count):
            self.current_secret = next_secret(self.current_secret)
        self.secret_index += count
        return self.current_secret

    @property
    def price(self):
        return self.current_secret % 10


class Buyer2:
    def __init__(self, initial_secret):
        self.secrets = []
        val = initial_secret
        for i in range(2000):
            self.secrets.append(val)
            val = next_secret(val)
        self.prices = [s % 10 for s in self.secrets]
        self.price_diffs = [a - b for a, b in zip(self.prices[1:], self.prices[:-1])]
        self.price_diffs.insert(0, 'xx')
        self.price_diffs2 = "".join([str(d).zfill(2) for d in self.price_diffs])

    def price_for_sequence(self, sequence: List[int]) -> int:
        for i in range(len(self.price_diffs) - len(sequence)):
            if sequence == self.price_diffs[i:i + len(sequence)]:
                return self.prices[i + len(sequence) - 1]
        return 0

    def price_for_sequence2(self, sequence: List[int]) -> int:
        sequence = "".join([str(n).zfill(2) for n in sequence])
        spot = self.price_diffs2.find(sequence)
        if spot < 0:
            return 0
        else:
            return self.prices[(spot + len(sequence))//2 - 1]

    def sequences_for_price(self, price: int) -> List[List[int]]:
        sequences = []
        for i in range(4, len(self.prices)):
            if self.prices[i] == price:
                sequence = self.price_diffs[i - 3:i + 1]
                sequences.append(sequence)
        return list(sequences)


if __name__ == '__main__':
    with open('test_input.txt', 'r') as file:
        buyers = [Buyer(int(line)) for line in file.read().splitlines()]
    print('Part 1')
    for buyer in buyers:
        buyer.next_secret(2000)
        # print(f'{buyer.initial_secret}: {buyer.current_secret}')
    print(f'Solution: {sum([b.current_secret for b in buyers])}')

    print('Part 2')
    print('loading data...')
    with open('input.txt', 'r') as file:
        buyers = [Buyer2(int(line)) for line in file.read().splitlines()]
    print('data loaded!')
    # buyers = [Buyer2(v) for v in [1,2,3,2024]]
    best_price = 0
    best_sequence = None
    i = 0
    for a in range(-9, 10):
        for b in range(-9, 10):
            for c in range(-9, 10):
                percentage = 100*i/(19*19*19)
                i+=1
                print(f'\r{percentage}%', end='')
                for d in range(-9, 10):
                    sequence = [a, b, c, d]
                    current_price = sum([b.price_for_sequence2(sequence) for b in buyers])
                    if current_price > best_price:
                        best_price = current_price
                        best_sequence = sequence
    print(f'\rSeqeunce {best_sequence} gives price {best_price}')
