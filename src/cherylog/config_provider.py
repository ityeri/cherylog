import os
from abc import ABC, abstractmethod

import dotenv


class Config(ABC):
    @property
    @abstractmethod
    def bot_token(self) -> str: ...


class DotenvConfig(Config):
    def __init__(self):
        dotenv.load_dotenv()
        self._bot_token: str = os.getenv('BOT_TOKEN')

    @property
    def bot_token(self) -> str: return self._bot_token