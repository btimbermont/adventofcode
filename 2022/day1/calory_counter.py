def group_lines(lines: [str]) -> [[int]]:
    result = []
    current = []
    for line in lines:
        if len(line):
            current.append(int(line))
        else:
            result.append(current)
            current = []
    # append last batch
    if len(current):
        result.append(current)
    return result


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        calory_groups_per_elf = group_lines(file.read().splitlines())
        calories_per_elf = [sum(group) for group in calory_groups_per_elf]
        calories_per_elf.sort()
        print(f'highest calories: {calories_per_elf[-1]}')
        top_three = calories_per_elf[-3:]
        print(f'top 3: {top_three}, total: {sum(top_three)}')
