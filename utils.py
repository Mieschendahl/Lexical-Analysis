from dataclasses import dataclass
from typing import Optional, Callable


@dataclass
class Tree:
    value: Optional[int] = None
    left: Optional["Tree"] = None
    right: Optional["Tree"] = None

    def get_value(self, value: int) -> int:
        if self.value is None:
            self.value = value
        return self.value

    def get_left(self) -> "Tree":
        if self.left is None:
            self.left = Tree()
        return self.left

    def get_right(self) -> "Tree":
        if self.right is None:
            self.right = Tree()
        return self.right

    @staticmethod
    def index_state(tree: "Tree", states: list[bool], store: int) -> int:
        index = 0
        while index < len(states):
            if states[index]:
                tree = tree.get_right()
            else:
                tree = tree.get_left()
            index += 1
        return tree.get_value(store)


def make_lookup(al: str) -> Callable[[str], int]:
    table = [-1] * (max(map(ord, al), default=0) + 1)
    for i, a in enumerate(al):
        table[ord(a)] = i

    def lookup(a: str) -> int:
        if ord(a) >= len(table):
            raise Exception(f"Unexpected character: '{a}' (not in alphabet)")
        res = table[ord(a)]
        if res == -1:
            raise Exception(f"Unexpected character: '{a}' (not in alphabet)")
        return res

    return lookup
