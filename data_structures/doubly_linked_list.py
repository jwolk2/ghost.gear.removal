from __future__ import annotations
from typing import Optional, Generic, TypeVar, Iterator

T = TypeVar("T")


class Node(Generic[T]):
    def __init__(self, data: T) -> None:
        self.data: T = data
        self.prev: Optional[Node[T]] = None
        self.next: Optional[Node[T]] = None

    def __repr__(self) -> str:
        return f"Node({self.data})"


class DoublyLinkedList(Generic[T]):
    def __init__(self) -> None:
        self.head: Optional[Node[T]] = None
        self.tail: Optional[Node[T]] = None
        self._size: int = 0

    def append(self, data: T) -> Node[T]:
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            assert self.tail is not None
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self._size += 1
        return new_node

    def remove(self, node: Node[T]) -> None:
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        node.prev = node.next = None
        self._size -= 1

    def __iter__(self) -> Iterator[T]:
        current = self.head
        while current:
            yield current.data
            current = current.next
