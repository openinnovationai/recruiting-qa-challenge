from typing import Iterator, Optional

from entities.db import Model, ModelVersion
from injector import inject, Scope
from persistence.common import InMemoryDao


@inject(Scope.Singleton)
class ModelDao(InMemoryDao[Model]):
    pass


@inject(Scope.Singleton)
class ModelVersionDao(InMemoryDao[ModelVersion]):

    def get_by_model_id(self, model_id: str) -> Iterator[ModelVersion]:
        for el in self.get_all():
            if el.parent_model_id == model_id:
                yield el

    def get_by_model_id_and_name(
        self, model_id: str, name: str
    ) -> Optional[ModelVersion]:
        for el in self.get_by_model_id(model_id):
            if el.name == name:
                return el
        return None

