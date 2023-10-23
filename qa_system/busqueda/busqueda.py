import json
import numpy as np
from typing import List, Dict

from pyserini.search.lucene import LuceneSearcher
from pygaggle.rerank.base import Query, Text

from busqueda.qa_info import QARespuesta
from busqueda.models import QAModels

class BusquedaInfo():
    
    # Función que obtiene los segmentos más relevantes para la pregunta
    def search(self, data: QARespuesta, config_path: str):
        searcher = LuceneSearcher(config_path.get('index_path'))
        hits = searcher.search(data.question, k=100)
        data.texts = hits
        del searcher 


    # Función que reordena los segmentos más relevantes para la pregunta
    def _rerank(self, model, query: str, texts: List[str]) -> List[str]:
        query = Query(query)
        # Se crea un objeto Text para cada segmento con el id, título, el contenido y el segmento
        texts = [Text(p['contents'], {'docid': p['id'], "title":p['title'], "text":p['contents']}, 0) for p in texts]
        # Se reordena los segmentos por relevancia
        reranked = model.rerank(query, texts)
        reranked.sort(key=lambda x: x.score, reverse=True)
        # Se devuelve una lista con los segmentos y sus scores
        return [(text.metadata,np.exp(text.score)) for text in reranked]


    # Función que rankea y devuelve los max_docs más relevantes
    def rerank_data(self, data: QARespuesta, model: QAModels, config_search: Dict):
        texts = [json.loads(hit.raw) for hit in data.texts]
        texts_scores = self._rerank(model= model.ranker, query=data.question, texts=texts)
        top_docs = []
        for i, (text, score) in enumerate(texts_scores[:config_search.get('max_docs')]):
            top_docs.append(text)
        data.ranked_texts = top_docs