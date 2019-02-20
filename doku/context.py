import os
from doku.client import Client
from doku.config_manager import ConfigManager

class Context:
    client: Client
    config: ConfigManager
    editor: str

    def __init__(self):
        self.editor = os.environ.get('EDITOR', 'vim')
        self.config = ConfigManager()
        self.__new_client()

    def __new_client(self):
        info = self.config['connection']
        self.client = Client(
            info['domain'],
            info['username'],
            info['password'],
            ssl=info.get('ssl', True),
            basepath=info.get('path', '/')
        )
