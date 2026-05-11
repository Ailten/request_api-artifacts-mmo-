from ..Characters import Characters
from ..primitives.Action import Actions
from ..primitives.V2 import V2

class WoodCuter(Characters):
    pos_to_cut: V2
    pos_to_craft: V2

    status: str
    
    item_cutting: str
    item_crafting: str
    craft_ingredient_quantity: int

    def __init__(self, pseudo: str, pos_to_cut: V2=V2(2,0), pos_to_craft: V2=V2(-2,-3)):
        super().__init__(pseudo)
        self.pos_to_cut = pos_to_cut
        self.pos_to_craft = pos_to_craft

        self.status = 'cutting'

        self.item_cutting = 'ash_wood'
        self.item_crafting = 'ash_plank'
        self.craft_ingredient_quantity = 10

    
    # ---> 
        

    def getActionPackage(self) -> str|tuple[str,dict]:

        match self.status:

            case 'cutting':  # cutting.

                if self.isInventoryFull():
                    self.status = 'crafting'
                    return self.getActionPackage()
                
                if self.pos == self.pos_to_cut:
                    return str(Actions.Gather)
                
                return (str(Actions.Move), { 'pos': self.pos_to_cut})
            
            case 'crafting':  # crafting.

                if self.pos != self.pos_to_craft:
                    return (str(Actions.Move), { 'pos': self.pos_to_craft})
                
                self.status = 'stocking'
                return (str(Actions.Craft, {
                    'item_to_craft': self.item_crafting,
                    'quantity': next([ i['quantity'] for i in self.inventory() if i['code'] == self.item_cutting ].__iter__(), 0) // self.craft_ingredient_quantity
                }))
            
            case 'stocking':  # bank.

                if self.pos != V2(4,1):
                    return (str(Actions.Move), { 'pos': V2(4,1) })
                
                self.status = 'cutting'
                return (str(Actions.DropInBank), {
                    'item_to_drop': [ i for i in self.inventory if (
                        i['type'] == 'ressource' and
                        (
                            i['code'] == self.item_crafting or
                            (  # drop also other ressource from minning.
                                i['subtype'] == 'woodcutting' and 
                                i['code'] != self.item_minning
                            )
                        )
                    ) ]
                })



    # ---> 



        