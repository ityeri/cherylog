from abc import ABC, abstractmethod

import discord

from .voice_events import VoiceEvent


class VoiceEventStore(ABC):
    @abstractmethod
    async def push_event(self, event: VoiceEvent, state: discord.VoiceState): ...

    @abstractmethod
    async def get_all(self) -> list[VoiceEvent]: ...