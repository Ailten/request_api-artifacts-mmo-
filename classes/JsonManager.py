import json

class JsonManager:


    def __init__(self):
        pass


    def readServerData(self):
        try:
            with open('json_data/server.json', 'r', encoding='utf-8') as f:
                data_str = f.read()
                data = json.load(data_str)
                return data
        except json.JSONDecodeError as e:
            return {'data': {'season': {'name': 'None'}}}
        except Exception as e:
            raise e
        
    def writeServerData(self, data):
        with open('json_data/server.json', 'w', encoding='utf-8') as f:
            data_str = json.dump(data)
            f.write(data_str)


    def readCharactersPseudo(self):
        try:
            with open('json_data/charactersPseudo.json', 'r', encoding='utf-8') as f:
                data_str = f.read()
                data = json.load(data_str)
                return data
        except json.JSONDecodeError as e:
            return {}
        except Exception as e:
            raise e

    def writeCharactersPseudo(self, characters_pseudo: list[str]):
        with open('json_data/charactersPseudo.json', 'w', encoding='utf-8') as f:
            data_str = json.dump(characters_pseudo)
            f.write(data_str)
