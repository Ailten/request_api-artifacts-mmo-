from ..Characters import Characters
from ..primitives.Action import Actions
from ..primitives.V2 import V2

class Crafter(Characters):
    status: str

    def __init__(self, pseudo: str, pos_to_craft: V2=V2(2,1), recipies:list=[{
        'ingredients': [{
            'code': 'feather',
            'quantity': 6
        }],
        'item_to_craft': 'apprentice_gloves',
        'pos_to_craft': V2(2,1),
        'is_recycle': True
    }]):
        super().__init__(pseudo)
        self.pos_to_craft = pos_to_craft

        self.status = 'get_bank'

    
    # ---> 
        

    def getActionPackage(self) -> str|tuple[str,dict]:

        match self.status:

            case 'get_bank':
                
                if self.pos != V2(4,1):  # walk to bank.
                    return (str(Actions.Move), { 'pos': V2(4,1) })

                if self.inventoryQuantityFill != 0:  # drop all inventory in bank.
                    return (str(Actions.DropInBank), { 'item_to_drop': self.inventory })
                
                

            
            case 'crafting':
                return 'nothing'
            
            case 'recycle':
                return 'nothing'
            
            case 'set_bank':
                return 'nothing'
