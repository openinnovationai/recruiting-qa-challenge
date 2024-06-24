import uuid
from typing import TypeVar, Generic, Dict, Iterator, Optional

from entities.db import Identifiable

T = TypeVar("T", bound=Identifiable)


class InMemoryDao(Generic[T]):

    def __init__(self):
        self.store: Dict[str, T] = dict()

    def add(self, item: T) -> T:
        item.id = str(uuid.uuid4())
        self.store[item.id] = item
        return item

    def delete(self, item_id: str) -> None:
        del self.store[item_id]

    def get_by_id(self, item_id: str) -> Optional[T]:
        return self.store.get(item_id)

    def get_by_name(self, name: str) -> Optional[T]:
        for el in self.get_all():
            if el.name == name:
                return el
        return None

    def get_all(self) -> Iterator[T]:
        for el in self.store.values():
            yield el
