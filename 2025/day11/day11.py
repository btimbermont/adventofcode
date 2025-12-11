from dataclasses import dataclass
from typing import List


@dataclass
class Node:
    name: str
    paths: List['Node']

    def __repr__(self):
        return f'Node({self.name}, {[p.name for p in self.paths]})'

    def __str__(self):
        return self.__repr__()

    def paths_to(self, destination: str) -> int:
        if self.name == destination:
            return 1
        return sum([p.paths_to(destination) for p in self.paths])


def parse_graph(input: str):
    nodes = dict()
    with open(input, 'r') as file:
        for line in file:
            name, paths = line.split(':')
            # create if needed
            if name not in nodes.keys():
                nodes[name] = Node(name, [])
            paths = paths.strip().split()
            for p in paths:
                if p not in nodes.keys():
                    nodes[p] = Node(p, [])
                nodes[name].paths.append(nodes[p])
    return nodes


if __name__ == '__main__':
    nodes = parse_graph('input.txt')
    print(nodes)
    print('part 1')
    print(nodes['you'].paths_to('out'))
