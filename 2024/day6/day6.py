from typing import List, Tuple


def guard_next_location(location: Tuple[int, int], orientation: str):
    match orientation:
        case '^':
            return location[0], location[1] - 1
        case '>':
            return location[0] + 1, location[1]
        case 'V':
            return location[0], location[1] + 1
        case '<':
            return location[0] - 1, location[1]
        case _:
            raise ValueError(f'Not a guard: "{orientation}" at {location}')


def rotate_right(orientation: str):
    match orientation:
        case '^':
            return '>'
        case '>':
            return 'V'
        case 'V':
            return '<'
        case '<':
            return '^'
        case _:
            raise ValueError(f'Not a guard: "{orientation}"')


class Map:
    def __init__(self, lines: List[str]):
        self.lines = [list(line) for line in lines]
        self.visit_history = [['' for _ in line] for line in lines]
        self.loop_detected = False
        self._find_guard()
        self.mark_guard_location()
        self.max_x = len(lines[0])
        self.max_y = len(lines)

    def _find_guard(self):
        for y, line in enumerate(self.lines):
            for x, cell in enumerate(line):
                if cell in '^>V<':
                    self.guard_location = (x, y)
                    self.guard_orientation = cell
                    return
        raise ValueError('Cannot find guard!')

    def mark_guard_location(self):
        self.remember_location()
        old_value = self._get_cell(self.guard_location)
        if old_value == '+':
            return
        current_mark = '-' if self.guard_orientation in '<>' else '|'
        if old_value not in '-|':
            self._set_cell(self.guard_location, current_mark)
        elif old_value == '-' and current_mark == '|':
            self._set_cell(self.guard_location, '+')
        elif old_value == '|' and current_mark == '-':
            self._set_cell(self.guard_location, '+')

    def remember_location(self):
        x,y = self.guard_location
        self.loop_detected = self.guard_orientation in self.visit_history[y][x]
        self.visit_history[y][x] += (self.guard_orientation)

    def _get_cell(self, coordinates: Tuple[int, int]) -> str:
        return self.lines[coordinates[1]][coordinates[0]]

    def _set_cell(self, coordinates: Tuple[int, int], new_val: str):
        self.lines[coordinates[1]][coordinates[0]] = new_val

    def advance_step(self) -> bool:
        next_location = guard_next_location(self.guard_location, self.guard_orientation)
        # finished?
        if not self._in_bounds(next_location):
            return False
        # should we rotate?
        if self._in_bounds(next_location) and self._get_cell(next_location) in '#O':
            self.guard_orientation = rotate_right(self.guard_orientation)
            self.mark_guard_location()
            return self.advance_step()
        # advance one step
        self.guard_location = next_location
        self.mark_guard_location()
        return not self.loop_detected

    def _in_bounds(self, location: Tuple[int, int]) -> bool:
        x_ok = 0 <= location[0] < self.max_x
        y_ok = 0 <= location[1] < self.max_y
        return x_ok and y_ok

    def get_visited_locations(self) -> List[Tuple[int, int]]:
        visited_locations = []
        for y, line in enumerate(self.lines):
            for x, cell in enumerate(line):
                if cell in '-|+':
                    visited_locations.append((x, y))
        return visited_locations

    def __str__(self):
        return "\n".join([
            "".join([
                cell if (x, y) != self.guard_location else self.guard_orientation
                for x, cell in enumerate(line)
            ])
            for y, line in enumerate(self.lines)
        ])


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        file_content = file.read().splitlines()
    print('part 1')
    m = Map(file_content)
    while True:
        keep_going = m.advance_step()
        if not keep_going:
            break
    print(len(m.get_visited_locations()))
    # print(m)
    print('part 2')
    candidates = m.get_visited_locations()
    loops = []
    print(f'testing {len(candidates)} candidates')
    for i, candidate in enumerate(candidates):
        if i%100 == 0:
            print(f'testing candidate {i}')
        m = Map(file_content)
        m._set_cell(candidate, 'O')
        while True:
            keep_going = m.advance_step()
            if not keep_going:
                break
        if m.loop_detected:
            loops.append(candidate)
            # print(f'====\n{m}\n{candidate}\n====')
    # print(loops)
    print(len(loops))
