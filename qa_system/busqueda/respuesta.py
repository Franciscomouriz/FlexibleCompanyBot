from typing import Dict
import language_tool_python

from busqueda.models import QAModels
from busqueda.qa_info import QARespuesta

class GenerarRespuesta():

    # Función que genera texto a partir de un texto de entrada
    def _generate(self, input_text, model, tokenizer, device):
        # Se convierte el texto en una lista de tokens
        # input_ids.to(device) envía el tensor obtenido de tokenizer a la GPU
        input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(device)
        # Se genera la respuesta de longitud máxima max_length
        gen_tokens = model.generate(
            input_ids,
            do_sample=False,
            max_length=128)
        # Se decodifica la respuesta
        output_text = tokenizer.decode(gen_tokens[0], skip_special_tokens=True)
        return output_text


    # Función que genera una respuesta a partir de de los segmentos rerankeados
    def generate_answer(self, data: QARespuesta, model: QAModels, device, config_qa: Dict):
        prompt= config_qa.get("prompt")
        # Se genera el prompt con los segmentos rerankeados en top_texts y la pregunta
        for i,doc in enumerate(data.ranked_texts):
            prompt+="Documento {0}: Título: {1}. Contenido: {2}\n".format(i+1,doc['title'],doc['text'])

        # Los modelos T5 requieren que se indique con una instrucción al principio del prompt el tipo de tarea que se va a realizar
        # Question: indica que se le va a pasar una pregunta
        # Explanation: como no se le pasa nada a continuación, indica que debe generar una explicación
        prompt += "Pregunta: {0}\n".format(data.question)

        # Se genera la respuesta a partir del prompt con la pregunta y la explicación
        answer = self._generate(prompt+"\nRespuesta:", model.qa_model, model.qa_tokenizer, device)
        data.answer = answer


    # Función que corrige gramaticalmente la respuesta generada
    def correct_answer(self, data: QARespuesta, config_corrector: Dict):
        
        # Se selecciona el corrector a utilizar
        tool = language_tool_python.LanguageTool(config_corrector.get("language"))

        # Lista de caracteres a corregir
        caracteres = ["ñ", "á", "é", "í", "ó", "ú", "Á", "É", "Í", "Ó", "Ú"]

        # Se divide la respuesta en palabras
        words = data.answer.split(" ")

        # Se crea la variable donde se almacenará la respuesta corregida
        corrected_text = ""

        # Se recorren las palabras
        for word in words:
            # Se revisa que no sea una palabra vacía
            if word != "":
                # Se revisa que la palabra sea correcta
                matches = tool.check(word)
                if len(matches) != 0:
                    aux = 0
                    # Se revisan las 3 primeras sugerencias
                    for suggestion in matches[0].replacements[0:3]:
                        # Se revisa si la sugerencia contiene uno de los caracteres a corregir
                        for caracter in caracteres:
                            # Si la sugerencia contiene el caracter, se reemplaza
                            if caracter in suggestion and aux == 0:
                                corrected_word = suggestion.replace(caracter, caracter)
                                corrected_text += corrected_word + " "
                                aux = 1
                                break
                    if aux == 0:
                        corrected_text += word + " "
                # La palabra es correcta, se agrega a la respuesta
                else:
                    corrected_text += word + " "
        
        # Se guarda la respuesta corregida
        data.answer_corrected = corrected_text