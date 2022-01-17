import typing
from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional

__all__ = ("Node", "Storage", "Iterator", "ShapeStorage")

from .shape import Shape
from .group import Group
from model.shapes import get_shapes_dict

T = TypeVar("T")


@dataclass(order=True)
class Node(Generic[T]):
    value: T = field(compare=False)
    priority: int = 0
    prev: Optional['Node'] = field(compare=False, default=None)
    next: Optional['Node'] = field(compare=False, default=None)


class Iterator:
    def __init__(self, storage: 'Storage', reverse: bool = False):
        self._storage = storage
        self._reverse = reverse
        if not self._reverse:
            self._storage.first()
        else:
            self._storage.last()

    def __iter__(self):
        return self

    def __next__(self):
        if self._storage.eol():
            raise StopIteration
        res = self._storage.get_current()
        if not self._reverse:
            self._storage.next()
        else:
            self._storage.prev()
        return res


class Storage(Generic[T]):
    def __init__(self):
        self._first: Optional[Node] = None
        self._last: Optional[Node] = None
        self._current: Optional[Node] = None
        self._size = 0

    def __iter__(self):
        return Iterator(self)

    def __reversed__(self):
        return Iterator(self, True)

    def first(self) -> None:
        self._current = self._first

    def last(self) -> None:
        self._current = self._last

    def eol(self) -> bool:
        return self._current is None

    def next(self) -> None:
        self._current = self._current.next

    def prev(self) -> None:
        self._current = self._current.prev

    def get_current(self) -> T:
        if self._current is None:
            raise ValueError("Trying to get current from empty list")
        return self._current.value

    def pop_current(self) -> T:
        if self._current is None:
            raise ValueError("Trying to pop current from empty list")

        self._size -= 1

        if self._current.prev:
            self._current.prev.next = self._current.next

        if self._current.next:
            self._current.next.prev = self._current.prev

        if self._current is self._first:
            self._first = self._current.next

        if self._current is self._last:
            self._last = self._current.prev

        v = self._current.value

        self._current = self._current.next

        return v

    def pop_back(self) -> T:
        if self._last is None:
            raise ValueError("Trying to pop back from empty list")

        self._size -= 1
        v = self._last.value
        p = self._last.prev
        if p:
            p.next = None

        self._last = p

        return v

    def pop_front(self) -> T:
        if self._first is None:
            raise ValueError("Trying to pop front from empty list")

        self._size -= 1
        v = self._first.value
        n = self._first.next
        if n:
            n.prev = None

        self._first = n

        return v

    def push(self, value: T, priority=0):
        self._size += 1
        node = Node(value, priority)
        if not self._first:
            self._current = self._first = self._last = node
            return

        if priority > self._first.priority:
            node.next = self._first
            self._first.prev = node
            self._first = node

        elif priority <= self._last.priority:
            self._last.next = node
            node.prev = self._last
            self._last = node

        else:
            curr = self._first
            while curr.priority <= priority and curr.next:
                curr = curr.next
            if curr.prev:
                curr.prev.next = node
                node.prev = curr.prev.next
            node.next = curr.prev
            curr.prev = node.next


class ShapeStorage(Storage[Shape]):
    def save(self, file: typing.IO):
        file.write(str(self._size) + "\n")
        self.first()
        while not self.eol():
            c = self.get_current()
            c.save(file)
            self.next()

    @classmethod
    def load(cls, file: typing.IO) -> "ShapeStorage":
        storage = cls()
        shapes = get_shapes_dict()

        try:
            n = int(file.readline().strip())
        except ValueError:
            return storage

        for i in range(n):
            name = file.readline().strip()
            if name == Group.name():
                s = Group.load(file)
            else:
                s = shapes[name].load(file)
            storage.push(s)

        return storage
