from typing import Dict

from preprocesado.segmentar_dataset import SegmentarDataset
from preprocesado.limpiar_dataset import LimpiarDataset
from preprocesado.cargar_dataset import CargarDataset

from preprocesado.dataset import QADataset

class ProcesarDatasetControlador:
    def __init__(self, config: Dict):
        self._cargar = CargarDataset()
        self._limpiar = LimpiarDataset()
        self._segmentar = SegmentarDataset()
        self._config = config
        self._data = None
        self._result = None
    
    def procesar_dataset(self, path: str):

        self._data = QADataset(path=path)
        self._cargar.load_data(self._data, self._config.get("data_path"))
        self._limpiar.clean_data(self._data)
        self._segmentar.segment_data(self._data, self._config.get("window"))

        self._result = self._data.data_segmented
        return self._result
