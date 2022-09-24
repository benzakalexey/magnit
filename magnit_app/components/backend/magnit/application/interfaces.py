from abc import ABC, abstractmethod
from typing import Optional, List



class DefaultRepo(ABC):

    @abstractmethod
    def get(self, id_: int):
        ...
