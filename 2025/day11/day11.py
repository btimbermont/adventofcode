from dataclasses import dataclass
from typing import List


@dataclass
class Node:
    name: str
    paths: List['Node']
    reachable: List[str] = None

    def __repr__(self):
        return f'Node({self.name}, {[p.name for p in self.paths]})'

    def __str__(self):
        return self.__repr__()

    def paths_to(self, destination: str, forbidden_nodes: List[str] = []) -> int:
        if self.name == destination:
            return 1
        if destination not in self.reachable:
            return 0
        return sum([p.paths_to(destination, forbidden_nodes) for p in self.paths if p.name not in forbidden_nodes])


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
    # have each node list its reachable paths
    for n in nodes.values():
        update_reachable(n)
    return nodes


def update_reachable(node: Node):
    if node.reachable is None:
        reachable = set()
        reachable.add(node.name)
        for p in node.paths:
            update_reachable(p)
            reachable.update(p.reachable)
        node.reachable = reachable


if __name__ == '__main__':
    print('part 1')
    nodes = parse_graph('input.txt')
    print(nodes['you'].paths_to('out'))

    print('part 2')
    nodes = parse_graph('input.txt')
    result = 0
    if 'dac' in nodes['fft'].reachable:
        # fft > dac
        print('a...')
        a = nodes['svr'].paths_to('fft', ['dac'])
        print('b...')
        b = nodes['fft'].paths_to('dac')
        print('c...')
        c = nodes['dac'].paths_to('out')
        result += a * b * c
    else:
        print("Can't do fft > dac")
    if 'fft' in nodes['dac'].reachable:
        # dac > fft
        print('a...')
        a = nodes['svr'].paths_to('dac', ['fft'])
        print('b...')
        b = nodes['dac'].paths_to('fft')
        print('c...')
        c = nodes['fft'].paths_to('out')
        result += a * b * c
    else:
        print("Can't do dac > fft")
    print(result)
