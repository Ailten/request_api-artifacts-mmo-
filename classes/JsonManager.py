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
    
    def resetSeason(self, data_server):
        self.writeServerData(data_server)

