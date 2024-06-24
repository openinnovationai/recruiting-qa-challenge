from pydantic import BaseModel
from typing import Optional


class Identifiable(BaseModel):
    id: Optional[str]
    name: str


class Model(Identifiable):
    owner: str


class ModelVersion(Identifiable):
    parent_model_id: str
    hugging_face_model: str
