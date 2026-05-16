from abc import ABC
from .primitives.V2 import V2
from datetime import datetime, timezone, timedelta

from typing import TYPE_CHECKING 
if TYPE_CHECKING:
    from APIConnection import APIConnection

class Characters(ABC):
    pseudo: str
    is_error: bool
    data_character: dict|None
    cooldown: datetime
    is_scripted_wait: bool

    # FIXME: maybe don't stock the apiConnection in Character.
    api: 'APIConnection|None' = None

    def __init__(self, pseudo: str):
        self.pseudo = pseudo
        self.is_error = False
        self.data_character = None
        self.cooldown = datetime.now(timezone.utc)
        self.is_scripted_wait = False

    @property
    def pos(self) -> 'V2':
        return V2(self.data_character['x'], self.data_character['y'])
    
    @property
    def inventory(self) -> list[dict]:
        return [ e for e in self.data_character['inventory'] if e['code'] != '' ]
    
    @property
    def inventoryQuantityFill(self) -> int:
        return sum([ e['quantity'] for e in self.inventory ])
    
    @property
    def inventoryMaxCapacity(self) -> int:
        return self.data_character['inventory_max_items']
    
    @property
    def hp(self) -> int:
        return self.data_character['hp']
    
    @property
    def maxHp(self) -> int:
        return self.data_character['max_hp']
    
    @property
    def bankInventory(self) -> list[dict]:
        response = self.api.request_get_bank_data()  # FIXME: take 100 first row bank (not all theoretically).
        return response.json()['data']
    

    # ---->
    

    # eval what action this character should do this update.
    def getActionPackage(self) -> str|tuple[str,dict]:
        self.is_error = True
        return 'nothing'
    

    # --->


    # reset cooldown (for next call api), based on data_character.
    def setCooldown(self):
        date_str = self.data_character['cooldown_expiration']
        self.cooldown = datetime.fromisoformat(date_str.replace('Z', '+00:00'))  # cast string to datetime.
    
    # define a scripted cooldown (when character don't have to do nothing from many minutes).
    def setScriptedWait(self, minutes_to_wait: int):
        self.cooldown = datetime.now(timezone.utc)
        self.cooldown += timedelta(minutes=minutes_to_wait)


    # ---->


    def isAtPos(self, map_pos: 'V2') -> bool:
        return self.pos == map_pos
    
    def isInventoryFull(self) -> bool:
        return self.inventoryQuantityFill == self.inventoryMaxCapacity
    
    def getPurcentInventoryFull(self) -> float:
        return self.inventoryQuantityFill / self.inventoryMaxCapacity

    def getPurcentHp(self) -> float:
        return self.hp / self.maxHp

    def getHpLeft(self) -> int:
        return self.maxHp - self.hp