from typing import List, Dict


def count_occurrences(line: str, word: str) -> int:
    return line.count(word) + line.count(word[::-1])


def get_vertical_lines(lines: List[str]) -> List[str]:
    result = []
    for i in range(len(lines[0])):
        result.append(''.join([l[i] for l in lines]))
    return result


def get_diagonals(lines: List[str]) -> List[str]:
    x = len(lines[0])
    y = len(lines)
    resultsa: Dict[int, str] = {}
    resultsb: Dict[int, str] = {}
    for i in range(x):
        for j in range(y):
            resultsa[j - i] = resultsa.get(j - i, '') + lines[i][j]
            resultsb[i + j] = lines[i][j] + resultsb.get(i + j, '')
    return list(resultsa.values()) + list(resultsb.values())


def count_all_occurences(lines: List[str], word: str) -> int:
    result = 0
    result = result + sum([count_occurrences(line, word) for line in lines])
    result = result + sum([count_occurrences(line, word) for line in get_vertical_lines(lines)])
    result = result + sum([count_occurrences(line, word) for line in get_diagonals(lines)])
    return result


def verify_XM_MAS(lines: List[str], i: int, j: int) -> bool:
    if lines[i][j] != 'A':
        return False
    diagonal1 = lines[i-1][j-1] + lines[i][j] + lines[i+1][j+1]
    if diagonal1 not in ['MAS', 'SAM']:
        return False
    diagonal2 = lines[i-1][j+1] + lines[i][j] + lines[i+1][j-1]
    if diagonal2 not in ['MAS', 'SAM']:
        return False
    return True


def count_X_MAS(lines: List[str]) -> int:
    x = len(lines[0])
    y = len(lines)
    count = 0
    for j in range(1, y - 1):
        for i in range(1, x - 1):
            if verify_XM_MAS(lines, i, j):
                count = count + 1
    return count


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        input = file.read().splitlines()
    print('part 1')
    print(count_all_occurences(input, 'XMAS'))
    print('part 2')
    print(count_X_MAS(input))
