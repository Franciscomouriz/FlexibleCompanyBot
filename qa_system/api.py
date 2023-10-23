from fastapi.middleware.cors import CORSMiddleware

import os
import gc
from fastapi import FastAPI, Request

from api_utils import read_yaml, write_segments, read_segments, process_files, create_index, get_files_path
from preprocesado.controlador_procesado import ProcesarDatasetControlador
from busqueda.controlador_qa import BusquedaRespuestaControlador


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/process-data/")
async def process_data():
    #Cargo el fichero de configuración y obtengo los path de los ficheros
    config = read_yaml("./config/config.yml")
    config_path = config.get("data_path")
    imput_path = config_path.get("new_files_path")
    segments_file = config_path.get("segments_file")

    # Creo el controlador
    controlador = ProcesarDatasetControlador(config)

    # Obtengo los path de los ficheros de la carpeta
    files_path = get_files_path(imput_path)

    # Obtengo los segmentos ya procesados
    segments = read_segments(segments_file)

    # Proceso cada fichero y obtengo los segmentos
    process_files(segments, files_path, config_path.get("temp_files"), controlador)

    # Escribo los segmentos en un fichero json
    write_segments(segments_file, segments)

    # Creo el índice de los segmentos
    create_index(config_path.get("segments_path"), config_path.get("index_path"))
    
    return {"message": "Los datos se han procesado correctamente"}

@app.post("/search")
async def search(query: Request):
    # Obtengo la pregunta
    query_data = await query.json()

    #Cargo el fichero de configuración
    config = read_yaml("./config/config.yml")

    # Creo el controlador
    controlador = BusquedaRespuestaControlador(config)

    # Obtengo la respuesta
    answer = controlador.search_answer(query_data['query'])

    #Vaciar memoria de la RAM
    gc.collect()

    return {"answer": answer}
