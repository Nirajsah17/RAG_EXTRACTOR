from utils.logger import get_logger
from typing import List, Union
from ollama import Client


logger = get_logger(__name__)

class Embedder:
    def __init__(self, model: str = "bge-m3"):
        self.client = Client()
        self.model = model

    def embed(self, texts: Union[str, List[str]]):
        logger.info(f"Embedding texts using model: {self.model}")
        response = self.client.embed(
            model=self.model,
            input=texts
        )
        logger.info(f"Received embeddings length: {len(response['embeddings'])} for input texts")
        return response["embeddings"]