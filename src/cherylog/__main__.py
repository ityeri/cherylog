import logging
import os
import time

import discord
from discord.ext import commands
import dotenv

from cherylog.voice_event_store import VoiceEventStore, ChannelChangeEvent, DeafEvent, MuteEvent, SelfDeafEvent, \
    SelfMuteEvent, StageMuteEvent, StreamEvent, VideoEvent, AfkSwitchEvent, VoiceEventStoreImpl

dotenv.load_dotenv()

bot: commands.Bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
log_handler = logging.FileHandler(filename='latest.log', encoding='utf-8', mode='w')

event_store: VoiceEventStore = VoiceEventStoreImpl()

@bot.event
async def on_ready():
    logging.info('Ready!')
    logging.info(f'Login as {bot.user.name}')
    logging.info('Timings Reset')

@bot.event
async def on_voice_state_update(
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState
):
    at = time.time()
    affected_channels = list()

    if before.channel is not None:
        affected_channels.append(before.channel)
    if after.channel is not None and after.channel not in affected_channels:
        affected_channels.append(after.channel)

    if before.channel != after.channel:
        event_store.push_event(
            ChannelChangeEvent(member, affected_channels, at, before.channel, after.channel)
        )
    if before.deaf != after.deaf:
        event_store.push_event(
            DeafEvent(member, affected_channels, at, after.deaf)
        )
    if before.mute != after.mute:
        event_store.push_event(
            MuteEvent(member, affected_channels, at, after.mute)
        )
    if before.self_deaf != after.self_deaf:
        event_store.push_event(
            SelfDeafEvent(member, affected_channels, at, after.self_deaf)
        )
    if before.self_mute != after.self_mute:
        event_store.push_event(
            SelfMuteEvent(member, affected_channels, at, after.self_mute)
        )
    if before.suppress != after.suppress:
        event_store.push_event(
            StageMuteEvent(member, affected_channels, at, after.suppress)
        )
    if before.self_stream != after.self_stream:
        event_store.push_event(
            StreamEvent(member, affected_channels, at, after.self_stream)
        )
    if before.self_video != after.self_video:
        event_store.push_event(
            VideoEvent(member, affected_channels, at, after.self_video)
        )
    if before.afk != after.afk:
        event_store.push_event(
            AfkSwitchEvent(member, affected_channels, at, after.afk)
        )

discord.utils.setup_logging()
bot.run(
    os.getenv("BOT_TOKEN"),
    log_handler=log_handler,
    log_level=logging.INFO,
    root_logger=True
)