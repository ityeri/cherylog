import logging
import time

import discord
from discord.ext import commands

from .voice_event_store import VoiceEventStore
from .voice_event_store import voice_events


class VoiceEventDispatcher:
    def __init__(self, bot: commands.Bot, event_store: VoiceEventStore):
        self.bot: commands.Bot = bot
        self.event_store: VoiceEventStore = event_store
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

        self.bot.add_listener(self.on_voice_state_update)

    async def on_voice_state_update(
            self,
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
            self.event_store.push_event(
                voice_events.ChannelChangeEvent(member, affected_channels, at, before.channel, after.channel)
            )
        if before.deaf != after.deaf:
            self.event_store.push_event(
                voice_events.DeafEvent(member, affected_channels, at, after.deaf)
            )
        if before.mute != after.mute:
            self.event_store.push_event(
                voice_events.MuteEvent(member, affected_channels, at, after.mute)
            )
        if before.self_deaf != after.self_deaf:
            self.event_store.push_event(
                voice_events.SelfDeafEvent(member, affected_channels, at, after.self_deaf)
            )
        if before.self_mute != after.self_mute:
            self.event_store.push_event(
                voice_events.SelfMuteEvent(member, affected_channels, at, after.self_mute)
            )
        if before.suppress != after.suppress:
            self.event_store.push_event(
                voice_events.StageMuteEvent(member, affected_channels, at, after.suppress)
            )
        if before.self_stream != after.self_stream:
            self.event_store.push_event(
                voice_events.StreamEvent(member, affected_channels, at, after.self_stream)
            )
        if before.self_video != after.self_video:
            self.event_store.push_event(
                voice_events.VideoEvent(member, affected_channels, at, after.self_video)
            )
        if before.afk != after.afk:
            self.event_store.push_event(
                voice_events.AfkSwitchEvent(member, affected_channels, at, after.afk)
            )