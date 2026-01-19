import logging

from ..voice_events import VoiceEvent
from ..voice_event_store import VoiceEventStore


class TempVoiceEventStore(VoiceEventStore):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def push_event(self, event: VoiceEvent):
        self.logger.info(f'Event!!!!!!!!: {event}')


__all__ = [
    'TempVoiceEventStore'
]