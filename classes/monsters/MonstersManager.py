from ..primitives.V2 import V2

class MonstersManager:
    __monsters: list[dict] = []

    @classmethod
    def isMonstersFilled(self) -> bool:
        return len(self.__monsters) > 0

    @classmethod
    def resetMonsters(cls):
        MonstersManager.__monsters = []

    @classmethod
    def fillMonsters(cls, *data_monsters: dict):
        MonstersManager.__monsters += data_monsters
    
    @classmethod
    def getMonster(cls,
        name: str|None = None,
        level_max: int|None = None,
        drop: str|None = None
    ) -> dict|None:
        monsters_filtered = MonstersManager.__monsters
        
        if name != None:
            monsters_filtered = [ m for m in monsters_filtered if m['code'] == name ]
        if level_max != None:
            monsters_filtered = [ m for m in monsters_filtered if m['level'] <= level_max ]
        if drop != None:
            monsters_filtered = [ m for m in monsters_filtered if (
                drop in [ d['code'] for d in m['drops'] ]
            ) ]
        
        if len(monsters_filtered) == 0:
            return None
        return monsters_filtered[0]

    

    

