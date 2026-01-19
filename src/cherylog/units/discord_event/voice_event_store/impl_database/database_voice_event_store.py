from ..voice_event_store import VoiceEventStore
from ..voice_events import VoiceEvent


class DatabaseVoiceEventStore(VoiceEventStore):
    def push_event(self, event: VoiceEvent):
        pass