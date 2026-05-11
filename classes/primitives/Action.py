from enum import Enum

class Actions(str, Enum):
    Move='move'
    Fight='fight'
    Rest='rest'
    Gather='gather'
    Unequip='unequip'
    Equip='equip'
    Craft='craft'
    DropInBank='DropInBank'

    def __str__(self) -> str:
        return super().__str__()