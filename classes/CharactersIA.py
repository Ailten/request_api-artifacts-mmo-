from enum import IntEnum
from .Action import Action
from .primitives.V2 import V2

class CharactersIA(IntEnum):
    FightChicken=1
    GatheringAshWood=2
    DropInventoryInBanque=3
    DigCopper=4
    CraftCopperSet=5
    WaitForACopperArmorSet=6
    FightGreenSlime=7
    FightYellowSlime=8
    NotBotting=9
    CraftAshPlank=10
    CraftCopperOre=11

    def do_actions(self, characterData) -> 'Action'|tuple['Action', any]:

        # first call, to return the characterData for the next action.
        if characterData == None:
            return Action.Rest

        # switch on enum.
        match self:

            case CharactersIA.FightChicken:

                #if self.__isLevelFightUpperOrEqual(characterData, 5):  # if lvl 5 or more, stuff upgrade + change spot.
                #    return (Action.ChangeAction, {
                #        'character_ia': CharactersIA.WaitForACopperArmorSet
                #    })
        
                if self.__isInventoryFull(characterData):  # check if full inventory, drop all in bank.
                    return CharactersIA.DropInventoryInBanque.do_actions(characterData)

                if not self.__isAtChunkPos(characterData, V2(0, 1)):  # check if not at right chunck.
                    return (Action.Move, {'pos_tile': V2(0, 1)})
                
                if self.__isHpUnderPurcent(characterData, 0.3):  # check if need a rest.
                    return Action.Rest
                
                return Action.Fight  # fight.
            
            case CharactersIA.GatheringAshWood:
        
                if self.__isInventoryFull(characterData):  # check if full inventory, drop all in bank.
                    return (Action.ChangeAction, {
                        'character_ia': CharactersIA.CraftAshPlank
                    })

                if not self.__isAtChunkPos(characterData, V2(-1, 0)):  # check if not at right chunck.
                    return (Action.Move, {'pos_tile': V2(-1, 0)})
                
                return Action.Gathering  # gathering wood.
            
            case CharactersIA.DropInventoryInBanque:
                    
                if not self.__isAtChunkBank(characterData):
                    return (Action.Move, {'pos_tile': V2(4, 1)})
                return (Action.DropInventoryInBanque, {
                    'inventory': [ {
                        'code': cd['code'], 
                        'quantity': cd['quantity']
                    } for cd in characterData['inventory'] if cd['code'] != '' ]
                })
            
            case CharactersIA.DigCopper:
        
                if self.__isInventoryFull(characterData):  # check if full inventory, drop all in bank.
                    return CharactersIA.DropInventoryInBanque.do_actions(characterData)
                
                if not self.__isAtChunkPos(characterData, V2(2, 0)):  # check if not at right chunck.
                    return (Action.Move, {'pos_tile': V2(2, 0)})
                
                return Action.Gathering  # gathering copper.
            
            case CharactersIA.CraftCopperSet:

                # TODO: check inventory ressources.
                # check if other characters has items.
                
                return Action.Rest
            
            case CharactersIA.WaitForACopperArmorSet:

                # TODO.

                return (Action.ChangeAction, {
                    'character_ia': CharactersIA.NotBotting
                })
            
            case CharactersIA.FightYellowSlime:
        
                if self.__isInventoryFull(characterData):  # check if full inventory, drop all in bank.
                    return CharactersIA.DropInventoryInBanque.do_actions(characterData)

                if not self.__isAtChunkPos(characterData, V2(1, -2)):  # check if not at right chunck.
                    return (Action.Move, {'pos_tile': V2(1, -2)})
                
                if self.__isHpUnderPurcent(characterData, 0.3):  # check if need a rest.
                    return Action.Rest
                
                return Action.Fight  # fight.
            
            case CharactersIA.FightGreenSlime:
        
                if self.__isInventoryFull(characterData):  # check if full inventory, drop all in bank.
                    return CharactersIA.DropInventoryInBanque.do_actions(characterData)

                if not self.__isAtChunkPos(characterData, V2(0, -1)):  # check if not at right chunck.
                    return (Action.Move, {'pos_tile': V2(0, -1)})
                
                if self.__isHpUnderPurcent(characterData, 0.3):  # check if need a rest.
                    return Action.Rest
                
                return Action.Fight  # fight.
            
            case CharactersIA.NotBotting:

                return Action.DoNothing

            case CharactersIA.CraftAshPlank:

                if self.__isHasInInventory(characterData, 'ash_plank'):
                    if self.__isAtChunkBank(characterData):
                        return (Action.DropInventoryInBanque, {
                            'inventory': [{
                                'code': 'ash_plank',
                                'quantity': next([ i['quantity'] for i in characterData['inventory'] if i['code'] == 'ash_plank' ].__iter__(), 0)
                            }]
                        })
                    return (Action.Move, {'pos_tile': V2(4, 1)})
                
                if self.__isAtChunkBank(characterData):
                    return (Action.ChangeAction, {
                        'character_ia': CharactersIA.GatheringAshWood
                    })
                
                if not self.__isAtChunkPos(characterData, V2(-2, -3)):
                    return (Action.Move, {'pos_tile': V2(-2, -3)})
                
                return (Action.Crafting, {
                    'item_to_craft': 'ash_plank',
                    'quantity': next([ i['quantity'] for i in characterData['inventory'] if i['code'] == 'ash_wood' ].__iter__(), 0) // 10
                })
            
            case CharactersIA.CraftCopperOre:

                item_code_to_craft = 'copper_bar'

                if self.__isHasInInventory(characterData, item_code_to_craft):
                    if self.__isAtChunkBank(characterData):
                        return (Action.DropInventoryInBanque, {
                            'inventory': [{
                                'code': item_code_to_craft,
                                'quantity': next([ i['quantity'] for i in characterData['inventory'] if i['code'] == item_code_to_craft ], 0)
                            }]
                        })
                    return (Action.Move, {'pos_tile': V2(4, 1)})
                
                if self.__isAtChunkBank(characterData):
                    return (Action.ChangeAction, {
                        'character_ia': CharactersIA.DigCopper
                    })
                
                if not self.__isAtChunkPos(characterData, V2(1, 5)):
                    return (Action.Move, {'pos_tile': V2(1, 5)})
                
                return (Action.Crafting, {
                    'item_to_craft': item_code_to_craft,
                    'quantity': next([ i['quantity'] for i in characterData['inventory'] if i['code'] == 'copper_ore' ], 0) // 10
                })



            case _:
                raise Exception('no declaration for {self}')



            

    # return true if hp is under the purcentage sendid.
    def __isHpUnderPurcent(self, characterData, purcent: float) -> bool:
        return characterData['hp'] / characterData['max_hp'] < 0.3
    
    # return true if the inventory is full.
    def __isInventoryFull(self, characterData) -> bool:
        items_inventory_count = sum([ i['quantity'] for i in characterData['inventory']])
        return items_inventory_count == characterData['inventory_max_items']
    
    def __isAtChunkPos(self, characterData, pos: V2) -> bool:
        return characterData['x'] == pos.x and characterData['y'] == pos.y
    def __isAtChunkBank(self, characterData) -> bool:
        return self.__isAtChunkPos(characterData, V2(4, 1))
    
    def __isLevelFightUpperOrEqual(self, characterData, level_ask:int) -> bool:
        return characterData['level'] >= level_ask

    def __isHasInInventory(self, characterData, item_code: str) -> bool:
        return len([ i for i in characterData['inventory'] if i['code'] == item_code ]) >= 1