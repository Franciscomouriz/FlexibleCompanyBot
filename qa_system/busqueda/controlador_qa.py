from typing import Dict

from busqueda.busqueda import BusquedaInfo
from busqueda.respuesta import GenerarRespuesta
from busqueda.qa_info import QARespuesta
from busqueda.models import QAModels
from api_utils import select_device

class BusquedaRespuestaControlador:
    def __init__(self, config: Dict):
        self._busqueda = BusquedaInfo()
        self._generacion = GenerarRespuesta()
        self._config = config
        self._data = QARespuesta()
        self._models = QAModels()
        self._device = select_device()
        self._result = None
    
    def search_answer(self, query: str):

        self._data.question = query

        self._busqueda.search(self._data, self._config.get('data_path'))
        self._models.select_reranker('caskcsg/cotmae_base_msmarco_reranker')
        self._busqueda.rerank_data(self._data, self._models, self._config.get('segment_rerank'))
        self._models.delete_ranker()

        self._models.select_QAModel(self._device, 'google/flan-t5-large')
        self._generacion.generate_answer(self._data, self._models, self._device, self._config.get('generate_answer'))
        self._generacion.correct_answer(self._data, self._config.get('correct_answer'))
        self._models.delete_qa_model()
        self._models.delete_qa_tokenizer()

        self._result = self._data.answer_corrected

        # Se libera memoria
        self._data.delete()
        del(self._data)
        del(self._models)
        
        return self._result
