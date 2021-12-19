import dataclasses
from typing import TypeVar, Generic, Optional

__all__ = ("Node", "Storage")

T = TypeVar("T")


@dataclasses.dataclass
class Node(Generic[T]):
    value: T
    prev: Optional['Node'] = None
    next: Optional['Node'] = None


class Storage(Generic[T]):
    def __init__(self):
        self._first: Optional[Node] = None
        self._last: Optional[Node] = None
        self._current: Optional[Node] = None
        self._size = 0

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

        v = self._last.value
        p = self._last.prev
        if p:
            p.next = None

        self._last = p

        return v

    def pop_front(self) -> T:
        if self._first is None:
            raise ValueError("Trying to pop front from empty list")

        v = self._first.value
        n = self._first.next
        if n:
            n.prev = None

        self._first = n

        return v

    def push_back(self, value: T) -> None:
        node = Node(value)
        if self._last:
            self._last.next = node
            node.prev = self._last
            self._current = self._last = node
        else:
            self._current = self._last = self._first = node

    def push_front(self, value: T) -> None:
        node = Node(value)
        if self._first:
            self._first.prev = node
            node.next = self._first
            self._current = self._first = node
        else:
            self._current = self._last = self._first = node

    def push_after(self, value: T) -> None:
        if not self._current:
            self.push_back(value)
            return

        node = Node(value)

        node.next = self._current.next
        node.prev = self._current

        if self._current.next:
            self._current.next.prev = node

        self._current.next = node

        self._current = node

    def push_before(self, value: T) -> None:
        if not self._current:
            self.push_front(value)

        node = Node(value)

        node.next = self._current
        node.prev = self._current.prev

        if self._current.prev:
            self._current.prev.next = node

        self._current.prev = node

        self._current = node
