word_to_number = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}


def replace_words_with_numbers(input_str):
    for key, value in word_to_number.items():
        input_str = input_str.replace(key, f'{key}{value}{key}')
    return input_str


def str_to_int(input: str) -> [int]:
    return [int(a) for a in input if a.isdigit()]


def process_line(line: str) -> int:
    ints = str_to_int(line)
    return int(''.join([str(ints[0]), str(ints[-1])]))


if __name__ == '__main__':
    print('starting part 1')
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        total = 0
        for line in file:
            line_value = process_line(line)
            # print(f'{line} -> {line_value}')
            total += line_value
        print(f'total value = {total}')

    print('starting part 2')
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        total = 0
        for line in file:
            numbers = replace_words_with_numbers(line)
            line_value = process_line(numbers)
            print(f'{line} -> {numbers} -> {line_value}')
            total += line_value
        print(f'total value = {total}')
