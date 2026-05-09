from .Characters import Characters
from datetime import datetime
from .CharactersIA import CharactersIA
from datetime import datetime, timezone

class CharactersBot:
    character: 'Characters'
    cooldown: datetime
    is_error: bool
    ia: 'CharactersIA'
    character_data: any

    def __init__(self, character: 'Characters', ia: 'CharactersIA'):
        self.character = character
        self.cooldown = datetime.now(timezone.utc)
        self.is_error = False
        self.ia = ia
        self.character_data = None

    # decrease cooldown (for update and see when it ready to do other action).
    def decreaseCooldown(self, value_decrease: int=1) -> int:
        self.cooldown -= value_decrease
        return self.cooldown
    
    # set cooldown date from a character_data (default, take the one in the CharacterBot it self).
    def setCooldown(self, character_data_send=None):
        if character_data_send == None:
            character_data_send = self.character_data

        date_str = character_data_send['cooldown_expiration']
        self.cooldown = datetime.fromisoformat(date_str.replace('Z', '+00:00'))  # cast string to datetime.
    
    # change IA of a characterBot.
    def changeIA(self, new_ia: 'CharactersIA', dict_body: dict, all_characters_bots: list['CharactersBot']):
        self.ia = new_ia

        # TODO: add request to comunicate intention with eatch others (from dict_body).

