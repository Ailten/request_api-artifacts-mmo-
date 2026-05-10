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
            f.write('')

    def writeMaps(self, *data_maps: dict):
        with open('json_data/maps.json', 'a', encoding='utf-8') as f:
            for map in data_maps:
                map_str = json.dumps(map)
                map_str += '\n'  # separator.
                f.write(map_str)

    def readMaps(self) -> list[dict]:
        with open('json_data/maps.json', 'r', encoding='utf-8') as f:
            maps_str = f.read()
            if maps_str[-1] == '\n':  # remove last separator.
                maps_str = maps_str[:-1]
            maps_str = maps_str.replace('\n', ',')
            maps_str = '[' + maps_str + ']'
            return json.loads(maps_str)
        
    def eraseMonsters(self):
        with open('json_data/monsters.json', 'w', encoding='utf-8') as f:
            f.write('')
        
    def writeMonsters(self, *data_monsters):
        with open('json_data/monsters.json', 'a', encoding='utf-8') as f:
            for monster in data_monsters:
                monster_str = json.dumps(monster)
                monster_str += '\n'  # separator.
                f.write(monster_str)

    def readMonsters(self):
        with open('json_data/monsters.json', 'r', encoding='utf-8') as f:
            monster_str = f.read()
            if monster_str[-1] == '\n':  # remove last separator.
                monster_str = monster_str[:-1]
            monster_str = monster_str.replace('\n', ',')
            monster_str = '[' + monster_str + ']'
            return json.loads(monster_str)
