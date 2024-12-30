from abc import ABC, abstractmethod
import boto3
import json
import numpy as np
from typing import List
from ..config import load_config

_config = load_config()

class BaseEmbeddingModel(ABC):
    @abstractmethod
    def encode(self, texts: List[str]) -> np.ndarray:
        pass

    @abstractmethod
    def encode_single(self, text: str) -> np.ndarray:
        pass

class BedrockEmbeddingModel(BaseEmbeddingModel):
    def __init__(self, model_name: str = None):
        self.model_name = model_name or _config["bedrock"]["embedding"]["model_id"]
        self.client = boto3.client(
            'bedrock-runtime',
            region_name=_config["bedrock"]["region"]
        )

    def encode_single(self, text: str) -> np.ndarray:
        try:
            response = self.client.invoke_model(
                modelId=self.model_name,
                body=json.dumps({"inputText": text})
            )
            response_body = json.loads(response.get('body').read())
            embedding = np.array(response_body.get('embedding'))

            if embedding.shape[0] != _config["bedrock"]["embedding"]["dimension"]:
                raise ValueError(
                    f"Unexpected embedding dimension: {embedding.shape[0]}, "
                    f"expected {_config['bedrock']['embedding']['dimension']}"
                )
            return embedding
        except Exception as e:
            raise Exception(f"Error encoding text with Bedrock: {str(e)}")

    def encode(self, texts: List[str]) -> np.ndarray:
        if not isinstance(texts, list):
            texts = [texts]

        embeddings = []
        batch_size = _config["bedrock"]["embedding"]["batch_size"]
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = [self.encode_single(text) for text in batch]
            embeddings.extend(batch_embeddings)

        return np.array(embeddings)

def get_embedding_model(model_name: str = None) -> BaseEmbeddingModel:
    model_name = model_name or _config["bedrock"]["embedding"]["model_id"]
    return BedrockEmbeddingModel(model_name)
