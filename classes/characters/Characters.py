from abc import ABC

class Characters(ABC):
    __pseudo: str
    skills: list[str]
    __is_error: bool
    priority_actions: list[str|tuple[str,dict]]

    def __init__(self, pseudo: str):
        self.__pseudo = pseudo
        self.skills = []
        self.__is_error = False
        self.priority_actions = []

    @property
    def pseudo(self) -> str:
        return self.__pseudo
    
    @property
    def is_error(self) -> bool:
        return self.__is_error
    

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
        
    

    # eval what action this character should do this update.
    def getActionPackage(self) -> str|tuple[str,dict]:

        return (
            self.__getPriorityAction() or
            self.__getSkillAction() or
            'nothing'
        )



