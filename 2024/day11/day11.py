from dataclasses import dataclass
from functools import cache
from typing import Callable, List


@dataclass
class Rule:
    applies: Callable[[int], bool]
    apply: Callable[[int], List[int]]


def split_stone(stone: int) -> List[int]:
    stone = str(stone)
    return [int(stone[:len(stone) // 2]), int(stone[len(stone) // 2:])]


RULES = [Rule(lambda s: s == 0, lambda s: [1]),
         Rule(lambda s: len(str(s)) % 2 == 0, lambda s: split_stone(s)),
         Rule(lambda s: True, lambda s: [s * 2024])]


def apply_rules(stone: int) -> List[int]:
    for rule in RULES:
        if rule.applies(stone):
            return rule.apply(stone)
    raise ValueError(f"None of the rules apply on {stone}")


def blink(stones: List[int]) -> List[int]:
    return [x for stone in stones for x in apply_rules(stone)]


@cache
def length_after_blinks(stone: int, blinks: int) -> int:
    if blinks == 0:
        return 1
    after_blink = apply_rules(stone)
    if len(after_blink) == 1:
        return length_after_blinks(after_blink[0], blinks - 1)
    else:
        return sum([length_after_blinks(s, blinks -1) for s in after_blink])


if __name__ == '__main__':
    print('part 1')
    input = [0, 44, 175060, 3442, 593, 54398, 9, 8101095]
    for i in range(25):
        input = blink(input)
    print(len(input))

    print('part 2')
    input = [0, 44, 175060, 3442, 593, 54398, 9, 8101095]
    result = sum([length_after_blinks(s, 75) for s in input])
    print(result)

