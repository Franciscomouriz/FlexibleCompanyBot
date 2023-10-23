import os


from preprocesado.dataset import QADataset
from docx import Document
from typing import Dict

class CargarDataset:

    def _load(self, dataset: QADataset, content: str, extension: str):
        dataset.data = content
        dataset.extension = extension
    
    def _load_xml(self, dataset: QADataset):
        content = []
        with open(dataset.path, "r", encoding="utf8") as f:
            content = f.readlines()
        content = "".join(content)
        self._load(dataset, content, "xml")

    def _load_txt(self, dataset: QADataset):
        data = {}
        file = dataset.path.split("/")[-1]
        with open(dataset.path, "r", encoding="utf8") as f:
            data[file] = f.read()
        self._load(dataset, data, "txt")

    def _load_pdf(self, dataset: QADataset, temp_path: str):
        # Se separan path, nombre y extensión del fichero
        path = dataset.path.split("/")[:-1]
        path = os.path.join(*path) + "/"
        path = path[2:]

        file = dataset.path.split("/")[-1]
        file_name = file.split(".")[0]

        # Se ejecuta grobid para convertir el pdf a xml
        os.system("java -Xmx4G -jar ../grobid-0.7.2/grobid-core/build/libs/grobid-core-0.7.2-onejar.jar -gH ../grobid-0.7.2/grobid-home -dIn " + path + " -dOut " + temp_path + "/ -r -exe processFullText")
        
        # Se cambia el path del dataset para que apunte al xml
        dataset.path = temp_path + file_name + ".tei.xml"

        # Se carga el xml
        self._load_xml(dataset)

    def _load_docx(self, dataset: QADataset):
        doc = Document(dataset.path)
        self._load(dataset, doc, "docx")


    # Función que carga los ficheros de un directorio
    # Devuelve un diccionario con el nombre del fichero como clave y el texto como valor
    # dataset: objeto QADataset que contiene el path del dataset y donde se almacenará la información
    def load_data(self, dataset: QADataset, config_path: Dict):
        #dataset.path finaliza con un fichero
        if dataset.path.endswith(".txt"):
            self._load_txt(dataset)
        elif dataset.path.endswith(".pdf"):
            self._load_pdf(dataset, config_path.get("temp_files"))
        elif dataset.path.endswith(".xml"):
            self._load_xml(dataset)
        elif dataset.path.endswith(".doc") or dataset.path.endswith(".docx"):
            self._load_docx(dataset)