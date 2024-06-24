from typing import List

from fastapi import HTTPException

from entities.api import ModelAdd, ModelVersionAdd, InferenceArguments
from entities.db import Model, ModelVersion
from injector import inject, Scope
from ml_utils.inferences import InferenceService
from persistence.model import ModelDao, ModelVersionDao


@inject(Scope.Singleton)
class ModelController:

    def __init__(self, model_dao: ModelDao):
        self.model_dao = model_dao

    def add_model(self, model_add: ModelAdd) -> Model:
        existing_model = self.model_dao.get_by_name(model_add.name)
        if existing_model is not None:
            raise HTTPException(
                status_code=400, detail=f"Duplicate name: {model_add.name}"
            )
        model = Model(id=None, name=model_add.name, owner=model_add.owner)
        return self.model_dao.add(model)

    def get_models(self) -> List[Model]:
        return list(self.model_dao.get_all())

    def delete(self, model_id: str) -> None:
        model = self.model_dao.get_by_id(model_id)
        if model is None:
            raise HTTPException(status_code=404, detail="Model not found")
        self.model_dao.delete(model_id)


@inject(Scope.Singleton)
class ModelVersionController:

    def __init__(
        self,
        model_dao: ModelDao,
        model_version_dao: ModelVersionDao,
        inference_service: InferenceService,
    ):
        self.model_dao = model_dao
        self.model_version_dao = model_version_dao
        self.inference_service = inference_service

    def get_versions(self, model_id: str) -> List[ModelVersion]:
        model = self.model_dao.get_by_id(model_id)
        if model is None:
            raise HTTPException(status_code=404, detail="Model not found")
        return list(self.model_version_dao.get_by_model_id(model_id))

    def add_model_version(
        self, model_id: str, model_version_add: ModelVersionAdd
    ) -> ModelVersion:
        model = self.model_dao.get_by_id(model_id)
        if model is None:
            raise HTTPException(status_code=404, detail="Model not found")
        existing_model_version = self.model_version_dao.get_by_model_id_and_name(
            model_id, model_version_add.name
        )
        if existing_model_version is not None:
            raise HTTPException(
                status_code=400, detail=f"Duplicate name: {model_version_add.name}"
            )
        model_version = ModelVersion(
            id=None,
            name=model_version_add.name,
            parent_model_id=model_id,
            hugging_face_model=model_version_add.hugging_face_model,
        )
        return self.model_version_dao.add(model_version)

    def delete(self, model_id: str, model_version_id: str) -> None:
        model_version = self.model_version_dao.get_by_id(model_version_id)
        if model_version is None:
            raise HTTPException(status_code=404, detail="Model version not found")
        self.model_version_dao.delete(model_version_id)

    def perform_inference(self, model_version_id: str, args: InferenceArguments) -> str:
        model_version = self.model_version_dao.get_by_id(model_version_id)
        if model_version is None:
            raise HTTPException(status_code=404, detail="Model version not found")
        text = args.text
        try:
            return self.inference_service.load_and_infer(
                model_version,
                text,
                apply_template=args.apply_template,
                max_new_tokens=args.max_new_tokens,
                do_sample=args.do_sample,
                temperature=args.temperature,
                top_k=args.top_k,
                top_p=args.top_p,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error during inference {e}")

