from abc import ABC, abstractmethod
from dataclasses import dataclass

from discord import VoiceState, VoiceChannel


class VoiceEventStore(ABC):
    @abstractmethod
    def add_event(self, timestamp: float, state: VoiceState): ...

@dataclass
class VoiceEvent:
    channel: VoiceChannel | None

    deaf: bool
    mute: bool

    self_mute: bool
    self_deaf: bool

    self_stream: bool
    self_video: bool

    afk: bool

class JsonEventStore(VoiceEventStore):
    def __init__(self, filepath: str):
        self.filepath: str = filepath
        self.data

    def add_event(self, timestamp: float, state: VoiceState):
