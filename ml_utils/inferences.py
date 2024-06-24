from typing import Any

import torch
import transformers
from transformers import AutoTokenizer

from entities.db import ModelVersion
from injector import inject, Scope


@inject(Scope.Singleton)
class InferenceService:

    def __init__(self):
        self.dtype = torch.float16

        self.cache = dict()

    def _create_pipeline(self, model: str) -> Any:
        tokenizer = AutoTokenizer.from_pretrained(model)
        pipeline = transformers.pipeline(
            "text-generation",
            model=model,
            torch_dtype=self.dtype,
        )
        return pipeline, tokenizer

    def _apply_template(self, tokenizer, msg: str) -> str:
        messages = [
            {
                "role": "system",
                "content": "You are a friendly chatbot who always responds with accurate information.",
            },
            {"role": "user", "content": msg},
        ]
        return tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

    def load_and_infer(
        self,
        model_version: ModelVersion,
        input_text: str,
        *,
        apply_template: bool = False,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95
    ) -> str:
        model = model_version.hugging_face_model
        pipeline_and_tokenizer = self.cache.get(model)
        if pipeline_and_tokenizer is None:
            self.cache[model] = self._create_pipeline(model)
            pipeline, tokenizer = self.cache[model]
        else:
            pipeline, tokenizer = pipeline_and_tokenizer
        if apply_template:
            prompt = self._apply_template(tokenizer, input_text)
        else:
            prompt = input_text
        sequences = pipeline(
            prompt,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
        )

        return sequences[0]["generated_text"]

