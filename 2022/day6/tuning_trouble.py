import itertools
from collections import deque


class Buffer:
    def __init__(self, min_size: int):
        self._buffer = deque()
        self._buffer_size = min_size

    def read_next(self, char: str):
        self._buffer.append(char)
        while len(self._buffer) > self._buffer_size:
            self._buffer.popleft()

    def has_distinct_characters(self) -> bool:
        if len(self._buffer) != self._buffer_size:
            return False
        for i in range(self._buffer_size - 1):
            if self._buffer[i] in itertools.islice(self._buffer, i + 1, len(self._buffer)):
                return False
        return True

    def __repr__(self):
        return f'[buffer: {self._buffer} distinct chars: {self.has_distinct_characters()}]'

    def __str__(self):
        return self.__repr__()


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        input = file.read()
        print('PART 1')
        buffer = Buffer(4)
        for i in range(len(input)):
            buffer.read_next(input[i])
            if buffer.has_distinct_characters():
                print(f'start of packet at {i+1}')
                break
        print('PART 2')
        buffer = Buffer(14)
        for i in range(len(input)):
            buffer.read_next(input[i])
            if buffer.has_distinct_characters():
                print(f'start of message at {i + 1}')
                break
