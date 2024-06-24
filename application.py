from typing import List

from fastapi import FastAPI

from controllers.model import ModelController, ModelVersionController
from entities.api import ModelAdd, ModelVersionAdd, InferenceArguments
from entities.db import Model, ModelVersion

app = FastAPI()

model_controller = ModelController.get_instance()
model_version_controller = ModelVersionController.get_instance()


@app.get("/models")
def get_models() -> List[Model]:
    return model_controller.get_models()


@app.post("/models")
def add_model(model: ModelAdd) -> Model:
    return model_controller.add_model(model)


@app.delete("/models/{model_id}")
def delete_model(model_id: str) -> None:
    model_controller.delete(model_id)


@app.get("/models/{model_id}/versions")
def get_model_versions(model_id: str) -> List[ModelVersion]:
    return model_version_controller.get_versions(model_id)


@app.post("/models/{model_id}/versions")
def add_model_versions(model_id: str, version: ModelVersionAdd) -> ModelVersion:
    return model_version_controller.add_model_version(model_id, version)


@app.delete("/models/{model_id}/versions/{version_id}")
def delete_model_version(model_id: str, version_id: str) -> None:
    model_version_controller.delete(model_id, version_id)


@app.post("/models/{model_id}/versions/{version_id}/infer")
def perform_inference(model_id: str, version_id: str, args: InferenceArguments) -> str:
    return model_version_controller.perform_inference(version_id, args)
