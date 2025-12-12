import re
from typing import List


class Shape:
    def __init__(self, outline: List[str]):
        if len(outline) == 0 or len(outline[0]) == 0:
            raise ValueError(f'Shape needs a strictly positive length and width: {outline}')
        self.height = len(outline)
        self.width = len(outline[0])
        self.area = 0
        for row in outline:
            if len(row) != self.width:
                raise ValueError(f'Not all rows are the same length in shape {outline}')
            for cell in row:
                if cell not in '#.':
                    raise ValueError(f'invalid cell "{cell}" in shape {outline}')
                if cell == '#':
                    self.area += 1
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

    def fits(self, shapes: List[Shape], shape_counts: List[int]):
        # if number of # is larger than grid, no use in trying to fit
        shapes_inner_area = 0
        for i in range(len(shapes)):
            inner_area = shapes[i].area
            shapes_inner_area += inner_area * shape_counts[i]
        if shapes_inner_area > self.width * self.height:
            print('Even with perfect packing these shapes won\'t fit!')
            return False
        # each shape is 3x3, if each shape has its own 3x3 square, no need to pack
        shapes_x, shapes_y = self.width // 3, self.height // 3
        total_shapes = sum(shape_counts)
        if total_shapes <= shapes_x * shapes_y:
            print('No need to pack, these shapes will work!')
            return True
        print(f'Easy approaches don\'t work, you need to implement packing...')
        return None


if __name__ == '__main__':
    reading_shape = False
    shapes = []
    grids_and_shapes = []
    with open('input.txt', 'r') as file:
        for line in file:
            if re.match(r'\d:', line):
                reading_shape = True
                shape_lines = []
            elif reading_shape and line.strip():
                shape_lines.append(line.strip())
            elif reading_shape and not line.strip():
                shapes.append(Shape(shape_lines))
                reading_shape = False
                shape_lines = []
            elif re.match(r'\d+x\d+:.*', line):
                grid, shape_counts = line.strip().split(':')
                w, h = grid.split('x')
                grid = Grid(int(w), int(h))
                shape_counts = [int(i) for i in shape_counts.split()]
                grids_and_shapes.append((grid, shape_counts))
                shape_counts = []
    print(f'done parsing!')

    known_fits, known_not_fits, unknowns = 0, 0, 0
    for grid, shape_counts in grids_and_shapes:
        result = grid.fits(shapes, shape_counts)
        if result is None:
            unknowns +=1
        elif result == True:
            known_fits +=1
        elif result == False:
            known_not_fits +=1
    print(f'{known_fits} will 100% fit, {known_not_fits} will 100% not, {unknowns} are unknown without packing code')
