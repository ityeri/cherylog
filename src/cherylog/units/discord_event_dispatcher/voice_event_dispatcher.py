import logging
import time

import discord
from discord.ext import commands

from cherylog.units.voice_event_store import VoiceEventStore, VoiceEvent, VoiceEventType


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
        default_kwargs = {
            'member': member,
            'guild': member.guild,
            'at': time.time(),

            'before_channel': before.channel,
            'after_channel': before.channel,

            'deaf': before.deaf,
            'mute': before.mute,
            'self_deaf': before.self_deaf,
            'self_mute': before.self_mute,

            'stage_mute': before.suppress,

            'stream': before.self_stream,
            'video': before.self_video,
            'afk': before.afk
        }

        if before.channel != after.channel:
            default_kwargs = default_kwargs | {'after_channel': after.channel}
            await self.event_store.push_event(VoiceEvent(
                event_type=VoiceEventType.CHANNEL_CHANGE,
                **default_kwargs
            ))

        if before.deaf != after.deaf:
            default_kwargs = default_kwargs | {'deaf': after.deaf}
            await self.event_store.push_event(VoiceEvent(
                event_type=VoiceEventType.DEAF,
                **default_kwargs
            ))
        if before.mute != after.mute:
            default_kwargs = default_kwargs | {'mute': after.mute}
            await self.event_store.push_event(VoiceEvent(
                event_type=VoiceEventType.MUTE,
                **default_kwargs
            ))
        if before.self_deaf != after.self_deaf:
            default_kwargs = default_kwargs | {'self_deaf': after.self_deaf}
            await self.event_store.push_event(VoiceEvent(
                event_type=VoiceEventType.SELF_DEAF,
                **default_kwargs
            ))
        if before.self_mute != after.self_mute:
            default_kwargs = default_kwargs | {'self_mute': after.self_mute}
            await self.event_store.push_event(VoiceEvent(
                event_type=VoiceEventType.SELF_MUTE,
                **default_kwargs
            ))

        if before.suppress != after.suppress:
            default_kwargs = default_kwargs | {'stage_mute': after.suppress}
            await self.event_store.push_event(VoiceEvent(
                event_type=VoiceEventType.STAGE_MUTE,
                **default_kwargs
            ))

        if before.self_stream != after.self_stream:
            default_kwargs = default_kwargs | {'stream': after.self_stream}
            await self.event_store.push_event(VoiceEvent(
                event_type=VoiceEventType.STREAM,
                **default_kwargs
            ))
        if before.self_video != after.self_video:
            default_kwargs = default_kwargs | {'video': after.self_video}
            await self.event_store.push_event(VoiceEvent(
                event_type=VoiceEventType.VIDEO,
                **default_kwargs
            ))
        if before.afk != after.afk:
            default_kwargs = default_kwargs | {'afk': after.afk}
            await self.event_store.push_event(VoiceEvent(
                event_type=VoiceEventType.AFK,
                **default_kwargs
            ))