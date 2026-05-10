from .Characters import Characters
from ..skills.skills import *
import random

class CharactersManager:
    characters: list['Characters'] = []

    @classmethod
    def generateRandomSkin(cls):
        skins = [
            'men1', 'men2', 'men3',
            'women1', 'women2', 'women3'
        ]
        rng_id = random.randint(0, len(skins)-1)
        return skins[rng_id]
    
    @classmethod
    def generateRandomPseudo(cls):
        voyelle_id = [ord('a'), ord('e'), ord('i'), ord('o'), ord('u'), ord('y') ]
        len_pseudo = 1 + random.randint(1, 2) * 2
        rand_pseudo = ''
        is_voyelle_first = random.randint(0, 1) == 1
        for i in range(len_pseudo):  # loop for the amount of char whant.
            is_even = i % 2 == 1
            is_voyelle = is_even == is_voyelle_first
            if is_voyelle:  # pick random voyelle.
                char_id = random.randint(0, len(voyelle_id) - 1)
                rand_char = chr(char_id)
                rand_pseudo += rand_char
                continue
            char_id = voyelle_id[0]  # pick random consonne.
            while char_id in voyelle_id:
                char_id = random.randint(ord('a'), ord('z'))
            rand_char = chr(char_id)
            rand_pseudo += rand_char
        rand_pseudo = rand_pseudo[0].upper() + rand_pseudo[1:]  # upper the first char.
        return rand_pseudo


    @classmethod
    def resetCharacters(cls):
        CharactersManager.characters = []

    @classmethod
    def loadCharacters(cls, characters_pseudo: list[str]):
        for i in range(len(characters_pseudo)):
            pseudo = characters_pseudo[i]
            character = Characters(pseudo)

            # assign skills.
            match i:
                case 0:
                    character.skills.append(SkillFighting)
                #case 1:
                #    character.skills.append(str(Skills.Woodcutting))  # TODO: other skills.
                #case 2:
                #    character.skills.append(str(Skills.Mining))
                #case 3:
                #    character.skills.append(str(Skills.Weaponcrafting))
                #    character.skills.append(str(Skills.Gearcrafting))
                #    character.skills.append(str(Skills.Jewelrycrafting))
                #case 4:
                #    character.skills.append(str(Skills.Fighting))
                #    character.skills.append(str(Skills.Cooking))

            CharactersManager.characters.append(character)

