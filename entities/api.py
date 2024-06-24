from pydantic import BaseModel


class ModelAdd(BaseModel):
    name: str
    owner: str


class ModelVersionAdd(BaseModel):
    name: str
    hugging_face_model: str


class InferenceArguments(BaseModel):
    text: str
    apply_template: bool = False
    max_new_tokens: int = 256
    do_sample: bool = True
    temperature: float = 0.7
    top_k: int = 50
    top_p: float = 0.95
