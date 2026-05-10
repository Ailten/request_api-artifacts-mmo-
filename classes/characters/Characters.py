from abc import ABC
#from ..skills.Skills import Skills
from ..primitives.V2 import V2

class Characters(ABC):
    __pseudo: str
    skills: list  # list['Skills']
    __is_error: bool
    priority_actions: list[str|tuple[str,dict]]
    data_character: dict|None

    def __init__(self, pseudo: str):
        self.__pseudo = pseudo
        self.skills = []
        self.__is_error = False
        self.priority_actions = []
        self.data_character = None

    @property
    def pseudo(self) -> str:
        return self.__pseudo
    
    @property
    def is_error(self) -> bool:
        return self.__is_error
    
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
    

    # get the priority action (or None).
    def __getPriorityAction(self) -> str|tuple[str,dict]|None:
        
        while True:
        
            if len(self.priority_actions) == 0:
                return None

            pa = self.priority_actions[0]

            if (
                pa is tuple and
                'verify_if_it\'s_done' in pa[1] and
                pa[1]['verify_if_it\'s_done'](self)
            ):
                del self.priority_actions[0]
                continue

            del self.priority_actions[0]
            return pa
        

    # get the action based on skills.
    def __getSkillAction(self) -> str|tuple[str,dict]|None:

        for s in self.skills:
            action_from_skill = s.getAction()
            if action_from_skill == None:
                continue
            return action_from_skill
        return None
    

    # eval what action this character should do this update.
    def getActionPackage(self) -> str|tuple[str,dict]:

        return (
            self.__getPriorityAction() or
            self.__getSkillAction() or
            'nothing'
        )
    

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