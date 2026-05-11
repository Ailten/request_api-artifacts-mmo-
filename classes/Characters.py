from abc import ABC
from .primitives.V2 import V2
from datetime import datetime, timezone

class Characters(ABC):
    pseudo: str
    is_error: bool
    data_character: dict|None
    cooldown: datetime

    def __init__(self, pseudo: str):
        self.pseudo = pseudo
        self.is_error = False
        self.data_character = None
        self.cooldown = datetime.now(timezone.utc)

    @property
    def pos(self) -> 'V2':
        return V2(self.data_character['x'], self.data_character['y'])
    
    @property
    def inventory(self) -> list[dict]:
        return self.data_character['inventory']
    
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