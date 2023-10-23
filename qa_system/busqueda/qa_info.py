from dataclasses import dataclass
from typing import List


@dataclass()
class QARespuesta:
    question: str = None
    answer: str = None
    answer_corrected: str = None
    texts: List = None
    ranked_texts: List = None

    # Función que vacía la memoria de los atributos de la clase
    def delete(self):
        self.question = None
        self.answer = None
        self.answer_corrected = None
        self.texts = None
        self.ranked_texts = None
