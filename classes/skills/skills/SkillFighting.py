from ..Skills import Skills
from ...characters.Characters import Characters
from ...primitives.Actions import Actions
from ...maps.MapsManager import MapsManager
from ...primitives.V2 import V2

class SkillFighting(Skills):

    def getAction(self, character: 'Characters') -> str|tuple[str,dict]|None:
        
        # TODO: implement MapsManager to compare pos and move to.

        if character.isInventoryFull():
            character.priority_actions.append(
                (Actions.DropInBank, {  # drop in bank all inventory ressource from mob loot.
                    'item_to_drop': [ i for i in character.inventory if (
                        i['type'] == 'resource' and
                        i['subtype'] == 'mob'
                    ) ]
                })
            )
            return (str(Actions.Move), {'pos': V2(4,1)})  # go to bank.

        if character.isAtPos(V2(0,1)):  # go map chicken.
            return (str(Actions.Move), {'pos': V2(0,1)})
        
        if character.getPurcentHp() < 0.3:  # regen HP.
            # TODO: if has consomable heal in inventory, and hp left >= quantity heal, use it. push other consomable in pool action. until hp > 0.8.
            return str(Actions.Rest)
        
        return str(Actions.Fight)  # fight.