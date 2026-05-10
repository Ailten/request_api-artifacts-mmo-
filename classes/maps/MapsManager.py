from ..primitives.V2 import V2

class MapsManager:
    __maps_find: list[dict] = []

    @classmethod
    def isMapsFindFilled(self) -> bool:
        return len(self.__maps_find) > 0

    @classmethod
    def resetMapsFind(cls):
        MapsManager.__maps_find = []

    @classmethod
    def fillMapsFind(cls, *data_maps: dict):
        MapsManager.__maps_find += data_maps

    @classmethod
    def filterEmptyMap(cls, *data_maps: dict) -> dict:
        return [ dm for dm in data_maps if not MapsManager.__is_map_empty(dm) ]

    @classmethod
    def getMapPos(cls, 
        interactions_contend: str|None=None,
        layer: str|None=None,
        monster_name: str|None = None,
        closest_to_pos: V2|None = None
    ) -> V2:
        maps_filtered = MapsManager.__maps_find
        
        if interactions_contend != None:
            maps_filtered = [ dm for dm in maps_filtered if dm['interactions']['contend']['type'] == interactions_contend ]
        if layer != None:
            maps_filtered = [ dm for dm in maps_filtered if dm['layer'] == layer ]
        if monster_name != None:
            maps_filtered = [ dm for dm in maps_filtered if (
                dm['interactions']['contend']['type'] == 'monster' and
                dm['interactions']['contend']['code'] == monster_name
            ) ]

        if closest_to_pos != None:
            maps_filtered.sort(key=lambda dm: closest_to_pos.distTo(V2(dm['x'], dm['y'])))

        if len(maps_filtered) == 0:
            return None
        return V2(maps_filtered[0]['x'], maps_filtered[0]['y'])
    
    @classmethod
    def getMapPosBank(cls,
        layer: str|None=None,
        closest_to_pos: V2|None = None
    ) -> V2:
        return MapsManager.getMapPos(
            interactions_contend='bank',
            layer=layer,
            closest_to_pos=closest_to_pos
        )



    # --->
    
    @classmethod
    def __is_map_empty(cls, data_map) -> bool:
        if data_map['name'] == 'Empty':
            return True
        if data_map['interactions']['content'] == None:
            return True
        return False
