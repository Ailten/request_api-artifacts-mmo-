import os
from dotenv import load_dotenv
from .AbstractToken import AbstractToken

class Token(AbstractToken):
    
    def _readTokenEnv(self, path_file_env: str='.env'):
        load_dotenv(dotenv_path=path_file_env)
        self.token = os.getenv("TOKEN")
