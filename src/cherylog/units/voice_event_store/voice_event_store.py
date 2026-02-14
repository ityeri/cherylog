from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

import discord


class VoiceEventType(Enum):
    CHANNEL_CHANGE = 'CHANNEL_CHANGE'

    DEAF = 'DEAF'
    MUTE = 'MUTE'

    SELF_DEAF = 'SELF_DEAF'
    SELF_MUTE = 'SELF_MUTE'

    STAGE_MUTE = 'STAGE_MUTE'

    STREAM = 'STREAM'
    VIDEO = 'VIDEO'

    AFK = 'AFK'

@dataclass
class VoiceEvent:
    event_type: VoiceEventType
    member: discord.Member
    guild: discord.Guild
    at: float # f64 unix timestamp seconds

    before_channel: discord.VoiceChannel | None
    after_channel: discord.VoiceChannel | None

    deaf: bool
    mute: bool
    self_deaf: bool
    self_mute: bool

    stage_mute: bool

    stream: bool
    video: bool
    afk: bool


class VoiceEventStore(ABC):
    @abstractmethod
    async def push_event(self, event: VoiceEvent): ...

    @abstractmethod
    async def get_all(self) -> list[VoiceEvent]: ...