import os
import spacy
from tqdm import tqdm
from typing import Dict

from preprocesado.dataset import QADataset

class SegmentarDataset:

    # Función que obtiene el nombre de un fichero sin la extensión
    # path: Ruta del fichero
    def _get_file_name(self, path: str):
        return os.path.splitext(os.path.basename(path))[0]

    # Función que recorre el texto segmentándolo
    # document: Diccionario con el nombre del fichero como clave y el texto como valor
    # stride: Número de oraciones que se saltan al segmentar el texto
    # max_length: Número máximo de oraciones por segmento
    # nlp: Objeto spaCy
    def _window(self, document: Dict, document_name: str, stride: int, max_length: int, nlp: spacy.lang):
        
        segments = []

        for text in tqdm(document):
            # Obtiene el texto del documento
            data_text = document[text]
            # Crea un objeto spacy con el texto del documento
            doc = nlp(data_text)
            # Separa el texto en oraciones
            sentences = [sent.text.strip() for sent in doc.sents]

            for i in range (0, len(sentences), stride):
                # Une las max_length oraciones en una sola separadas por un espacio
                segment = " ".join(sentences[i:i+max_length])
                # Se crea un diccionario con el título del documento como clave y el texto segmentado como valor
                segments.append({"title": f"{document_name} > {text}", "contents": segment})

                # Si el segmento es el último, se sale del bucle
                if i + max_length >= len(sentences):
                    break

        # Add an id to each segment
        for i, doc in enumerate(segments):
            doc['id'] = i

        return segments
    

    # Función que realiza la segmentación de los datos y los almacena en un fichero .jsonl
    def segment_data(self, dataset: QADataset, config_window: Dict):
        # Se comprueba que el json a segmentar existe
        if dataset.data_clean is None:
            raise ValueError("El dataset no ha sido limpiado")
        # El dataset está en español, por lo que se crea un objeto spacy en español
        nlp = spacy.blank("es")
        # Se añade el componente sentencizer para segmentar el texto en oraciones
        nlp.add_pipe('sentencizer')

        document_name = self._get_file_name(dataset.path)
        segments = self._window(dataset.data_clean, document_name, config_window.get("stride"), config_window.get("max_length"), nlp)
        dataset.data_segmented = segments