from enum import Enum
from .CharactersIA import CharactersIA

class Characters(str, Enum):
    RedHat='RedHat'
    Askunk='Askunk'
    Digidix='Digidix'
    Craftax='Craftax'
    Fedora='Fedora'

    def __str__(self) -> str:
        return super().__str__()
    
    # assigne an action to value enum of Characters.
    def get_ia(self) -> 'CharactersIA':

        match self:
            case Characters.RedHat:
                return CharactersIA.FightChicken
                #return CharactersIA.FightYellowSlime
                #return CharactersIA.NotBotting
            case Characters.Askunk:
                return CharactersIA.GatheringAshWood
            case Characters.Digidix:
                return CharactersIA.DigCopper
            case Characters.Craftax:
                return CharactersIA.NotBotting
                #return CharactersIA.DigCopper
                #return CharactersIA.CraftCopperSet
            case Characters.Fedora:
                return CharactersIA.FightChicken
            
            case _:
                raise Exception(f'no IA assigne to {self}')
