from .tokens.AbstractToken import AbstractToken
from .primitives.V2 import V2
from .primitives.Actions import Actions
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
    def request_move(self, character_pseudo: str, pos_tile: 'V2'):
        return requests.post(
            url=f'{self.__base_url}/my/{character_pseudo}/action/move', 
            headers=self.__getHeader(), 
            json=pos_tile.__dict__()
        )
    
    # make character fight at his current chunk.
    def request_fight(self, character_pseudo: str):
        return requests.post(
            url=f'{self.__base_url}/my/{character_pseudo}/action/fight', 
            headers=self.__getHeader()
        )
    
    # make a character rest (after a fight).
    def request_rest(self, character_pseudo: str):
        return requests.post(
            url=f'{self.__base_url}/my/{character_pseudo}/action/rest', 
            headers=self.__getHeader()
        )
    
    # make character cutting wood (or get ressources of the chunk).
    def request_gathering(self, character_pseudo: str):
        return requests.post(
            url=f'{self.__base_url}/my/{character_pseudo}/action/gathering', 
            headers=self.__getHeader()
        )

    # unequipe an item (move to inventory).
    def request_unequip(self, character_pseudo: str, category_equipement: str):
        return requests.post(
            url=f'{self.__base_url}/my/{character_pseudo}/action/unequip', 
            headers=self.__getHeader(),
            json={ "slot": str(category_equipement) }
        )
    
    # craft an item (need to have ressources in invetory character).
    def request_craft(self, character_pseudo: str, item_to_craft: str, quantity: int=1):
        return requests.post(
            url=f'{self.__base_url}/my/{character_pseudo}/action/crafting', 
            headers=self.__getHeader(),
            json={ "code": item_to_craft , "quantity": quantity}
        )
    
    # equip an equipement from inventaire to the slot of character.
    def request_equip(self, character_pseudo: str, equipement: str, category_equipement: str):
        return requests.post(
            url=f'{self.__base_url}/my/{character_pseudo}/action/equip', 
            headers=self.__getHeader(),
            json={ "code": equipement, "slot": category_equipement }
        )
    
    # drop items in banque.
    def request_drop_in_banque(self, character_pseudo: str, items_to_drop: list):
        return requests.post(
            url=f'{self.__base_url}/my/{character_pseudo}/action/bank/deposit/item', 
            headers=self.__getHeader(),
            json=items_to_drop
        )
    

    def request_action(self, character_pseudo: str, action: str, body_action: dict|None=None):
        match action:  # TODO: make it a class abc and sub-class Actions.
            case 'nothing':
                return
            case str(Actions.Move):
                self.request_move(character_pseudo, body_action['pos'])
            case str(Actions.Fight):
                self.request_fight(character_pseudo)
            case str(Actions.Rest):
                self.request_rest(character_pseudo)
            case str(Actions.Gather):
                self.request_gathering(character_pseudo)
            case str(Actions.Unequip):
                self.request_unequip(character_pseudo, body_action['category_equipement'])
            case str(Actions.Craft):
                self.request_craft(character_pseudo, body_action['item_to_craft'], body_action.get('quantity', 1))
            case str(Actions.Equip):
                self.request_equip(character_pseudo, body_action['equipement'], body_action['category_equipement'])
            case str(Actions.DropInBank):
                self.request_drop_in_banque(character_pseudo, body_action['item_to_drop'])

            case _:
                raise Exception(f'no implement for action {action}')
                
    

    # --- server.

    # get data from server (about season).
    def checkServer(self):
        return requests.get(
            url=f'https://api.artifactsmmo.com/',
            headers={ "Accept": "application/json" }
        )
    
    def getCharacters(self, acount_name: str):
        return requests.get(
            url=f'https://api.artifactsmmo.com/accounts/{acount_name}/characters',
            headers={ "Accept": "application/json" }
        )
        
    def createCharacter(self, character_pseudo: str, skin: str='men1'):
        return requests.get(
            url=f'https://api.artifactsmmo.com/characters/create',
            headers=self.__getHeader(),
            json={  
                "name": character_pseudo,
                "skin": skin
            }
        )