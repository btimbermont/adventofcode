from functools import cache
from typing import Set, List


class Computer:
    def __init__(self, name: str):
        self.name = name
        self.connections = set()

    def make_connection(self, other_computer: 'Computer'):
        self.connections.add(other_computer)

    def get_clusters(self) -> Set['TriCluster']:
        clusters = set()
        for other_pc in self.connections:
            for third_pc in other_pc.connections:
                if self in third_pc.connections:
                    clusters.add(TriCluster(self, other_pc, third_pc))
        return clusters

    def __lt__(self, other):
        return self.name.__lt__(other.name)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f'Computer({self.name})'

    def __repr__(self):
        return f'Computer({self.name})'


class TriCluster:
    def __init__(self, c1: Computer, c2: Computer, c3: Computer):
        self.computers = [c1, c2, c3]
        self.computers.sort(key=lambda c: c.name)

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return f'Cluster({",".join([c.name for c in self.computers])})'

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return str(self).__lt__(str(other))


class Cluster:
    def __init__(self):
        self.computers: List[Computer] = []

    def copy(self) -> 'Cluster':
        c = Cluster()
        c.computers = self.computers.copy()
        return c

    def try_add(self, computer: Computer) -> bool:
        if all([computer in c.connections for c in self.computers]):
            self.computers.append(computer)
            self.computers.sort(key=lambda c: c.name)
            return True
        return False

    def get_candidates(self) -> Set[Computer]:
        candidates = set()
        for member in self.computers:
            if not candidates:
                candidates |= member.connections
            else:
                candidates = candidates.intersection(member.connections)
        return candidates

    def __len__(self):
        return len(self.computers)

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return f'Cluster({",".join([c.name for c in self.computers])})'

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return str(self).__lt__(str(other))


@cache
def maximize_cluster(cluster: Cluster) -> Cluster:
    computers_to_add = cluster.get_candidates()
    if not computers_to_add:
        return cluster
    expanded_clusters = set()
    for computer in computers_to_add:
        expanded_cluster = cluster.copy()
        expanded_cluster.try_add(computer)
        expanded_cluster = maximize_cluster(expanded_cluster)
        expanded_clusters.add(expanded_cluster)
    expanded_clusters = list(expanded_clusters)
    expanded_clusters.sort(key=len)
    return expanded_clusters[-1]


def get_largest_cluster(computers: List[Computer]) -> Cluster:
    clusters = set()
    for c in computers:
        cluster = Cluster()
        cluster.try_add(c)
        clusters.add(maximize_cluster(cluster))
    clusters = list(clusters)
    clusters.sort(key=len)
    return clusters[-1]


if __name__ == '__main__':
    computers = {}
    with open('input.txt', 'r') as file:
        for line in file.read().splitlines():
            c1, c2 = line.split('-')
            c1 = computers.get(c1, Computer(c1))
            c2 = computers.get(c2, Computer(c2))
            c1.make_connection(c2)
            c2.make_connection(c1)
            computers[c1.name] = c1
            computers[c2.name] = c2
    print('part 1')
    cluster_with_t = set()
    for c in computers.values():
        if c.name.startswith('t'):
            cluster_with_t |= c.get_clusters()
    print(len(cluster_with_t))

    print('part 2')
    largest_cluster = get_largest_cluster([c for c in computers.values()])
    print(largest_cluster)
