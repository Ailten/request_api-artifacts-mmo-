from .tokens.AbstractToken import AbstractToken
from .Characters import Characters
from .primitives.V2 import V2
from .CategoryEquipement import CategoryEquipement
from .Action import Action
from.CharactersBot import CharactersBot
import requests

class APIConnection:
    __base_url: str = 'https://api.artifactsmmo.com'
    __token_cls: 'AbstractToken'
    is_debug: bool

    def __init__(self, token_cls: 'AbstractToken', is_debug:bool=True):
        self.__token_cls = token_cls
        self.is_debug = is_debug

    # get header.
    def __getHeader(self) -> dict:
        return {
          "Accept": "application/json",
          "Content-Type": "application/json",
          "Authorization": f"Bearer {self.__getToken()}"
        }
    
    # get token.
    def __getToken(self) -> 'AbstractToken':
        return self.__token_cls()
    

    # --- actions.

    # move a character to a chunck.
    def request_move(self, character: 'Characters', pos_tile: 'V2'):
        return requests.post(
            url=f'{self.__base_url}/my/{str(character)}/action/move', 
            headers=self.__getHeader(), 
            json=pos_tile.__dict__()
        )
    
    # make character fight at his current chunk.
    def request_fight(self, character: 'Characters'):
        return requests.post(
            url=f'{self.__base_url}/my/{str(character)}/action/fight', 
            headers=self.__getHeader()
        )
    
    # make a character rest (after a fight).
    def request_rest(self, character: 'Characters'):
        return requests.post(
            url=f'{self.__base_url}/my/{str(character)}/action/rest', 
            headers=self.__getHeader()
        )
    
    # make character cutting wood (or get ressources of the chunk).
    def request_gathering(self, character: 'Characters'):
        return requests.post(
            url=f'{self.__base_url}/my/{str(character)}/action/gathering', 
            headers=self.__getHeader()
        )

    # unequipe an item (move to inventory).
    def request_unequip(self, character: 'Characters', category_equipement: 'CategoryEquipement'):
        return requests.post(
            url=f'{self.__base_url}/my/{str(character)}/action/unequip', 
            headers=self.__getHeader(),
            json={ "slot": str(category_equipement) }
        )
    
    # craft an item (need to have ressources in invetory character).
    def request_craft(self, character: 'Characters', item_to_craft: str, quantity: int=1):
        return requests.post(
            url=f'{self.__base_url}/my/{str(character)}/action/crafting', 
            headers=self.__getHeader(),
            json={ "code": item_to_craft , "quantity": quantity}
        )
    
    # equip an equipement from inventaire to the slot of character.
    def request_equip(self, character: 'Characters', equipement: str, category_equipement: 'CategoryEquipement'):
        return requests.post(
            url=f'{self.__base_url}/my/{str(character)}/action/equip', 
            headers=self.__getHeader(),
            json={ "code": equipement, "slot": str(category_equipement) }
        )
    
    # drop items in banque.
    def request_drop_in_banque(self, character: 'Characters', items_to_drop: list):
        return requests.post(
            url=f'{self.__base_url}/my/{str(character)}/action/bank/deposit/item', 
            headers=self.__getHeader(),
            json=items_to_drop
        )
    
    # action spliter.
    def request_action(self, action: 'Action', character: 'Characters', dict_body: dict|None=None):

        match action:
            case Action.Move:
                return self.request_move(character, dict_body['pos_tile'])
            case Action.Fight:
                return self.request_fight(character)
            case Action.Rest:
                return self.request_rest(character)
            case Action.Gathering:
                return self.request_gathering(character)
            case Action.Unequip:
                return self.request_unequip(character, dict_body['category_equipement'])
            case Action.Crafting:
                return self.request_craft(character, dict_body['item_to_craft'], dict_body['quantity'])
            case Action.Equip:
                return self.request_equip(character, dict_body['equipement'], dict_body['category_equipement'])
            case Action.DropInventoryInBanque:
                return self.request_drop_in_banque(character, dict_body['inventory'])
            
            case _:
                raise Exception(f'no action declared for {action}')
