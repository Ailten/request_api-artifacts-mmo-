from abc import ABC

class Characters(ABC):
    __pseudo: str
    __skills: list[str]
    __is_error: bool

    def __init__(self, pseudo: str):
        self.__pseudo = pseudo
        self.__skills = []
        self.__is_error = False

    @property
    def pseudo(self) -> str:
        return self.__pseudo
    
    @property
    def is_error(self) -> bool:
        return self.__is_error