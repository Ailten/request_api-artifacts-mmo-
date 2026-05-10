from enum import Enum

class MapsLayer(str, Enum):
    Interior='interior'
    Overworld='overworld'
    Underground='underground'

    def __str__(self) -> str:
        return super().__str__()