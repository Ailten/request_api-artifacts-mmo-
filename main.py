
from classes import *


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

            jm.eraseMaps()  # maps.
            for data_maps in api.getMaps():
                data_maps_filtered = MapsManager.filterEmptyMap(*data_maps)
                jm.writeMaps(*data_maps_filtered)
            MapsManager.resetMapsFind()

            jm.eraseMonsters()  # monsters.
            for data_monsters in api.getMonsters():
                jm.writeMonsters(*data_monsters)
            MonstersManager.resetMonsters()

        # load from jsons.
        print('--- load from json ---')
        if len(CharactersManager.characters) == 0:  # characters.
            CharactersManager.loadCharacters(characters_json)

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

            action_package = c.getActionPackage()
            action = None
            body_action = None
            if action_package is str:
                action = action_package
            elif action_package is tuple:
                action = action_package[0]
                body_action = action_package[1]

            api.request_action(c.pseudo, action, body_action)

        # break update if all character ar errored.
        if len([ c for c in CharactersManager.characters if c.is_error ]) == len(CharactersManager.characters):
            print('--- all characters errored ---')
            break