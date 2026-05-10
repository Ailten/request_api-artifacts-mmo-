import json

class JsonManager:


    def __init__(self):
        pass


    def readServerData(self) -> dict:
        try:
            with open('json_data/server.json', 'r', encoding='utf-8') as f:
                data_str = f.read()
                if data_str == '':
                    return {'data': {'season': {'name': 'None'}}}
                data = json.loads(data_str)
                return data
        except Exception as e:
            raise e
        
    def writeServerData(self, data):
        with open('json_data/server.json', 'w', encoding='utf-8') as f:
            data_str = json.dumps(data)
            f.write(data_str)


    def readCharactersPseudo(self) -> list:
        try:
            with open('json_data/charactersPseudo.json', 'r', encoding='utf-8') as f:
                data_str = f.read()
                data = json.loads(data_str)
                return data
        except Exception as e:
            raise e

    def writeCharactersPseudo(self, characters_pseudo: list[str]):
        with open('json_data/charactersPseudo.json', 'w', encoding='utf-8') as f:
            data_str = json.dumps(characters_pseudo)
            f.write(data_str)

    def eraseMaps(self):
        with open('json_data/maps.json', 'w', encoding='utf-8') as f:
            f.write('[\n')
    def closeMaps(self):
        with open('json_data/maps.json', 'a', encoding='utf-8') as f:
            f.write('\n]')

    def writeMaps(self, *data_maps: dict, is_first_write: bool=False):
        with open('json_data/maps.json', 'a', encoding='utf-8') as f:
            for map in data_maps:
                map_str = json.dumps(map)
                if is_first_write:
                    self.eraseMaps()
                    is_first_write = False
                else:
                    map_str = ',\n' + map_str  # separator.
                f.write(map_str)

    def readMaps(self) -> list[dict]:
        with open('json_data/maps.json', 'r', encoding='utf-8') as f:
            maps_str = f.read()
            return json.loads(maps_str)
        
    def eraseMonsters(self):
        with open('json_data/monsters.json', 'w', encoding='utf-8') as f:
            f.write('[\n')
    def closeMonsters(self):
        with open('json_data/monsters.json', 'a', encoding='utf-8') as f:
            f.write('\n]')
        
    def writeMonsters(self, *data_monsters, is_first_write: bool=False):
        with open('json_data/monsters.json', 'a', encoding='utf-8') as f:
            for monster in data_monsters:
                monster_str = json.dumps(monster)
                if is_first_write:
                    self.eraseMonsters()
                    is_first_write = False
                else:
                    monster_str = ',\n' + monster_str  # separator.
                f.write(monster_str)

    def readMonsters(self) -> list[dict]:
        with open('json_data/monsters.json', 'r', encoding='utf-8') as f:
            monster_str = f.read()
            return json.loads(monster_str)
