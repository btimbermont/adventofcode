from typing import List


class Node:
    def __init__(self, name: str, type: str, size: int = 0, parent: 'Node' = None):
        self.name = name
        self._size = size
        self._type = type
        self.children: List[Node] = [] if type == 'dir' else None
        self.parent = parent

    def is_dir(self):
        return self._type == 'dir'

    def add_children(self, *children: 'Node'):
        if not self.is_dir():
            raise Exception(f'Cannot add children to other type then dir! type: {self._type}')
        for child in children:
            self.children.append(child)
        self.children.sort(key=lambda node: node.name)

    def get_child(self, name) -> 'Node':
        if not self.is_dir():
            raise Exception(f'Cannot get children from other type then dir! type: {self._type}')
        found_items = [child for child in self.children if child.name == name]
        if len(found_items) != 1:
            raise Exception(f'found mutiple children with given name {name}: {found_items}')
        return found_items[0]

    def size(self):
        if self.is_dir():
            size = 0
            for _child in self.children:
                size += _child.size()
            return size
        return self._size

    def __repr__(self) -> str:
        return f'[Node({self.name}) {self._type}]'

    def __str__(self):
        return f'{self.name} ({self._type}{f", size={self._size}" if self._size else ""})'


def dir_node(name: str, parent: Node) -> Node:
    return Node(name, 'dir', parent=parent)


def file_node(name: str, size: int, parent: Node) -> Node:
    return Node(name, 'file', size, parent=parent)


def parse_ls_line(line: str, parent: Node) -> Node:
    pt1, pt2 = line.split(' ', 2)
    if pt1 == 'dir':
        return dir_node(pt2, parent)
    else:
        return file_node(pt2, int(pt1), parent)


if __name__ == '__main__':
    print('PART 1')
    root = Node('/', type='dir', parent=None)
    root.parent = root
    all_nodes = [root]
    with open('input.txt', 'r') as file:
        for line in file.read().splitlines():
            if line.startswith('$'):
                # parse a command
                command = line.split(' ')[1:]  # remove '$'
                if command[0] == 'cd':
                    # change current node
                    if command[1] == '/':
                        current_node = root
                    elif command[1] == '..':
                        current_node = current_node.parent
                    else:
                        current_node = current_node.get_child(command[1])
                    continue
                if command[0] == 'ls':
                    # parsing the output is always from ls, so we can jsut continue this loop
                    continue
            else:
                node = parse_ls_line(line, current_node)
                current_node.add_children(node)
                all_nodes.append(node)
    print('done parsing!')
    print('getting al directories')
    all_dirs = [node for node in all_nodes if node.is_dir()]
    max_size = 100000
    print(f'Size of folders under max size: {sum([dir.size() for dir in all_dirs if dir.size() <= max_size])}')

    print('PART 2')
    total_space, space_required = 70000000, 30000000
    current_free_space = total_space - root.size()
    free_up_required = space_required - current_free_space
    print(f'current free space = {current_free_space}, cleanup require for {free_up_required}')
    folders_big_enough = [dir for dir in all_dirs if dir.size() >= free_up_required]
    folders_big_enough.sort(key=Node.size)
    print(f'Size of smallest folder that solves our problem: {folders_big_enough[0].size()}')
