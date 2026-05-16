from ..Characters import Characters
from ..primitives.Action import Actions
from ..primitives.V2 import V2
import copy

class Crafter(Characters):
    status: str
    recipie: dict|list[dict]
    quantity_to_craft_now: int

    def __init__(self, pseudo: str, pos_to_craft: V2=V2(2,1), recipie:dict={
        'ingredients': [{
            'code': 'feather',
            'quantity': 6
        }],
        'item_to_craft': 'apprentice_gloves',
        'pos_to_craft': V2(2,1),
        'is_recycle': True
    }):
        super().__init__(pseudo)
        self.pos_to_craft = pos_to_craft
        self.quantity_to_craft_now = 0
        self.recipie = recipie

        self.status = 'set_bank'

    
    # ---> 
        

    def getActionPackage(self) -> str|tuple[str,dict]:

        match self.status:

            case 'get_bank':
                
                if self.pos != V2(4,1):  # walk to bank.
                    return (str(Actions.Move), { 'pos': V2(4,1) })

                # get items from bank (to make a clean craft quantity).
                bank_inventory = self.bankInventory
                item_to_get = []
                while True:  
                    item_to_get_current = []
                    is_current_valid = True
                    for ingredient in self.recipie['ingredients']:  # loop on every ingredients need to craft.
                        ingredient_get = next([ e for e in bank_inventory if (
                            e['code'] == ingredient['code'] and
                            e['quantity'] >= ingredient['quantity']
                        ) ].__iter__(), None)
                        if ingredient_get == None:  # no ingredient found (or not enougth).
                            is_current_valid = False
                            break
                        ingredient_take = copy.copy(ingredient_get)  # assigne quantity.
                        ingredient_take['quantity'] = ingredient['quantity']
                        ingredient_get['quantity'] -= ingredient['quantity']
                        item_to_get_current.append(ingredient_take)  # push in cash.
                    if not is_current_valid:
                        break
                    if (  # verify max capacity inventory.
                        sum([ e['quantity'] for e in item_to_get ]) +
                        sum([ e['quantity'] for e in item_to_get_current ])
                        > 100
                    ):
                        break
                    if len(item_to_get) == 0:
                        item_to_get = item_to_get_current
                        self.quantity_to_craft_now = 1
                    else:
                        for itgc in item_to_get_current:
                            item_match = next([ e for e in item_to_get if e['code'] == itgc['code'] ].__iter__(), None)
                            item_match['quantity'] += itgc['quantity']
                        self.quantity_to_craft_now += 1

                if self.quantity_to_craft_now == 0:
                    self.setScriptedWait(30)
                    return 'nothing'
                
                self.status = 'crafting'
                return (str(Actions.WithDrawBank), {
                    'item_to_get': item_to_get
                })
                
            case 'crafting':
                
                if self.pos != self.recipie['pos_to_craft']:  # move to craft pos.
                    return (str(Actions.Move), { 'pos': self.recipie['pos_to_craft'] })
                
                self.status = 'recycle' if self.recipie['is_recycle'] else 'set_bank'
                return (str(Actions.Craft), {
                    'item_to_craft': self.recipie['item_to_craft'],
                    'quantity': self.quantity_to_craft_now
                })
            
            case 'recycle':
                
                self.status = 'set_bank'
                return (str(Actions.Recycle), {
                    'items_to_recycle': self.recipie['item_to_craft'],
                    'items_quantity': self.quantity_to_craft_now
                })
            
            case 'set_bank':
                
                if self.pos != V2(4,1):  # walk to bank.
                    return (str(Actions.Move), { 'pos': V2(4,1) })

                self.status = 'get_bank'
                if self.inventoryQuantityFill != 0:
                    return (str(Actions.DropInBank), { 'item_to_drop': self.inventory })
                
                # already all done for 'set_bank'.
                return self.getActionPackage()
                    
