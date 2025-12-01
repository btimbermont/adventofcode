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
        self.current_value = (self.current_value + clicks) % (self.max_value+1)
        if self.current_value == self.value_to_watch:
            self.counter += 1

if __name__ == '__main__':
    dial = Dial(99, 0, 50)

    print("part 1")

    with open("input.txt", 'r') as file:
        for line in file:
            direction, value = line[0], int(line[1:])
            if direction == 'L':
                dial.left(value)
            else:
                dial.right(value)
    print(f'times at zero: {dial.counter}')

