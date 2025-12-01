import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class PartNumber:
    value: int
    len: int = field(init=False)
    x: int
    y: int
    is_part: bool

    def __post_init__(self):
        self.len = len(str(self.value))

    def neighbors(self) -> List[Tuple[int, int]]:
        result = []
        result += ([(i, self.y - 1) for i in range(self.x - 1, self.x + self.len + 1)])
        result += [(self.x - 1, self.y)]
        result += [(self.x + self.len, self.y)]
        result += ([(i, self.y + 1) for i in range(self.x - 1, self.x + self.len + 1)])
        return [r for r in result if 0 <= r[0] < MAX_X and 0 <= r[1] < MAX_Y]


def is_part(schematic: [str], coordinate: (int, int)) -> bool:
    character = schematic[coordinate[1]][coordinate[0]]
    return not (character.isdigit() or character == '.')


def parse_schematic(schematic: [str]) -> Dict[str, List[PartNumber]]:
    numbers = []
    # get all numbers
    for i in range(len(schematic)):
        for match in re.finditer(r'\d+', schematic[i]):
            value = int(match.group())
            numbers.append(PartNumber(value=value, x=match.start(), y=i, is_part=False))
    # check all numbers and see if they're parts
    for number in numbers:
        for coordinate in number.neighbors():
            if is_part(schematic, coordinate):
                number.is_part = True
                break
    return dict(parts=[number for number in numbers if number.is_part],
                rest=[number for number in numbers if not number.is_part])


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        schematic = [line.strip() for line in file]
        MAX_X = len(schematic[0])
        MAX_Y = len(schematic)

    groups = parse_schematic(schematic)
    parts = groups['parts']

    print('part 1')
    print(sum([n.value for n in parts]))

    print('part 2')
    result = 0
    for y, line in enumerate(schematic):
        for x, c in enumerate(line):
            if c == '*':
                # gear: get parts (this is inefficient because I don't feel like rewriting my part 1 code)
                connected_to_gear = [p.value for p in parts if (x, y) in p.neighbors()]
                if len(connected_to_gear) != 2:
                    continue
                result += connected_to_gear[0] * connected_to_gear[1]
    print(f'result: {result}')
