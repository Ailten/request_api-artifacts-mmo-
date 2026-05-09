from enum import Enum

class CategoryEquipement(str, Enum):
    Weapon='weapon'
    Helmet='helmet'
    Shield='shield'
    BodyArmor='body_armor'
    Amulet='amulet'
    LegArmor='leg_armor'
    Boots='boots'
    Ring1='ring1'
    Ring2='ring2'

    def __str__(self):
        return super().__str__()