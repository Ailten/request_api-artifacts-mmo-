from abc import ABC
from ..characters.Characters import Characters

class Skills(ABC):

    def __init__(self):
        pass

    def getAction(self, character: 'Characters') -> str|tuple[str,dict]|None:
        return None
    

    
    # Fighting="Fighting"  # not a real skill.
    # Mining="Mining"
    # Woodcutting="Woodcutting"
    # Fishing="Fishing"
    # Weaponcrafting="Weaponcrafting"
    # Gearcrafting="Gearcrafting"
    # Jewelrycrafting="Jewelrycrafting"
    # Cooking="Cooking"
    # Alchemy="Alchemy"