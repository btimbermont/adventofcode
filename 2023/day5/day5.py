import re
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class IntervalRule:
    start: int
    range: int
    shift: int

    def __init__(self, line: str):
        values = [int(n) for n in line.strip().split(' ')]
        self.start = values[1]
        self.range = values[2]
        self.shift = values[0] - values[1]

    def contains(self, value: int) -> bool:
        return self.start <= value < self.start + self.range


@dataclass
class Transformation:
    source: str
    destination: str
    rules: [IntervalRule] = field(init=False)

    def __init__(self, name: str):
        map_name_parts = name.split(' ')[0].split('-')
        self.source = map_name_parts[0]
        self.destination = map_name_parts[-1]
        self.rules = []

    def _apply(self, value: int) -> int:
        for rule in self.rules:
            if rule.contains(value):
                return value + rule.shift
        return value

    def apply_to_seed(self, seed: Dict[str, int]):
        seed[self.destination] = self._apply(seed[self.source])


def transformation_can_be_applied(seed: Dict[str, int], transformation: Transformation) -> bool:
    return transformation.source in seed.keys() and not transformation.destination in seed.keys()


if __name__ == '__main__':
    seeds: List[Dict[str, int]] = []
    transformations: Dict[str, Transformation] = {}
    instruction_line_regex = re.compile("\d+\s+\d+\s+\d")

    with (open('input.txt') as file):
        for line in file:
            if line.startswith('seeds:'):
                seeds = [dict(seed=int(n)) for n in line.split(':')[-1].strip().split(' ')]
            elif 'map:' in line:
                # start parsing new transformation:
                current_transformation = Transformation(line)
                transformations[current_transformation.source] = current_transformation
            elif instruction_line_regex.match(line):
                current_transformation.rules.append(IntervalRule(line))
            elif not line.strip():
                current_transformation = None
            else:
                raise Exception(f'unexpected line: "{line}"')

    print('part 1')
    for seed in seeds:
        while True:
            did_something = False
            for transformation in transformations.values():
                if transformation_can_be_applied(seed, transformation):
                    transformation.apply_to_seed(seed)
                    did_something = True
            if not did_something:
                break
        print(f'Done with seed {seed["seed"]}: {seed}')
    print(f'Minimum location: {min([s["location"] for s in seeds])}')
