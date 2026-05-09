from enum import Enum

class Actions(str, Enum):
    Move='move'
    Fight='fight'
    Gather='gather'
    Unequip='unequip'
    Equip='equip'
    Craft='craft'

    def __str__(self) -> str:
        return super().__str__()
