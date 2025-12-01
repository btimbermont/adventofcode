import functools
from typing import List, Union

PacketPair = (List, List)


def parse_lines(lines: [str]) -> [PacketPair]:
    packet_pairs = []
    for i in range(0, len(lines), 3):
        left = eval(lines[i])
        right = eval(lines[i + 1])
        packet_pairs.append((left, right))
    return packet_pairs


def packets_in_order(left: Union[int, List], right: Union[int, List]) -> int:
    # return negative if not in order, positive if in order, 0 if equal
    # if one is int and the other is list: wrap int in list
    if type(left) != type(right):
        if isinstance(left, int):
            return packets_in_order([left], right)
        else:
            return packets_in_order(left, [right])
    # types are the same: first check ints:
    if isinstance(left, int):
        return right - left
    # both lists: compare each item
    for i in range(max(len(left), len(right))):
        if i >= len(left):  # If the left list runs out of items first, the inputs are in the right order
            return 1
        if i >= len(right):  # If the right list runs out of items first, the inputs are not in the right order
            return -1
        element_cmp = packets_in_order(left[i], right[i])
        if element_cmp == 0:  # keep going if elements are the same
            continue
        else:  # return result if elements are not the same
            return element_cmp
    return 0


if __name__ == '__main__':
    with open('input.txt') as file:
        packet_pairs = parse_lines(file.read().splitlines())
    print('PART 1')
    print(f'We have {len(packet_pairs)} pairs: {packet_pairs}')
    s = 0
    for i in range(len(packet_pairs)):
        in_order = packets_in_order(packet_pairs[i][0], packet_pairs[i][1]) > 0
        print(f'Packet {i + 1} is in order' if in_order else f'Packet {i + 1} is NOT in order')
        if in_order:
            s += i + 1
    print(f'Sum of indices of in order packets: {s}')

    print('PART 2')
    all_packets = [packet for pair in packet_pairs for packet in pair]
    divider1, divider2 = [[2]], [[6]]
    all_packets.append(divider1)
    all_packets.append(divider2)
    all_packets = sorted(all_packets, key=functools.cmp_to_key(packets_in_order), reverse=True)
    print('Sorted packets:')
    print('\n'.join([p.__str__() for p in all_packets]))
    i1 = all_packets.index(divider1)+1
    i2 = all_packets.index(divider2)+1
    print(f'decoder key: {i1*i2}')
