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
        interactions_contend: str,
        layer: str="overworld",
        closest_to_pos: V2|None = None
    ) -> V2:
        maps_filtered = [ dm for dm in MapsManager.__maps_find if (
            dm['interactions']['contend'] == interactions_contend and
            dm['layer'] == layer
        ) ]

        if closest_to_pos != None:
            maps_filtered.sort(key=lambda dm: closest_to_pos.distTo(V2(dm['x'], dm['y'])))

        if len(maps_filtered) == 0:
            return None
        return V2(maps_filtered[0]['x'], maps_filtered[0]['y'])


    # --->
    
    @classmethod
    def __is_map_empty(cls, data_map) -> bool:
        if data_map['name'] == 'Empty':
            return True
        if data_map['interactions']['content'] == None:
            return True
        return False
