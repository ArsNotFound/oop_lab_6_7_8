import typing
from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional

__all__ = ("Storage", "ShapeStorage")

from PySide6.QtCore import QObject, Signal, Slot

from .shape import Shape
from .group import Group
from .shapes import get_shapes_dict

T = TypeVar("T")


class Storage(Generic[T]):
    @dataclass(order=True)
    class Node(Generic[T]):
        value: T = field(compare=False)
        priority: int = 0
        prev: Optional["Storage.Node"] = field(compare=False, default=None)
        next: Optional["Storage.Node"] = field(compare=False, default=None)

    class Iterator(Generic[T]):
        def __init__(self, storage: "Storage[T]", reverse: bool = False):
            self._storage = storage
            self._reverse = reverse
            if not self._reverse:
                self._curr = self._storage._first
            else:
                self._curr = self._storage._last

        def __iter__(self) -> "Storage.Iterator[T]":
            return self

        def __next__(self) -> T:
            if not self._curr:
                raise StopIteration
            res = self._curr.value
            if not self._reverse:
                self._curr = self._curr.next
            else:
                self._curr = self._curr.prev
            return res

    def __init__(self):
        self._first: Optional[Storage.Node] = None
        self._last: Optional[Storage.Node] = None
        self._current: Optional[Storage.Node] = None
        self._size = 0

    @property
    def size(self) -> int:
        return self._size

    def __iter__(self):
        return Storage.Iterator(self)

    def __reversed__(self):
        return Storage.Iterator(self, True)

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

    def clear(self) -> None:
        self._current = self._first = self._last = None
        self._size = 0

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
        node = Storage.Node(value, priority)
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


class ShapeStorage(QObject, Storage[Shape]):
    storage_changed = Signal()

    def __init__(self, parent: Optional[QObject] = None):
        QObject.__init__(self, parent)
        Storage.__init__(self)

    @Slot(object)
    def on_changed(self, item: Shape):
        self.storage_changed.emit()

    def push(self, value: Shape, priority=0):
        value.changed.connect(self.on_changed)
        super().push(value, priority)
        self.storage_changed.emit()

    def pop_back(self) -> Shape:
        s = super().pop_back()
        s.changed.disconnect(self.on_changed)
        self.storage_changed.emit()
        return s

    def pop_front(self) -> Shape:
        s = super().pop_front()
        s.changed.disconnect(self.on_changed)
        self.storage_changed.emit()
        return s

    def pop_current(self) -> Shape:
        s = super().pop_current()
        s.changed.disconnect(self.on_changed)
        self.storage_changed.emit()
        return s

    def save(self, file: typing.IO):
        file.write(str(self._size) + "\n")
        self.first()
        while not self.eol():
            c = self.get_current()
            c.save(file)
            self.next()

    def load(self, file: typing.IO):
        self.clear()
        shapes = get_shapes_dict()

        try:
            n = int(file.readline().strip())
        except ValueError:
            return

        for i in range(n):
            name = file.readline().strip()
            if name == Group.name():
                s = Group.load(file)
            else:
                s = shapes[name].load(file)
            self.push(s)
