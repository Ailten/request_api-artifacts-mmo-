from abc import ABC

class AbstractToken(ABC):
    the_token_init: 'AbstractToken|None' = None
    token: str

    # singleton.
    def __new__(cls):
        if cls.the_token_init is None:
            cls.the_token_init = super().__new__(cls)
            cls.the_token_init._readTokenEnv()
        return cls.the_token_init
    
    def _readTokenEnv(self):
        pass
    
    # cast string.
    def __str__(self) -> str:
        return self.token
