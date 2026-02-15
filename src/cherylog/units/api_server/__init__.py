from dataclasses import dataclass

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from cherylog.config_provider import Config
from cherylog.units.voice_event_store import VoiceEventStore, VoiceEvent, VoiceEventType


@dataclass
class VoiceEventScheme:
    event_type: VoiceEventType
    user_id: int
    guild_id: int
    at: float

    before_channel_id: int | None
    after_channel_id: int | None

    deaf: bool
    mute: bool
    self_deaf: bool
    self_mute: bool

    stage_mute: bool

    stream: bool
    video: bool
    afk: bool

def to_voice_event_scheme(event: VoiceEvent):
    return VoiceEventScheme(
        event_type=event.event_type,
        user_id=event.member.id,
        guild_id=event.guild.id,
        at=event.at,

        before_channel_id=event.before_channel.id if event.before_channel else None,
        after_channel_id=event.after_channel.id if event.after_channel else None,

        deaf=event.deaf,
        mute=event.mute,
        self_deaf=event.self_deaf,
        self_mute=event.self_mute,

        stage_mute=event.stage_mute,

        stream=event.stream,
        video=event.video,
        afk=event.afk
    )


class FastAPIServer:
    def __init__(self, config: Config, event_store: VoiceEventStore):
        self.event_store: VoiceEventStore = event_store
        self.config: Config = config
        self._app: FastAPI = FastAPI()

    def init(self):
        router = APIRouter(prefix='/api')

        @router.get("/all")
        async def get_all() -> list[VoiceEventScheme]:
            return list(map(to_voice_event_scheme, await self.event_store.get_all()))

        self._app.include_router(router)

        # TODO jung suck
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=False,
            allow_methods=["*"],
            allow_headers=["*"]
        )

    async def start(self):
        config = uvicorn.Config(
            self._app,
            host=self.config.api_host,
            port=self.config.api_port,
            log_config=None,
            loop='asyncio'
        )
        server = uvicorn.Server(config)
        await server.serve()


__all__ = [
    "FastAPIServer"
]