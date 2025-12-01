import re
from pathlib import Path
from typing import List


def read_muls(path: Path) -> List[str]:
    with open(path, 'r') as file:
        input = file.read()
    regex = "mul\\(\\d{1,3},\\d{1,3}\\)"
    return re.findall(regex, input)


def do_mul(mul: str) -> int:
    pattern = "mul\\((\\d{1,3}),(\\d{1,3})\\)"
    match = re.search(pattern, mul)
    a, b = int(match.group(1)), int(match.group(2))
    return a * b


def read_muls_and_dos(path: Path) -> List[str]:
    with open(path, 'r') as file:
        input = file.read()
    regex = "mul\\(\\d{1,3},\\d{1,3}\\)|do\\(\\)|don't\\(\\)"
    return re.findall(regex, input)


def filter_do_and_dont(input: List[str]) -> List[str]:
    output = []
    ignore = False
    for op in input:
        if op == "don't()":
            ignore = True
        elif op == "do()":
            ignore = False
        else:
            if not ignore:
                output.append(op)
    return output


if __name__ == '__main__':
    print("part 1")
    muls = read_muls(Path('input.txt'))
    print(sum([do_mul(mul) for mul in muls]))
    print("part 2")
    muls_and_dos = read_muls_and_dos(Path('input.txt'))
    muls = filter_do_and_dont(muls_and_dos)
    print(sum([do_mul(mul) for mul in muls]))
