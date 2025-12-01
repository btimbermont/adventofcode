RESULTS = ['draw', 'win', 'loss']
RESULT_SCORE = dict(loss=0, draw=3, win=6)
MOVE_SCORE = [1, 2, 3]


def translate_move(move: str) -> int:
    if move in 'AX':
        return 0  # rock
    if move in 'BY':
        return 1  # paper
    if move in 'CZ':
        return 2  # scissors


def translate_outcome(outcome: str) -> str:
    return RESULTS[(translate_move(outcome) - 1) % 3]


def translate_game(line: str) -> (int, int):
    return tuple([translate_move(move) for move in line.split(' ')])


def translate_game_part2(line: str) -> (int, int):
    their_move, outcome = line.split(' ')
    their_move = translate_move(their_move)
    outcome = translate_outcome(outcome)
    my_move = (their_move + ((RESULT_SCORE[outcome] // 3) - 1)) % 3
    print(f'their move: {their_move}, outcome: {outcome}, my move: {my_move}')

    return their_move, my_move


def game_score(my_move: int, their_move: int) -> int:
    result = (my_move - their_move) % 3  # 0 = draw, 1= win, 2=loss
    return RESULT_SCORE[RESULTS[result]]


def move_score(my_move: int) -> int:
    return MOVE_SCORE[my_move]


def calculate_score(line: str) -> int:
    their_move, my_move = translate_game(line)
    return game_score(my_move, their_move) + move_score(my_move)


def calculate_score_part2(line: str) -> int:
    their_move, my_move = translate_game_part2(line)
    return game_score(my_move, their_move) + move_score(my_move)


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        lines = file.read().splitlines()
        points = [calculate_score(line) for line in lines]
    print(sum(points))
    print("PART 2")
    with open('input.txt', 'r') as file:
        lines = file.read().splitlines()
        points = [calculate_score_part2(line) for line in lines]
    print(sum(points))
