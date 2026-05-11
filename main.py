
from classes import *
from time import time
from datetime import datetime, timezone

print('--- start ---')


api = APIConnection(Token)
all_characters = [
    Fighter('RedHat', V2(0, -1)),
    WoodCuter('Askunk'),
    Miner('Digidix'),
    Characters('Craftax'),  # TODO: make as alchimist.
    Fighter('Fedora')
]
for c in all_characters:
    response = api.request_rest(c.pseudo)
    data = response.json()
    c.data_character = data['data']['character']
    c.setCooldown()


while True:

    for c in all_characters:
        
        if c.is_error:
            continue
        if c.cooldown > datetime.now(timezone.utc):
            continue

        action_package = c.getActionPackage()
        action = None
        body_action = None
        if type(action_package) == str:
            action = action_package
        elif type(action_package) == tuple:
            action = action_package[0]
            body_action = action_package[1]

        if action == 'nothing':
            continue

        try:

            response = api.request_action(c.pseudo, action, body_action)
            data_action = response.json()
                
            if "error" in data_action:
                if "message" in data_action["error"]:
                    raise Exception(data_action["error"]["message"])
                raise Exception(data_action["error"])
                
            if 'character' in data_action['data']:
                c.data_character = data_action['data']['character']
            elif 'characters' in data_action['data']:
                data_characters = data_action['data']['characters']
                data_characters = [ cs for cs in data_characters if cs['name'] == str(c.pseudo)]
                if len(data_characters) != 1:
                    raise Exception(f'data[\'characters\'] has no character named {c.pseudo}')
                c.data_character = data_characters[0]
            else:
                raise Exception(f'data[\'characters\'] has no character named {c.pseudo}')

        except Exception as e:

            c.is_error = True
            print('/!\\ --- ERROR --- /!\\')
            print(f'character : {c.pseudo}')
            print(f'error : {e}')
            print(f'action try : {action_package}')
            print('---------------------')

            if api.is_debug:
                raise e
                
        c.setCooldown()

