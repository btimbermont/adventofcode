def is_invalid(id: int):
    id = str(id)
    i = len(id)
    if i % 2 != 0:
        return False
    return id[:i // 2] == id[i // 2:]

def is_invalid_part2(id: int):
    id = str(id)
    for i in range(1, 1+len(id)//2):
        if len(id) % i != 0:
            continue
        times = len(id)//i
        i_times = id[:i] * times
        if i_times == id:
            return True
    return False

if __name__ == '__main__':
    print("part 1")
    with open('input.txt', 'r') as file:
        segments = file.read().split(',')
    segments = [(int(s.split('-')[0]), int(s.split('-')[1])) for s in segments]
    # segments = sorted(segments, key=lambda s: s[0])

    invalid_ids = []
    for s in segments:
        for i in range(s[0], s[1] + 1):
            if is_invalid(i):
                invalid_ids.append(i)
                print(f'{i} is invalid')
    print(f'Sum: {sum(invalid_ids)}')

    print("part 2")
    invalid_ids = []
    for s in segments:
        for i in range(s[0], s[1] + 1):
            if is_invalid_part2(i):
                invalid_ids.append(i)
                print(f'{i} is invalid')
    print(f'Sum: {sum(invalid_ids)}')

