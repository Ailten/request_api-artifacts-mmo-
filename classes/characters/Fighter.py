from ..Characters import Characters
from ..primitives.Action import Actions
from ..primitives.V2 import V2

class Fighter(Characters):
    pos_to_fight: V2

    def __init__(self, pseudo: str, pos_to_fight: V2=V2(0,1)):
        super().__init__(pseudo)
        self.pos_to_fight = pos_to_fight

    
    # ---> 
        

    def getActionPackage(self) -> str|tuple[str,dict]:

        # if inventory full.
        if self.isInventoryFull():

            # if at bank.
            if self.pos == V2(4,1):

                # drop in bank.
                return (str(Actions.DropInBank), {
                    'item_to_drop': [ i for i in self.inventory if (
                        i['type'] == 'ressource' and
                        i['subtype'] == 'mob'
                    ) ]
                })
            
            # else, walk to bank.
            return (str(Actions.Move), { 'pos': V2(4,1) })
        
        # if hp under 30%.
        if self.getPurcentHp() < 0.3:

            # rest.
            return self._rest()
        
        # if at pos to fight.
        if self.pos == self.pos_to_fight:

            # fight.
            return str(Actions.Fight)

        # else, walk to pos to fight.
        return (str(Actions.Move), { 'pos': self.pos_to_fight})


    # ---> 
            

    def _rest(self) -> str|tuple[str,dict]:

        # TODO: eat, if can.

        # rest.
        return str(Actions.Rest)



        