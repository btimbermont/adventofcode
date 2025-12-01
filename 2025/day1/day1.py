from dataclasses import dataclass


@dataclass
class Dial:
    max_value: int
    value_to_watch: int
    current_value: int
    counter: int = 0

    def left(self, clicks: int):
        self.right(-clicks)

    def right(self, clicks: int):
        self.current_value = (self.current_value + clicks) % (self.max_value + 1)
        if self.current_value == self.value_to_watch:
            self.counter += 1


@dataclass
class DialPart2:
    max_value: int
    value_to_watch: int
    current_value: int
    counter: int = 0

    def left(self, clicks: int):
        while clicks > 0:
            clicks -= 1
            self.current_value = (self.current_value - 1) % (self.max_value + 1)
            if self.current_value == 0:
                self.counter += 1

    def right(self, clicks: int):
        while clicks > 0:
            clicks -= 1
            self.current_value = (self.current_value + 1) % (self.max_value + 1)
            if self.current_value == 0:
                self.counter += 1


if __name__ == '__main__':
    print("part 1")
    dial = Dial(99, 0, 50)
    with open("input.txt", 'r') as file:
        for line in file:
            direction, value = line[0], int(line[1:])
            if direction == 'L':
                dial.left(value)
            else:
                dial.right(value)
    print(f'times at zero: {dial.counter}')

    print("part 2")
    dial = DialPart2(99, 0, 50)
    with open("input.txt", 'r') as file:
        for line in file:
            direction, value = line[0], int(line[1:])
            if direction == 'L':
                dial.left(value)
            else:
                dial.right(value)
    print(f'times at zero: {dial.counter}')
