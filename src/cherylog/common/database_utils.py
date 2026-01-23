import logging
from abc import ABC, abstractmethod

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

from cherylog.config_provider import Config


class Base(DeclarativeBase): ...


class DatabaseManager(ABC):
    @abstractmethod
    def init(self): ...
    @abstractmethod
    def get_session(self) -> Session | None: ...
    @abstractmethod
    def get_async_session(self) -> AsyncSession | None: ...

class AsyncPostgresDatabaseManager(DatabaseManager):
    def __init__(self, config: Config):
        self.config: Config = config

        self.engine: Engine | None = None
        self.async_engine: AsyncEngine | None = None

        self.session_factory: sessionmaker[Session] | None = sessionmaker()
        self.async_session_factory: async_sessionmaker[AsyncSession] | None = async_sessionmaker()

        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

    def init(self):
        url_back_part = (
            f'{self.config.db_user}:{self.config.db_pw}@'
            f'{self.config.db_host}:{self.config.db_port}/{self.config.db_name}'
        )
        url = f'postgresql+psycopg2://' + url_back_part
        async_url = f'postgresql+asyncpg://' + url_back_part

        self.engine = create_engine(url)
        self.async_engine = create_async_engine(async_url)
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        return self.session_factory(bind=self.engine)
    def get_async_session(self) -> AsyncSession:
        return self.async_session_factory(bind=self.async_engine)