from configparser import ConfigParser
from pathlib import Path
import os

class ConfigManager:
    __config: ConfigParser

    def __init__(self):
        self.__config = None

    def __load(self):
        filepath = os.path.join(Path.home(), '.doku.ini')

        self.__config = ConfigParser()
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f'File not found: {filepath}')
        self.__config.read(filepath)

    def __getitem__(self, key):
        if self.__config is None:
            self.__load()

        try:
            return self.__config[key]
        except KeyError:
            return None

    def get(self, section, key, default):
        try:
            return self.__config[section][key]
        except KeyError:
            return default

    def sections(self):
        if self.__config is None:
            self.__load()

        return self.__config.sections()
