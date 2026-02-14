from fastapi import FastAPI, APIRouter

from cherylog.units.voice_event_store import VoiceEventStore, VoiceEvent


class FastAPIServer:
    def __init__(self, event_store: VoiceEventStore):
        self.event_store: VoiceEventStore = event_store
        self.app: FastAPI = FastAPI()

    def init_routers(self):
        router = APIRouter()

        @router.get("/all")
        async def get_all() -> list[VoiceEvent]:
            # TODO
            return {}

        self.app.include_router(router)


__all__ = [
    "FastAPIServer"
]