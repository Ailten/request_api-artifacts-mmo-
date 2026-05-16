from .tokens.AbstractToken import AbstractToken
from .primitives.Action import Actions
from .primitives.V2 import V2
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
    def request_drop_in_banque(self, character_pseudo: str, items_to_drop: list[dict]):
        return requests.post(
            url=f'{self.__base_url}/my/{character_pseudo}/action/bank/deposit/item', 
            headers=self.__getHeader(),
            json=items_to_drop
        )
    
    # get list items from bank.
    def request_get_bank_items(self, character_pseudo: str, items_to_get: list[dict]):
        return requests.post(
            url=f'{self.__base_url}/my/{character_pseudo}/action/bank/withdraw/item', 
            headers=self.__getHeader(),
            json=items_to_get
        )
    
    # recycle items (from inventory character).
    def request_recycle(self, character_pseudo: str, items_to_recycle: str, items_quantity: int=1):
        return requests.post(
            url=f'{self.__base_url}/my/{character_pseudo}/action/recycling', 
            headers=self.__getHeader(),
            json={ 'code': items_to_recycle, 'quantity': items_quantity }
        )
    

    def request_action(self, character_pseudo: str, action: str, body_action: dict|None=None):
        match action:
            case str(Actions.Move):
                return self.request_move(character_pseudo, body_action['pos'])
            case str(Actions.Fight):
                return self.request_fight(character_pseudo)
            case str(Actions.Rest):
                return self.request_rest(character_pseudo)
            case str(Actions.Gather):
                return self.request_gathering(character_pseudo)
            case str(Actions.Unequip):
                return self.request_unequip(character_pseudo, body_action['category_equipement'])
            case str(Actions.Craft):
                return self.request_craft(character_pseudo, body_action['item_to_craft'], body_action.get('quantity', 1))
            case str(Actions.Equip):
                return self.request_equip(character_pseudo, body_action['equipement'], body_action['category_equipement'])
            case str(Actions.DropInBank):
                return self.request_drop_in_banque(character_pseudo, body_action['item_to_drop'])
            case str(Actions.WithDrawBank):
                return self.request_get_bank_items(character_pseudo, body_action['item_to_get'])
            case str(Actions.Recycle):
                return self.request_recycle(character_pseudo, body_action['items_to_recycle'], body_action['items_quantity'])

            case _:
                raise Exception(f'no implement for action {action}')
                
    
    # ----> acount request.


    # get bank data.
    def request_get_bank_data(self):
        return requests.get(
            url=f'{self.__base_url}/my/bank/items?size={100}',
            headers=self.__getHeader()
        )