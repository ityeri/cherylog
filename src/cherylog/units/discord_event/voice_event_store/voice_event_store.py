from abc import ABC, abstractmethod

from .voice_events import VoiceEvent


class VoiceEventStore(ABC):
    @abstractmethod
    def push_event(self, event: VoiceEvent): ...