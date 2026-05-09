
from classes import *
import time
from datetime import datetime, timezone


print('--- start ---')
api = APIConnection(Token)


#request = api.request_equip(Characters.Digidix, 'copper_pickaxe', CategoryEquipement.Weapon)
#print(request.json())
#raise Exception()


charactersBot = [ CharactersBot(c, c.get_ia()) for c in Characters]

while True:

    for c in charactersBot:

        action_tuple = None
        try:

            # if character has found an error: continue.
            if c.is_error:
                continue

            # if not ready yet: continue.
            if c.cooldown > datetime.now(timezone.utc):
                continue

            # get action todo.
            action = None
            dict_body = None
            while True:  # loop (only for change action case).

                action_tuple = c.ia.do_actions(c.character_data)

                if type(action_tuple) == tuple:
                    action = action_tuple[0]
                    dict_body = action_tuple[1]
                else:
                    action = action_tuple

                # case when action whant to change the action of a characterBot (definitely).
                if str(action) == 'change_action':
                    c.changeIA(dict_body['character_ia'], dict_body, charactersBot)
                    continue

                break

            if str(action) == 'nothing':
                continue

            # do the action.
            response = api.request_action(action, c.character, dict_body)
            data = response.json()

            # catch error from api call.
            if "error" in data:
                if "message" in data["error"]:
                    raise Exception(data["error"]["message"])
                raise Exception(data["error"])
            
            # set data (for next call).
            if 'character' in data['data']:
                c.character_data = data['data']['character']
            elif 'characters' in data['data']:
                data_characters = data['data']['characters']
                data_characters = [ cs for cs in data_characters if cs['name'] == str(c.character)]
                if len(data_characters) != 1:
                    raise Exception(f'data[\'characters\'] has no character named {c.character}')
                c.character_data = data_characters[0]
            else:
                print([ k for k, v in data['data'].items() ])
                raise Exception('no character found in response')
            c.setCooldown()

        except Exception as e:
            
            c.is_error = True
            print('/!\\ --- ERROR --- /!\\')
            print(f'character : {c.character}')
            print(f'error : {e}')
            print(f'action try : {action_tuple}')
            print('---------------------')

            if api.is_debug:
                raise e

    # cut if all character are error.
    if next([ c for c in charactersBot if not c.is_error ].__iter__(), None) == None:
        print('--- all character has error ---')
        break


    time.sleep(1)

print('--- end ---')


# TODO: add an IA logic about take coper from bank, making lingot, crafting full set armor, drop back at bank.
# TODO: add an IA logic about cutting fight interaction, and moving to bank, grab full set armor, and go back fight.
# TODO: same for axe, and picax.

# TODO: scan map, for searching spot to farm (like bank, tree, mine, mobs).

# TODO: edit fight chicken, for doing craft with meat, when a big quantity in inventory (30~60).
# TODO: edit fight chicken, for making eat meat cooked, if has in inventory.

# TODO: add a character to farm sun-flower, and craft potion.

# TODO: edit fight chicken, for making take a quest before.
# TODO: re-take quest when completed.

# TODO: add loop craft between mine and bank.

# TODO: allow sub action, or linked action.

# TODO: rate limite exceed (10000/hour).