
from classes import *


print('--- start ---')
api = APIConnection(Token)


# re do the check server if all character are errored.
while True:


    # verify if data stock localy is matching server data (changing season).
    try:
        response = api.checkServer()
        data = response.json()

        if 'error' in data:
            if 'message' in data['error']:
                raise Exception(data['error']['message'])
            raise Exception(data['error'])

        jm = JsonManager()
        data_server_json = jm.readServerData()
        if data_server_json['data']['season']['name'] != data['data']['season']['name']:
            jm.writeServerData(data)
            characters_data = api.getCharacters(str(AcountName()))
            characters_json = jm.readCharactersPseudo()
            
            for i in range(len(characters_json)):
                cj = characters_json[i]
                cd = next([ cd for cd in characters_data if cd['name'] == cj ].__iter__(), None)

                if cd == None:
                    new_pseudo = CharactersManager.generateRandomPseudo()
                    api.createCharacter(cj, new_pseudo, CharactersManager.generateRandomSkin())
                    characters_json[i] = new_pseudo

            # erase/edit jsons, for new season start.
            jm.writeCharactersPseudo(characters_json)

    except Exception as e:
        raise e


    # update.
    while True:

        # TODO.

        break