from copy import deepcopy
from math import prod
from typing import Callable


class Monkey:
    def __init__(self, items: [int],
                 operation: Callable[[int], int],
                 test: Callable[[int], bool],
                 true_throw: int,
                 false_throw: int):
        self.items = items
        self.operation = operation
        self.test = test
        self.true_throw = true_throw
        self.false_throw = false_throw
        self.inspect_counter = 0


def parse_monkey(text: str) -> Monkey:
    lines = text.splitlines()
    items = [int(i) for i in lines[1].split(': ')[1].split(',')]

    operation = lines[2].split('= ')[-1].split(' ')
    left: Callable[[int], int] = lambda a: (a if operation[0] == 'old' else int(operation[0]))
    right: Callable[[int], int] = lambda a: (a if operation[2] == 'old' else int(operation[2]))
    monkey_operation: Callable[[int], int]
    if operation[1] == '+':
        monkey_operation = lambda item: left(item) + right(item)
    elif operation[1] == '*':
        monkey_operation = lambda item: left(item) * right(item)
    else:
        raise Exception(f'Unknown operator: {operation[1]}')

    divisible_by = int(lines[3].split(' ')[-1])
    test = lambda item: item % divisible_by == 0
    true_throw = int(lines[4].split(' ')[-1])
    false_throw = int(lines[5].split(' ')[-1])
    return Monkey(items, monkey_operation, test, true_throw, false_throw)


def parse_input(path: str) -> [Monkey]:
    monkeys = []
    with open(path) as file:
        current_monkey_text = ''
        for line in file.read().splitlines():
            if line == '':
                monkeys.append(parse_monkey(current_monkey_text))
                current_monkey_text = ''
            else:
                current_monkey_text += line
                current_monkey_text += '\n'
        if current_monkey_text != '':
            monkeys.append(parse_monkey(current_monkey_text))
    return monkeys


def get_modulo(path: str) -> int:
    with open(path) as file:
        factors = [int(line.split(' ')[-1]) for line in file.read().splitlines() if 'Test:' in line]
    return prod(factors)


def do_round(monkeys: [Monkey], worry_management: Callable[[int], int]):
    i = 0
    for monkey in monkeys:
        # print(f'Monkey {i}:')
        i += 1
        # inspect and throw each item
        for item_worry_level in monkey.items:
            # print(f'\tMonkey inspects an item with a worry level of {item_worry_level}')
            new_worry_level = monkey.operation(item_worry_level)
            monkey.inspect_counter += 1
            # print(f'\t\t Worry level is increased to {new_worry_level}.')
            new_worry_level = worry_management(new_worry_level)
            # print(f'\t\tMonkey gets bored with item. Worry level is divided by 3 to {new_worry_level}.')
            if monkey.test(new_worry_level):
                # print(f'\t\tItem with worry level {new_worry_level} is thrown to monkey {monkey.true_throw}.')
                monkeys[monkey.true_throw].items.append(new_worry_level)
            else:
                # print(f'\t\tItem with worry level {new_worry_level} is thrown to monkey {monkey.false_throw}.')
                monkeys[monkey.false_throw].items.append(new_worry_level)
        monkey.items = []


def print_monkeys(monkeys: [Monkey]):
    for i in range(len(monkeys)):
        print(f'Monkey {i}: {monkeys[i].items}\tinspect:{monkeys[i].inspect_counter}')


def monkey_business(monkeys: [Monkey]) -> int:
    copy = deepcopy(monkeys)
    copy.sort(key=lambda monkey: monkey.inspect_counter)
    return copy[-1].inspect_counter * copy[-2].inspect_counter


if __name__ == '__main__':
    print('PART 1')
    monkeys = parse_input('input.txt')
    for i in range(20):
        do_round(monkeys, lambda a: a // 3)
    print_monkeys(monkeys)
    monkeys.sort(key=lambda monkey: monkey.inspect_counter)
    print(f'Monkey business: {monkey_business(monkeys)}')

    print('PART 2')
    path = 'input.txt'
    monkeys = parse_input(path)
    modulo = get_modulo(path)
    for i in range(10000):
        do_round(monkeys, lambda a: a % modulo)
    print_monkeys(monkeys)
    monkeys.sort(key=lambda monkey: monkey.inspect_counter)
    print(f'Monkey business: {monkey_business(monkeys)}')
