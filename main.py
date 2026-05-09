
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
            jm.writeServerData(data)
            characters_data = api.getCharacters(str(AcountName()))
            
            for i in range(len(characters_json)):
                cj = characters_json[i]
                cd = next([ cd for cd in characters_data if cd['name'] == cj ].__iter__(), None)

                if cd == None:
                    new_pseudo = CharactersManager.generateRandomPseudo()
                    api.createCharacter(cj, new_pseudo, CharactersManager.generateRandomSkin())
                    characters_json[i] = new_pseudo

            # erase/edit jsons, for new season start.
            jm.writeCharactersPseudo(characters_json)
            CharactersManager.resetCharacters()

        # load characters.
        if len(CharactersManager.characters) == 0:
            CharactersManager.loadCharacters(characters_json)

    except Exception as e:
        raise e
    


    # update.
    print('--- update ---')
    while True:

        for c in CharactersManager.characters:

            if len(c.priority_actions) > 0:
                


        # break update if all character ar errored.
        if len([ c for c in CharactersManager.characters if c.is_error ]) == len(CharactersManager.characters):
            print('--- all characters errored ---')
            break