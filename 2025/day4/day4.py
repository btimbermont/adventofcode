from advent_utils.two_d_utils import String2dMap

if __name__ == '__main__':
    map = String2dMap('input.txt')
    print("part 1")
    access_rolls = []
    for roll in map.lookup_content('@'):
        neighbors = map.get_neighbors(roll, include_diagonals=True)
        neighboring_rolls = len([n for n in neighbors if map.get_cell(n) == '@'])
        if neighboring_rolls < 4:
            access_rolls.append(roll)
    print(len(access_rolls))