import logging

import discord
from dependency_injector import containers
from dependency_injector.providers import Singleton, Object
from discord.ext import commands

from cherylog import config_provider
from cherylog.units.discord_event import VoiceEventDispatcher
from cherylog.units.discord_event import voice_event_store


class Container(containers.DeclarativeContainer):
    bot: Object[commands.Bot] = \
        Object(commands.Bot(command_prefix='/', intents=discord.Intents.all()))

    config: Singleton[config_provider.Config] = \
        Singleton(config_provider.DotenvConfig)

    log_handler: Object[logging.Handler] = \
        Object(logging.FileHandler(filename='latest.log', encoding='utf-8', mode='w'))

    voice_event_store: Singleton[voice_event_store.VoiceEventStore] = \
        Singleton(voice_event_store.impl_temp.TempVoiceEventStore)

    voice_event_dispatcher: Singleton[VoiceEventDispatcher] = \
        Singleton(VoiceEventDispatcher, bot=bot, event_store=voice_event_store)


class Bootstrapper:
    def __init__(self, container: Container):
        self.container: Container = container
        self.logger = logging.getLogger(self.__class__.__name__)
        self.bot: commands.Bot = container.bot()

    async def on_ready(self):
        self.logger.info('Bot started')
        self.logger.info(f'Login as {self.bot.user.name}')
        self.logger.info('Timings Reset')

    def run(self):
        print('Bootstrapper: Setup logging...')
        discord.utils.setup_logging()
        self.logger.info('If you can see it, logging setup is complete')

        self.bot.add_listener(self.on_ready)

        self.logger.info('Load voice event dispatcher...')
        self.container.voice_event_dispatcher()
        self.logger.info('Done')

        self.logger.info('Starting bot...')
        self.bot.run(
            token=self.container.config().bot_token,
            log_handler=self.container.log_handler(),
            log_level=logging.INFO,
            root_logger=True
        )