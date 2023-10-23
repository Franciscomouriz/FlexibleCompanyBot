import yaml
import os
import codecs
import json
import torch

from typing import List

from preprocesado.controlador_procesado import ProcesarDatasetControlador

# Función que lee un fichero yaml
def read_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.FullLoader,)
    
# Función que escribe los segmentos en el fichero de la base de conocimiento
def write_segments(path: str, data: List):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    with codecs.open(path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(data):
            f.write(json.dumps(segment, ensure_ascii=False)+"\n")
        f.close()

# Función que lee los segmentos del fichero de la base de conocimiento
def read_segments(path: str) -> List:
    if not os.path.exists(path):
        write_segments(path, [])

    with codecs.open(path, "r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f]
        f.close()
    return data

# Función que obtiene el path de los ficheros de la carpeta
def get_files_path(path: str) -> List:
    return [os.path.join(path, file) for file in os.listdir(path)]

# Función que recorre los ficheros del path y los preprocesa
def process_files(segments: List, files_path: List, temp_path: str, controlador: ProcesarDatasetControlador):
    for file_path in files_path:
        segments += controlador.procesar_dataset(file_path)
        
        # Se elimina el contenido del directorio temporal si la carpeta está vacía
        if len(os.listdir(temp_path)) == 0:
            os.system("rm -r " + temp_path + "*")

        # Se mueve el fichero a la carpeta de ficheros procesados
        os.system("mv " + file_path + " ./dataset/files/processed_files/")

# Función que crea el índice de los segmentos
def create_index(segments_path: str, index_path: str):
    os.system('python -m pyserini.index.lucene -collection JsonCollection \
    -generator DefaultLuceneDocumentGenerator \
    -threads 1 \
    -input ' + segments_path + ' \
    -index ' + index_path + ' \
    -storePositions -storeDocvectors -storeRaw -language spanish')


# Function to select the device to use (CPU or GPU)
def select_device():
    if torch.cuda.is_available(): 
        dev = "cuda:0"
    else: 
        dev = "cpu"
    return torch.device(dev)
