
from classes import *
import time
from datetime import datetime, timezone


print('--- start ---')
api = APIConnection(Token)
CharactersManager.resetCharacters()


# re do the check server if all character are errored.
while True:


    # verify if data stock localy is matching server data (changing season).
    print('--- check server ---')
    try:
        response = api.checkServer()
        data = response.json()

        if 'error' in data:
            if 'message' in data['error']:
                raise Exception(data['error']['message'])
            raise Exception(data['error'])

        jm = JsonManager()
        data_server_json = jm.readServerData()
        characters_json = jm.readCharactersPseudo()
        if data_server_json['data']['season']['name'] != data['data']['season']['name']:

            print('--- new season ---')
            jm.writeServerData(data)
            characters_response = api.getCharacters(str(AcountName()))
            characters_data = characters_response.json()
            
            for i in range(len(characters_json)):
                cj = characters_json[i]
                cd = next([ cd for cd in characters_data['data'] if cd['name'] == cj ].__iter__(), None)

                if cd == None:
                    new_pseudo = CharactersManager.generateRandomPseudo()
                    api.createCharacter(cj, new_pseudo, CharactersManager.generateRandomSkin())
                    characters_json[i] = new_pseudo

            # erase/edit jsons, for new season start.
            jm.writeCharactersPseudo(characters_json)  # characters.
            CharactersManager.resetCharacters()

            is_first_map = True  # maps.
            for data_maps in api.getMaps():
                data_maps_filtered = MapsManager.filterEmptyMap(*data_maps)
                if len(data_maps_filtered) == 0:
                    continue
                jm.writeMaps(*data_maps_filtered, is_first_write=is_first_map)
                is_first_map = False
            jm.closeMaps()
            MapsManager.resetMapsFind()

            is_first_monster = True   # monsters.
            for data_monsters in api.getMonsters():
                jm.writeMonsters(*data_monsters, is_first_write=is_first_monster)
                is_first_monster = False
            jm.closeMonsters()
            MonstersManager.resetMonsters()

        # load from jsons.
        print('--- load from json ---')
        if len(CharactersManager.characters) == 0:  # characters.
            CharactersManager.loadCharacters(characters_json)
            for c in CharactersManager.characters:
                response = api.getCharacterData(c.pseudo)
                c_data_character = response.json()
                c.data_character = c_data_character['data']

        if not MapsManager.isMapsFindFilled():  # maps.
            data_maps_from_json = jm.readMaps()
            MapsManager.fillMapsFind(*data_maps_from_json)

        if not MonstersManager.isMonstersFilled():  # monsters.
            data_monsters = jm.readMonsters()
            MonstersManager.fillMonsters(*data_monsters)


    except Exception as e:
        raise e
    


    # update.
    print('--- update ---')
    while True:

        for c in CharactersManager.characters:
            
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
                
                if 'character' in data['data']:
                    c.data_character = data['data']['character']
                elif 'characters' in data['data']:
                    data_characters = data['data']['characters']
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


        # break update if all character ar errored.
        if len([ c for c in CharactersManager.characters if c.is_error ]) == len(CharactersManager.characters):
            print('--- all characters errored ---')
            break

        time.sleep(1)


# TODO: debug 'Rate limit exceeded: 10000 per 1 hour'.
# TODO: infinit loop somewhere after the json load.