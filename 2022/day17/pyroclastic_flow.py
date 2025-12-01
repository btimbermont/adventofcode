from dataclasses import dataclass

BLOCKS = []


@dataclass
class Pixel:
    x: int
    y: int

    def __add__(self, other):
        return Pixel(self.x + other.x, self.y + other.y)

    def copy(self) -> 'Pixel':
        return Pixel(self.x, self.y)


@dataclass()
class Bounds:
    top_left: Pixel
    bottom_right: Pixel

    @staticmethod
    def of_pixels(pixels: [Pixel]) -> 'Bounds':
        min_x, max_x = 1000, -1000
        min_y, max_y = 1000, -1000
        for p in pixels:
            min_x = min(min_x, p.x)
            min_y = min(min_y, p.y)
            max_x = max(max_x, p.x)
            max_y = max(max_y, p.y)
        return Bounds(Pixel(min_x, min_y), Pixel(max_x, max_y))

    def move(self, offset: Pixel):
        self.top_left += offset
        self.bottom_right += offset

    def contains(self, pixel: Pixel) -> bool:
        return self.top_left.x <= pixel.x <= self.bottom_right.x and self.top_left.y <= pixel.y <= self.bottom_right.y

    def copy(self) -> 'Bounds':
        return Bounds(self.top_left.copy(), self.bottom_right.copy())


class Block:
    def __init__(self, pixels: [Pixel]):
        self.pixels = pixels
        self.bounds = Bounds.of_pixels(pixels)

    @staticmethod
    def from_lines(lines: [str]) -> 'Block':
        pixels = []
        y = 0
        for line in lines:
            x = 0
            for c in line:
                if c == '#':
                    pixels.append(Pixel(x, y))
                x += 1
            y += 1
        return Block(pixels)

    def move(self, offset: Pixel):
        self.bounds.move(offset)
        self.pixels = [offset + p for p in self.pixels]

    def collides_with(self, pixels: [Pixel]):
        for other_pixel in pixels:
            if self.bounds.contains(other_pixel):
                if other_pixel in self.pixels:
                    return True
        return False

    def copy(self) -> 'Block':
        clone = Block([])
        clone.pixels = [p.copy() for p in self.pixels]
        clone.bounds = self.bounds.copy()
        return clone

    def print(self):
        for y in range(self.bounds.top_left.y, self.bounds.bottom_right.y + 1):
            line = ''
            for x in range(self.bounds.top_left.x, self.bounds.bottom_right.x + 1):
                line += '#' if Pixel(x, y) in self.pixels else '.'
            print(line)


def load_blocks(path: str) -> [Block]:
    blocks = []
    with open(path) as f:
        lines = []
        for line in f.readlines():
            if '#' in line:
                lines.append(line)
            else:
                blocks.append(Block.from_lines(lines))
                lines = []
        if len(lines) > 0:
            blocks.append(Block.from_lines(lines))
    return blocks


def get_block(turn: int) -> Block:
    return BLOCKS[turn % len(BLOCKS)]


if __name__ == '__main__':
    BLOCKS = load_blocks('blocks.txt')
    for i in range(10):
        print(f'block for turn {i}:')
        get_block(i).print()
