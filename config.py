import json
from typing import Dict


class Config:
    CONFIG_PATH = "config.json"
    _data: Dict

    def __init__(self):
        self._load_config()

    def get(self, name: str) -> any:
        return self._data.get(name)

    def set(self, name: str, data: any):
        self._data[name] = data

    def save(self):
        with open(self.CONFIG_PATH, 'w') as file:
            json.dump(self._data, fp=file)

    def _load_config(self):
        with open(self.CONFIG_PATH, 'r') as file:
            self._data = json.load(fp=file)
