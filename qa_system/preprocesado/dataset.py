from dataclasses import dataclass, field
from bs4 import BeautifulSoup
from typing import List


@dataclass()
class QADataset:
    path: str = field(init=True)
    name: str = None
    extension: str = None
    data: BeautifulSoup = None
    data_clean: str = None
    data_segmented: List = None
