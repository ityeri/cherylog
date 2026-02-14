import os
from abc import ABC, abstractmethod

import dotenv


class Config(ABC):
    @property
    @abstractmethod
    def bot_token(self) -> str: ...

    @property
    @abstractmethod
    def db_user(self) -> str: ...
    @property
    @abstractmethod
    def db_pw(self) -> str: ...
    @property
    @abstractmethod
    def db_host(self) -> str: ...
    @property
    @abstractmethod
    def db_port(self) -> int: ...
    @property
    @abstractmethod
    def db_name(self) -> str: ...


class DotenvConfig(Config):
    """
    The dotenv file format is in .env.example file
    """

    def __init__(self):
        dotenv.load_dotenv()
        self._bot_token: str = os.getenv('BOT_TOKEN')

        self._db_user: str = os.getenv('DB_USER')
        self._db_pw: str = os.getenv('DB_PW')
        self._db_host: str = os.getenv('DB_HOST')
        self._db_port: int = int(os.getenv('DB_PORT'))
        self._db_name: str = os.getenv('DB_NAME')

    @property
    def bot_token(self) -> str: return self._bot_token

    @property
    def db_user(self) -> str: return self._db_user
    @property
    def db_pw(self) -> str: return self._db_pw
    @property
    def db_host(self) -> str: return self._db_host
    @property
    def db_port(self) -> int: return self._db_port
    @property
    def db_name(self) -> str: return self._db_name