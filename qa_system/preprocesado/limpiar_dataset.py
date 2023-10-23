import re
from bs4 import BeautifulSoup

from preprocesado.dataset import QADataset

class LimpiarDataset:

    def _clean_txt(self, dataset: QADataset):
        dataset.data_clean = dataset.data.copy()
        # Recorro el diccionario por el título del fichero
        for text in dataset.data_clean:
            soup = BeautifulSoup(dataset.data_clean[text], "html.parser")
            soup_text = soup.get_text()

            # Cambio los saltos de línea por espacios
            soup_text = soup_text.replace("\n", " ")
            # Elimino los espacios en blanco sobrantes
            soup_text = re.sub(" +", " ", soup_text)

            # Sustituyo text por el texto limpio
            dataset.data_clean[text] = soup_text

    def _clean_xml(self, dataset: QADataset):
        # Extrae las etiquetas <div>
        bs_content = BeautifulSoup(dataset.data, "xml")
        divs = bs_content.find_all("div")
        data = {}
        # Recorre las etiquetas <div>
        for div in divs:
            # Extrae <head>
            head = div.find("head")
            # Extrae <p>
            p = div.find_all("p")
            p = " ".join([str(par) for par in p])

            # Se añade el título del documento como clave y el texto como valor
            soup_head = BeautifulSoup(str(head), "lxml")
            soup_p = BeautifulSoup(str(p), "lxml")
            if p:
                data[soup_head.text] = soup_p.text
        dataset.data_clean = data

    def _clean_docx(self, dataset: QADataset):
        doc = dataset.data
        data = {}
        current_section = None
        current_text = ''

        # Se recorre el documento por párrafos
        for para in doc.paragraphs:
            # Consideramos un título si su estilo comienza con 'Heading'
            if para.style.name.startswith('Heading'):
                # Si ya había una sección, se guarda
                if current_section:
                    data[current_section] = current_text.strip()
                current_section = para.text
                current_text = ''
            else:
                current_text += ' ' + para.text
        
        # Aseguramos que se guarde la última sección
        if current_section:
            data[current_section] = current_text.strip()
        
        dataset.data_clean = data

        

    # Función que limpia los datos
    # dataset: objeto QADataset donde se almacena la información limpia
    def clean_data(self, dataset: QADataset):
        if dataset.extension == "txt":
            self._clean_txt(dataset)
        elif dataset.extension == "xml":
            self._clean_xml(dataset)
        elif dataset.extension == "docx":
            self._clean_docx(dataset)