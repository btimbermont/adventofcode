import math
import re
from math import sqrt
from typing import List


def quadratic_equation(a: float, b: float, c: float) -> None | float | List[float]:
    d = (b * b) - 4 * a * c
    if d < 0:
        print(f'Discriminant is negatief: {d}')
        return None
    if d == 0:
        return -b / (2 * a)
    if d > 0:
        sqrtd = sqrt(d)
        results = [(-b - sqrtd) / (2 * a), (-b + sqrtd) / (2 * a)]
        results.sort()
        return results


def calculate_millis_for_outcome(race_millis: int, distance: int) -> None | float | List[float]:
    """
    Given a race outcome, consisting of the milliseconds the race took, and the distance
    that the car traveled to se the record, this method returns how long the car was held
    to achieve this outcome.
    This is calculated by doing a simple quadratic equation, the result being x:
        -x^2 + a*x - b = 0
        with a being the length of the race (race_millis),
        b the distance that the car traveled,
        and x the number of seconds the car was held

    :param race_millis: how long this race took
    :param distance: the distance the car traveled
    :return: the number of milliseconds the car was held to achieve this result, can be
    either 0, 1 or 2 possibilities
    """
    return quadratic_equation(-1, race_millis, -distance)


def calculate_possibilities_to_beat_record(time: int, distance: int) -> int:
    record_options = calculate_millis_for_outcome(time, distance)
    # we have to assume there's 2 options, otherwise the records is impossible to beat
    # we round these numbers up and down to get the range of winning options
    lower_bound = int(math.ceil(record_options[0]))
    if lower_bound == record_options[0]:
        lower_bound += 1
    upper_bound = int(math.floor(record_options[1]))
    if upper_bound == record_options[1]:
        upper_bound -= 1
    possibilities = upper_bound - lower_bound + 1
    return possibilities


if __name__ == '__main__':
    values = {}
    with open('test.txt', 'r') as file:
        for line in file:
            match = re.match(r'(\S+):\s*(\d+(\s+\d+)*)', line)
            header = match.group(1)
            numbers_str = match.group(2)
            numbers = list(map(int, numbers_str.split()))
            values[header] = numbers
    print(values)
    print('part 1')
    records = list(zip(values['Time'], values['Distance']))
    result = 1
    for i, record in enumerate(records):
        time = record[0]
        distance = record[1]
        possibilities = calculate_possibilities_to_beat_record(time, distance)
        print(
            f'{i + 1}) record: {record}, {possibilities} possible new records')
        result *= possibilities
    print(result)

    print('part 2')
    print(calculate_possibilities_to_beat_record(38677673, 234102711571236))
