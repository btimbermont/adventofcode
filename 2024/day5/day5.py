from pathlib import Path
from typing import List, Tuple


class Rule:
    def __init__(self, line: str):
        self.l, self.r = (int(a) for a in line.split('|'))

    def applies(self, update: List[int]):
        return self.l in update and self.r in update

    def validate(self, update: List[int]) -> bool:
        if not self.applies(update):
            return True
        return update.index(self.l) < update.index(self.r)

    def fix_update(self, update: List[int]):
        if self.validate(update):
            return
        l_index = update.index(self.l)
        r_index = update.index(self.r)
        update[l_index] = self.r
        update[r_index] = self.l

    def __str__(self):
        return f'Rule({self.l}|{self.r})'

    def __repr__(self):
        return f'Rule({self.l}|{self.r})'


def read_file(path: Path) -> Tuple[List[Rule], List[List[int]]]:
    rules = []
    pages = []
    with open(path, 'r') as file:
        is_rule = True
        for line in file.read().splitlines():
            if not line:
                is_rule = False
                continue
            if is_rule:
                rules.append(Rule(line))
            else:
                pages.append([int(i) for i in line.split(',')])
    return rules, pages


def is_valid_update(update: List[int], rules: List[Rule]) -> bool:
    for rule in rules:
        if not rule.validate(update):
            return False
    return True


def fix_update(update: List[int], rules: List[Rule]) -> List[int]:
    result = update.copy()
    while not is_valid_update(result, rules):  # Could be more efficient, but good enough for now
        for rule in rules:
            rule.fix_update(result)
    return result


if __name__ == '__main__':
    rules, updates = read_file(Path("input.txt"))
    print('part 1')
    valid_updates = [update for update in updates if is_valid_update(update, rules)]
    middle_pages = [update[int(len(update) / 2)] for update in valid_updates]
    print(sum(middle_pages))
    print('part 2')
    fixed_update = [fix_update(update, [rule for rule in rules if rule.applies(update)]) for update in updates if not is_valid_update(update, rules)]
    middle_pages = [update[int(len(update) / 2)] for update in fixed_update]
    print(sum(middle_pages))
