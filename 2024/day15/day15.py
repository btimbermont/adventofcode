from dataclasses import dataclass
from typing import Callable

from advent_utils.two_d_utils import String2dMap, Point


@dataclass
class Movement:
    direction: str
    apply: Callable[[Point], Point]


MOVEMENTS = {
    '^': Movement('^', lambda p: (p[0], p[1] - 1)),
    '>': Movement('>', lambda p: (p[0] + 1, p[1])),
    'v': Movement('v', lambda p: (p[0], p[1] + 1)),
    '<': Movement('<', lambda p: (p[0] - 1, p[1]))
}


class Warehouse(String2dMap):
    def __init__(self, input: str):
        super().__init__(input=input)

    @property
    def submarine(self) -> Point:
        return self.lookup['@'][0]

    @property
    def boxes(self):
        single_boxes = self.lookup.get('O', [])
        double_boxes = self.lookup.get('[', [])
        return single_boxes + double_boxes

    def process_movement(self, movement: str) -> bool:
        if movement not in MOVEMENTS.keys():
            print(f'UNKNOWN MOVEMENT: {movement}')
            return False
        movement = MOVEMENTS[movement]
        if not self._can_move(self.submarine, movement):
            return False
        self._process_movement_no_checks(self.submarine, movement)
        return True

    def _can_move(self, cell_to_move: Point, movement: Movement):
        cell_content = self.get_cell(cell_to_move)
        if cell_content is None or cell_content == '#':
            return False
        if cell_content == '.':
            return True
        # cell has content: check if target cell can move
        target_cell = movement.apply(cell_to_move)
        target_cell_content = self.get_cell(target_cell)
        # if target cell is double box: check both parts
        if movement.direction in '<>' or target_cell_content not in '[]':
            return self._can_move(target_cell, movement)
        elif target_cell_content == '[':
            neighbor = target_cell[0] + 1, target_cell[1]
            return self._can_move(target_cell, movement) and self._can_move(neighbor, movement)
        elif target_cell_content == ']':
            neighbor = target_cell[0] - 1, target_cell[1]
            return self._can_move(target_cell, movement) and self._can_move(neighbor, movement)
        else:
            raise ValueError('Unknown state')

    def _process_movement_no_checks(self, cell_to_move: Point, move_op: Movement):
        cell_content = self.get_cell(cell_to_move)
        if cell_content is None or cell_content in '#.':
            return
        target_cell = move_op.apply(cell_to_move)
        target_cell_content = self.get_cell(target_cell)
        if move_op.direction in 'v^' and target_cell_content in '[]':
            if target_cell_content == '[':
                neighbor = target_cell[0] + 1, target_cell[1]
                self._process_movement_no_checks(target_cell, move_op)
                self._process_movement_no_checks(neighbor, move_op)
            else:
                neighbor = target_cell[0] - 1, target_cell[1]
                self._process_movement_no_checks(neighbor, move_op)
                self._process_movement_no_checks(target_cell, move_op)

        # else: submarine or single box
        else:
            self._process_movement_no_checks(target_cell, move_op)
        self.set_cell(target_cell, cell_content)
        self.set_cell(cell_to_move, '.')

    def gps_value(self):
        value = 0
        for box in self.boxes:
            value += box[0] + 100 * box[1]
        return value


def expand_map(map: str) -> str:
    new_lines = []
    for line in map.splitlines():
        new_line = ''
        for c in line:
            match c:
                case '.':
                    new_line += '..'
                case '#':
                    new_line += '##'
                case 'O':
                    new_line += '[]'
                case '@':
                    new_line += '@.'
                case _:
                    print(f'unknown character: {c}')
        new_lines.append(new_line)
    return '\n'.join(new_lines)


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        warehouse_text, movements = file.read().split('\n\n')
    warehouse = Warehouse(warehouse_text)
    print('part1')
    for m in movements:
        warehouse.process_movement(m)
    print(warehouse)
    print(warehouse.gps_value())

    print('part 2')
    warehouse = Warehouse(expand_map(warehouse_text))
    print(warehouse)
    for m in movements:
        warehouse.process_movement(m)
    print(warehouse)
    print(warehouse.gps_value())
