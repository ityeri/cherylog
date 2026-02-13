import enum
from typing import Type

import sqlalchemy
from sqlalchemy import Column, BIGINT, Table, ForeignKey, BOOLEAN, Float
from sqlalchemy.orm import Mapped, relationship

from cherylog.common.database_utils import Base
from cherylog.units.voice_event_store import voice_events

voice_event_voice_channel = Table(
    'voice_event_voice_channel',
    Base.metadata,
    Column('voice_event_id', ForeignKey('voice_events.id'), primary_key=True),
    Column('voice_channel_id', ForeignKey('voice_channels.channel_id'), primary_key=True)
)

class VoiceEventType(enum.Enum):
    _ignore_ = ['_event_type_map']

    CHANNEL_CHANGE = 'CHANNEL_CHANGE'

    DEAF = 'DEAF'
    MUTE = 'MUTE'

    SELF_DEAF = 'SELF_DEAF'
    SELF_MUTE = 'SELF_MUTE'

    STAGE_MUTE = 'STAGE_MUTE'

    STREAM = 'STREAM'
    VIDEO = 'VIDEO'

    AFK = 'AFK'

_event_type_map: dict[Type[voice_events.VoiceEvent], VoiceEventType] = {
    voice_events.ChannelChangeEvent: VoiceEventType.CHANNEL_CHANGE,

    voice_events.DeafEvent: VoiceEventType.DEAF,
    voice_events.MuteEvent: VoiceEventType.MUTE,

    voice_events.SelfDeafEvent: VoiceEventType.SELF_DEAF,
    voice_events.SelfMuteEvent: VoiceEventType.SELF_MUTE,

    voice_events.StageMuteEvent: VoiceEventType.STAGE_MUTE,

    voice_events.StreamEvent: VoiceEventType.STREAM,
    voice_events.VideoEvent: VoiceEventType.VIDEO,

    voice_events.AfkSwitchEvent: VoiceEventType.AFK
}

def get_event_type(voice_event: voice_events.VoiceEvent) -> VoiceEventType:
    return _event_type_map[voice_event.__class__]


class VoiceEventRow(Base):
    __tablename__ = 'voice_events'
    id: Mapped[int] = Column(BIGINT, primary_key=True, autoincrement=True)
    member_id: Mapped[int] = Column(BIGINT, nullable=False)
    type: Mapped[VoiceEventType] = Column(
        sqlalchemy.Enum(VoiceEventType, name='voice_event_type', native_enum=False),
        nullable=False
    )
    at: Mapped[float] = Column(Float, nullable=False) # f64
    affected_channels: Mapped[list[VoiceChannelRow]] = relationship(
        secondary=voice_event_voice_channel,
        back_populates='events'
    )

    # TODO
    before: Mapped[VoiceChannelRow] = ...
    after: Mapped[VoiceChannelRow] = ...

    deaf: Mapped[bool] = Column(BOOLEAN, nullable=False)
    mute: Mapped[bool] = Column(BOOLEAN, nullable=False)

    self_deaf: Mapped[bool] = Column(BOOLEAN, nullable=False)
    self_mute: Mapped[bool] = Column(BOOLEAN, nullable=False)

    stage_mute: Mapped[bool] = Column(BOOLEAN, nullable=False)

    stream: Mapped[bool] = Column(BOOLEAN, nullable=False)
    video: Mapped[bool] = Column(BOOLEAN, nullable=False)

    afk: Mapped[bool] = Column(BOOLEAN, nullable=False)

class VoiceChannelRow(Base):
    __tablename__ = 'voice_channels'
    channel_id: Mapped[int] = Column(BIGINT, primary_key=True, unique=True)
    guild_id: Mapped[int] = Column(BIGINT, nullable=False)
    events: Mapped[list[VoiceEventRow]] = relationship(
        secondary=voice_event_voice_channel,
        back_populates='affected_channels'
    )