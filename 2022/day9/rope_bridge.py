from dataclasses import dataclass
from typing import Tuple

Position = Tuple[int, int]


def max_distance(pos1: Position, pos2: Position) -> int:
    return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))


@dataclass
class Knot:
    positional_history: [Position]

    def current_position(self):
        return self.positional_history[-1]


class RopeHead(Knot):
    def __init__(self, start_position: Position = (0, 0)):
        self.positional_history = []
        self.positional_history.append(start_position)

    def move(self, direction: str):
        if direction == 'U':
            new_position = self.current_position()[0], self.current_position()[1] + 1
            self.positional_history.append(new_position)
        elif direction == 'D':
            new_position = self.current_position()[0], self.current_position()[1] - 1
            self.positional_history.append(new_position)
        elif direction == 'L':
            new_position = self.current_position()[0] - 1, self.current_position()[1]
            self.positional_history.append(new_position)
        elif direction == 'R':
            new_position = self.current_position()[0] + 1, self.current_position()[1]
            self.positional_history.append(new_position)
        else:
            raise Exception(f'Unknown direction: {direction}')


class FollowingKnot(Knot):
    def __init__(self, knot_to_follow: Knot):
        self.positional_history = []
        self._head = knot_to_follow
        self.positional_history.append(knot_to_follow.current_position())

    def has_to_move(self):
        # this knot has to move when it is too far from knot it should follow
        return max_distance(self.current_position(), self._head.current_position()) > 1

    def update_after_head_moved(self):
        if self.has_to_move():
            x_move, y_move = 0, 0
            if self.current_position()[0] != self._head.current_position()[0]:
                # if head is right of us: move right
                x_move = 1 if self._head.current_position()[0] > self.current_position()[0] else -1
            if self.current_position()[1] != self._head.current_position()[1]:
                # if head is above us: move upward
                y_move = 1 if self._head.current_position()[1] > self.current_position()[1] else -1

            # apply move to current position and store new position
            new_pos = self.current_position()[0] + x_move, self.current_position()[1] + y_move
            self.positional_history.append(new_pos)


class Rope:
    def __init__(self, start_pos: Position = (0, 0), knots: int = 1):
        self.head = RopeHead(start_pos)
        self.tail = []
        last_knot = self.head
        for i in range(knots):
            current_knot = FollowingKnot(last_knot)
            self.tail.append(current_knot)
            last_knot = current_knot

    def move(self, direction: str, times: int = 1):
        for i in range(times):
            self.head.move(direction)
            for knot in self.tail:
                knot.update_after_head_moved()

    def __str__(self):
        all_head_positions = self.head.positional_history
        min_x = min([pos[0] for pos in all_head_positions])
        max_x = max([pos[0] for pos in all_head_positions])
        min_y = min([pos[1] for pos in all_head_positions])
        max_y = max([pos[1] for pos in all_head_positions])
        start_pos = self.head.positional_history[0]
        head_pos = self.head.current_position()
        tail_positions = [knot.current_position() for knot in self.tail]
        all_tail_positions = self.tail[-1].positional_history
        lines = []
        for y in range(max_y, min_y - 1, -1):
            line = ''
            for x in range(min_x, max_x + 1):
                pos = (x, y)
                if pos == head_pos:
                    character = 'H'
                elif pos in tail_positions:
                    for i in range(len(tail_positions)):
                        if pos == tail_positions[i]:
                            character = str(i+1)
                            break
                elif pos == start_pos:
                    character = 'S'
                elif pos in all_tail_positions:
                    character = '#'
                else:
                    character = '.'
                line += character
            lines.append(line)
        return '\n'.join(lines)


if __name__ == '__main__':
    print('PART 1')
    rope = Rope()
    with open('input.txt', 'r') as file:
        for line in file.read().splitlines():
            direction, times = line.split(' ')
            rope.move(direction, int(times))
            # print(f'After move {line}:\n{rope}')
    with open('output_part1.txt', 'w') as file:
        file.write(rope.__str__())
    # print(rope)
    print(len(set(rope.tail[-1].positional_history)))

    print('PART 2')
    long_rope = Rope(knots=9)
    with open('input.txt', 'r') as file:
        for line in file.read().splitlines():
            direction, times = line.split(' ')
            long_rope.move(direction, int(times))
    with open('output_part2.txt', 'w') as file:
        file.write(long_rope.__str__())
    # print(long_rope)
    print(len(set(long_rope.tail[-1].positional_history)))
