from dataclasses import dataclass
from typing import List
import torch

from pygaggle.rerank.transformer import SentenceTransformersReranker
from transformers import T5Tokenizer, T5ForConditionalGeneration

@dataclass()
class QAModels:
    ranker = None
    qa_tokenizer = None
    qa_model = None

    # Función que selecciona el modelo a utilizar para el reranking
    def select_reranker(self, ranker_name: str):
        reranker = SentenceTransformersReranker(ranker_name)
        self.ranker = reranker

    # Función que selecciona el modelo a utilizar para la generación de respuestas
    def select_QAModel(self, device, qa_name: str):
        self.qa_tokenizer = T5Tokenizer.from_pretrained(qa_name)
        self.qa_model = T5ForConditionalGeneration.from_pretrained(qa_name)

        self.qa_model = self.qa_model.to(device)

    def delete_ranker(self):
        del self.ranker
        torch.cuda.empty_cache()

    def delete_qa_tokenizer(self):
        del self.qa_tokenizer
        torch.cuda.empty_cache()

    def delete_qa_model(self):
        del self.qa_model
        torch.cuda.empty_cache()