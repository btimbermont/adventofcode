from typing import List


class Shape:
    def __init__(self, outline: List[str]):
        if len(outline) == 0 or len(outline[0]) == 0:
            raise ValueError(f'Shape needs a strictly positive length and width: {outline}')
        self.height = len(outline)
        self.width = len(outline[0])
        for row in outline:
            if len(row) != self.width:
                raise ValueError(f'Not all rows are the same length in shape {outline}')
            for cell in row:
                if cell not in '#.':
                    raise ValueError(f'invalid cell "{cell}" in shape {outline}')
        self.outline = [list(row) for row in outline]

    def rotate(self) -> 'Shape':
        rotated_lines = []
        for x in range(self.width):
            line = ''
            for y in range(self.height - 1, -1, -1):
                line += self.outline[y][x]
            rotated_lines.append(line)
        return Shape(rotated_lines)

    def __str__(self):
        return '\n'.join([''.join(self.outline[y][x] for x in range(self.width)) for y in range(self.height)])


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [['.' for x in range(self.width)] for y in range(self.height)]

    def __str__(self):
        return '\n'.join([''.join(self.grid[y][x] for x in range(self.width)) for y in range(self.height)])

    def place_shape(self, shape: Shape, x: int, y: int, place_symbol: str = '#') -> bool:
        if not self.can_place(shape, x, y):
            raise ValueError(f'Cannot place shape at {x, y}')
        if len(place_symbol) != 1:
            raise ValueError(f'Invalid symbol for placing shapes: {place_symbol}')
        for j in range(shape.height):
            for i in range(shape.width):
                if shape.outline[j][i] == '#':
                    self.grid[y + j][x + i] = place_symbol

    def can_place(self, shape: Shape, x: int, y: int) -> bool:
        if x < 0 or (x + shape.width > self.width) or y < 0 or (y + shape.height > self.height):
            print(f'Shape does not fit within bounds of grid')
            return False
        for j in range(shape.height):
            for i in range(shape.width):
                if shape.outline[j][i] != '.':
                    if self.grid[y + j][x + i] != '.':
                        print(f'Cannot place shape at {x, y} because {x + i, y + j} is not free!')
                        return False
        return True


if __name__ == '__main__':
    g = Grid(20, 3)
    print(g)
    s = Shape(['###.#', '..###'])
    print()
    g.place_shape(s.rotate().rotate(), 0, 0, 'A')
    print(g)
    print()
    g.place_shape(s, 5, 1, 'B')
    print(g)
