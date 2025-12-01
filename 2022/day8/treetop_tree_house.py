from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Tree:
    x: int
    y: int
    height: int


class Forrest:
    def __init__(self, trees: [[Tree]]):
        # rows
        self._tree_rows = trees.copy()
        # store columns
        self._tree_columns = []
        for i in range(len(self._tree_rows)):
            self._tree_columns.append([row[i] for row in self._tree_rows])
        # all trees
        self._trees = []
        for row in self._tree_rows:
            for tree in row:
                self._trees.append(tree)

    def __str__(self) -> str:
        return '\n'.join([','.join([str(t.height) for t in row]) for row in self._tree_rows])

    def __repr__(self) -> str:
        return '\n'.join([tree.__str__() for tree in self._tree_rows])

    def get_outlook(self, tree: Tree) -> Tuple[List[Tree], List[Tree], List[Tree], List[Tree]]:
        left = self._tree_rows[tree.y][:tree.x][::-1]
        right = self._tree_rows[tree.y][tree.x + 1:]
        top = self._tree_columns[tree.x][:tree.y][::-1]
        bottom = self._tree_columns[tree.x][tree.y + 1:]

        return left, right, top, bottom

    def is_visible(self, tree: Tree):
        for direction in self.get_outlook(tree):
            if len(direction) == 0 or tree.height > max([tree.height for tree in direction]):
                return True
        return False

    def visible_trees(self) -> [Tree]:
        return [tree for tree in self._trees if self.is_visible(tree)]

    def get_scenic_score(self, tree: Tree) -> int:
        score = 1
        for direction in self.get_outlook(tree):
            if len(direction) == 0:  # optimization
                return 0
            subscore = 0
            for visible_tree in direction:
                subscore += 1
                if visible_tree.height >= tree.height:
                    break
            score *= subscore
        return score

    def get_max_scenic_score(self) -> int:
        return max([self.get_scenic_score(t) for t in self._trees])


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        trees = []
        row = 0
        for line in file.read().splitlines():
            treeline = []
            column = 0
            for height in line:
                treeline.append(Tree(column, row, int(height)))
                column += 1
            trees.append(treeline)
            row += 1
    forrest = Forrest(trees)
    print('PART 1')
    print(len(forrest.visible_trees()))
    print('PART 2')
    print(forrest.get_max_scenic_score())
