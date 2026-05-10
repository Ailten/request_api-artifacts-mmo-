from ..Skills import Skills
from ...characters.Characters import Characters
from ...primitives.Actions import Actions
from ...maps.MapsManager import MapsManager
from ...primitives.V2 import V2
from ...monsters.MonstersManager import MonstersManager

class SkillFighting(Skills):
    data_monster: dict|None
    pos_to_fight: V2|None

    def __init__(self, data_monster: dict|None):
        self.data_monster = data_monster or MonstersManager.getMonster(level_max=1)



    def getAction(self, character: 'Characters') -> str|tuple[str,dict]|None:
        
        if self.pos_to_fight == None:
            self.pos_to_fight = MapsManager.getMapPos(
                monster_name=self.data_monster['code']
            )
            if self.pos_to_fight == None:
                raise Exception(f'no map pos found for {self.data_monster['code']}')

        if character.isInventoryFull():
            character.priority_actions.append(
                (Actions.DropInBank, {  # drop in bank all inventory ressource from mob loot.
                    'item_to_drop': [ i for i in character.inventory if (
                        i['type'] == 'resource' and
                        i['subtype'] == 'mob'
                    ) ]
                })
            )
            return (str(Actions.Move), {'pos': MapsManager.getMapPosBank()})  # go to bank.

        if character.isAtPos(self.pos_to_fight):  # go map for fight.
            return (str(Actions.Move), {'pos': self.pos_to_fight})
        
        if character.getPurcentHp() < 0.3:  # regen HP.
            # TODO: if has consomable heal in inventory, and hp left >= quantity heal, use it. push other consomable in pool action. until hp > 0.8.
            return str(Actions.Rest)
        
        return str(Actions.Fight)  # fight.