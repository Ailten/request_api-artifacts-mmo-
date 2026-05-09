from ..Skills import Skills
from ...characters.Characters import Characters
from ...primitives.Actions import Actions

class SkillFighter(Skills):

    def getAction(self, character: 'Characters') -> str|tuple[str,dict]|None:

        # TODO:
        # if character is at poss chicken (make a manager for position map, get from api, save on json when season start).
        # if hp upper 30%. (using function in character)
        # return action fight.

        #if character.isPos()