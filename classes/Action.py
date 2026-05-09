from enum import Enum

class Action(str, Enum):
    Move='move'
    Fight='fight'
    Rest='rest'
    Gathering='gathering'
    Unequip='unequip'
    Crafting='crafting'
    Equip='equip'
    DropInventoryInBanque='bank/deposit/item'
    ChangeAction='change_action'  # special case.
    DoNothing='nothing'  # special case.

    # cast string.
    def __str__(self) -> str:
        return super().__str__()