from dataclasses import dataclass


@dataclass
class CubeCount:
    red: int
    green: int
    blue: int

    def fits_in(self, other_cube_count: 'CubeCount'):
        return self.red <= other_cube_count.red and self.green <= other_cube_count.green and self.blue <= other_cube_count.blue

    def power(self) -> int:
        return self.red * self.green * self.blue


def expand_bag_contents(a: CubeCount, b: CubeCount) -> CubeCount:
    return CubeCount(max(a.red, b.red), max(a.green, b.green), max(a.blue, b.blue))


@dataclass
class Game:
    id: int
    turns: [CubeCount]

    def minimum_bag_contents(self) -> CubeCount:
        minimal_contents = CubeCount(0, 0, 0)
        for turn in self.turns:
            minimal_contents = expand_bag_contents(minimal_contents, turn)
        return minimal_contents

    def is_possible(self, bag: CubeCount):
        minimal_bag_contents = self.minimum_bag_contents()
        return minimal_bag_contents.fits_in(bag)


def parse_turn(turn_str: str) -> CubeCount:
    color_counts = dict(red=0, green=0, blue=0)
    for color_grab in turn_str.split(','):
        color_grab_parsed = color_grab.split(' ')
        color_counts[color_grab_parsed[-1].strip()] = int(color_grab_parsed[-2])
    return CubeCount(color_counts["red"], color_counts["green"], color_counts["blue"])


def parse_game(line: str) -> Game:
    game_part = line.split(':')[0]
    turns_part = line.split(':')[1]

    game_id = int(game_part.split(' ')[-1])
    turns = [parse_turn(turn) for turn in turns_part.split(';')]
    return Game(game_id, turns)


if __name__ == '__main__':
    bag_contents = CubeCount(12, 13, 14)
    with open('input.txt', 'r') as file:
        games = [parse_game(line) for line in file]

    print('part 1')
    game_ids = [game.id for game in games if game.is_possible(bag_contents)]
    print(sum(game_ids))

    print('part 2')
    powers = [game.minimum_bag_contents().power() for game in games]
    print(sum(powers))
