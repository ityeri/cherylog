import asyncio
import logging
from logging import root
from math import trunc

import discord
from dependency_injector import containers
from dependency_injector.providers import Singleton, Object
from discord.ext import commands

import cherylog.log_formatter
from cherylog import config_provider
from cherylog.common import database_utils
from cherylog.units import voice_event_store
from cherylog.units.api_server import FastAPIServer
from cherylog.units.discord_event_dispatcher import VoiceEventDispatcher


class Container(containers.DeclarativeContainer):
    bot: Object[commands.Bot] = \
        Object(commands.Bot(command_prefix='/', intents=discord.Intents.all()))

    config: Singleton[config_provider.Config] = \
        Singleton(config_provider.DotenvConfig)

    database_manager: Singleton[database_utils.DatabaseManager] = \
        Singleton(database_utils.AsyncPostgresDatabaseManager, config=config)

    voice_event_store: Singleton[voice_event_store.VoiceEventStore] = \
        Singleton(voice_event_store.impl_database.DatabaseVoiceEventStore, bot=bot, db_manager=database_manager)

    voice_event_dispatcher: Singleton[VoiceEventDispatcher] = \
        Singleton(VoiceEventDispatcher, bot=bot, event_store=voice_event_store)

    api_server = Singleton(FastAPIServer, config=config, event_store=voice_event_store)


class Bootstrapper:
    def __init__(self, container: Container):
        self.container: Container = container
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        self.bot: commands.Bot = container.bot()

    async def on_ready(self):
        self.logger.info('Bot ready')
        self.logger.info(f'Login as {self.bot.user.name}')
        self.logger.info('Timings Reset')

    async def start(self):
        print('Bootstrapper: Setup logging...')
        root_logger = logging.getLogger()

        file_handler = logging.FileHandler(filename='latest.log', encoding='utf-8', mode='w')
        file_handler.setFormatter(cherylog.log_formatter.ColourFormatter())
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(cherylog.log_formatter.ColourFormatter())

        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(stream_handler)

        self.logger.info('If you can see it, logging setup is complete')

        self.bot.add_listener(self.on_ready)

        self.logger.info('Load voice event dispatcher...')
        self.container.voice_event_dispatcher()
        self.logger.info('Done')

        self.logger.info('Initialize database...')
        self.container.database_manager().init()
        self.logger.info('Done')

        self.logger.info('Starting api sever...')
        api_server = self.container.api_server()
        api_server.init()
        api_server_task = asyncio.create_task(api_server.start())
        self.logger.info('Done')

        self.logger.info('Starting bot...')
        bot_task = asyncio.create_task(self.bot.start(token=self.container.config().bot_token))
        self.logger.info('Done')

        self.logger.info('Bootstrapping is complete! now you just waiting for actual log with delicious ramyeon')

        await api_server_task
        await bot_task

    def run(self):
        asyncio.run(self.start())