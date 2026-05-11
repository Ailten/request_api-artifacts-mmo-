from ..Characters import Characters
from ..primitives.Action import Actions
from ..primitives.V2 import V2

class Crafter(Characters):
    pos_to_craft: V2

    status: str

    is_recycle: bool

    def __init__(self, pseudo: str, pos_to_craft: V2=V2(2,1)):
        super().__init__(pseudo)
        self.pos_to_craft = pos_to_craft

        self.status = 'get_bank'

        is_recycle = True

    
    # ---> 
        

    def getActionPackage(self) -> str|tuple[str,dict]:

        match self.status:

            case 'get_bank':
                return 'nothing'
            
            case 'crafting':
                return 'nothing'
            
            case 'recycle':
                return 'nothing'
            
            case 'set_bank':
                return 'nothing'
