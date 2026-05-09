
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
            jm.resetSeason(data)

    except Exception as e:
        raise e


    # TODO: request, to compare if need to re create Character.
    # TODO: request when launch to compare the API data, to data stocked (for re-write json data).


    # update.
    while True:

        # TODO.

        break