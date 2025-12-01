from collections import deque


def parse_stacks_line(line: str) -> [str]:
    return [line[i+1] for i in range(0, len(line), 4)]


class Move:
    def __init__(self, line: str):
        words = line.split(' ')
        self.amount = int(words[1])
        self.source = int(words[3]) - 1
        self.dest = int(words[5]) - 1


class Stacks:
    def __init__(self, input_file: str):
        levels = []
        with open(input_file, 'r') as file:
            for line in file.read().splitlines():
                if line == '':
                    break
                levels.append(parse_stacks_line(line))
        # process levels upwards
        levels.reverse()
        # first level: number of stacks
        self._stacks = [deque() for i in levels[0]]
        # other levels: parse
        for level in levels[1:]:
            for i in range(len(level)):
                if level[i] != ' ':
                    self._stacks[i].append(level[i])

    def apply(self, move: Move):
        for i in range(move.amount):
            crate = self._stacks[move.source].pop()
            self._stacks[move.dest].append(crate)

    def apply_new(self, move: Move):
        crates = deque()
        for i in range(move.amount):
            crates.append(self._stacks[move.source].pop())
        while len(crates):
            self._stacks[move.dest].append(crates.pop())

    def current_message(self) -> str:
        message = ''
        for _stack in self._stacks:
            if len(_stack) > 0:
                message += _stack[-1]
            else:
                message += ' '
        return message


if __name__ == '__main__':
    print('PART 1')
    input = 'input.txt'
    stacks = Stacks(input)
    moves = []
    with open(input, 'r') as file:
        for line in file.read().splitlines():
            if line.startswith('move'):
                moves.append(Move(line))
    for move in moves:
        stacks.apply(move)
    print(stacks.current_message())
    print('PART 2')
    input = 'input.txt'
    stacks = Stacks(input)
    moves = []
    with open(input, 'r') as file:
        for line in file.read().splitlines():
            if line.startswith('move'):
                moves.append(Move(line))
    for move in moves:
        stacks.apply_new(move)
    print(stacks.current_message())