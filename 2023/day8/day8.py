import math
import re
from typing import Dict

NODE_PARSER = re.compile('(...) = \\((...), (...)\\)')

if __name__ == '__main__':
    instructions: str = None
    nodes: [Dict[str, str]] = []
    with open('input.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if not instructions:
                instructions = line
            if NODE_PARSER.match(line):
                node = {'name': (NODE_PARSER.match(line).groups())[0],
                        'L': (NODE_PARSER.match(line).groups())[1],
                        'R': (NODE_PARSER.match(line).groups())[2]}
                nodes.append(node)
    map = {node['name']: node for node in nodes}
    for node in map.values():
        node['L'] = map.get(node['L'])
        node['R'] = map.get(node['R'])

    print('part 1')
    current_node = map.get('AAA')
    destination = map.get('ZZZ')
    next_instruction = 0
    step = 0
    while current_node != destination:
        # print(f'Currently at {current_node["name"]}, going {instructions[next_instruction]}')
        current_node = current_node[instructions[next_instruction]]
        step += 1
        next_instruction = (next_instruction + 1) % len(instructions)
    print(step)

    print('part 2')
    start_nodes = [node for node in nodes if node['name'].endswith('A')]
    cycles = []
    for current_node in start_nodes:
        next_instruction = 0
        step = 0
        while not current_node['name'].endswith('Z'):
            current_node = current_node[instructions[next_instruction]]
            step += 1
            next_instruction = (next_instruction + 1) % len(instructions)
        cycles.append(step)
    print(math.lcm(*cycles))
