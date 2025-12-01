from typing import List

from advent_utils.two_d_utils import String2dMap, Point


class MemorySpace(String2dMap):
    def __init__(self, size: int):
        input = "." * size
        input = input + "\n"
        input = input * size
        super().__init__(input=input)

    def corrupt(self, corrupted_addresses=List[Point]):
        for point in corrupted_addresses:
            self.set_cell(point, '#')


def load_corruption(path: str) -> List[Point]:
    addresses = []
    with open(path, 'r') as file:
        for line in file.read().splitlines():
            x, y = line.split(',')
            addresses.append((int(x), int(y)))
    return addresses


if __name__ == '__main__':
    # test input
    input = 'test_input.txt'
    size = 7
    # real input
    input = 'input.txt'
    size = 71
    corruption = load_corruption(input)

    print('part 1')
    memory = MemorySpace(size)
    memory.corrupt(corruption[:1024])
    print(memory)
    dist = memory.get_shortest_distance((0, 0), (size - 1, size - 1))
    print(dist)

