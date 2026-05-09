from enum import Enum

class Skills(str, Enum):
    Fighting="Fighting"  # not a real skill.
    Mining="Mining"
    Woodcutting="Woodcutting"
    Fishing="Fishing"
    Weaponcrafting="Weaponcrafting"
    Gearcrafting="Gearcrafting"
    Jewelrycrafting="Jewelrycrafting"
    Cooking="Cooking"
    Alchemy="Alchemy"

    def __str__(str) -> str:
        return super().__str__()