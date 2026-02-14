import sqlalchemy
from sqlalchemy import Column, BIGINT, BOOLEAN, Float
from sqlalchemy.orm import Mapped

from cherylog.common.database_utils import Base
from ..voice_event_store import VoiceEventType


class VoiceEventRow(Base):
    __tablename__ = 'voice_events'
    id: Mapped[int] = Column(BIGINT, primary_key=True, autoincrement=True)

    event_type: Mapped[VoiceEventType] = Column(
        sqlalchemy.Enum(VoiceEventType, name='voice_event_type', native_enum=False),
        nullable=False
    )
    user_id: Mapped[int] = Column(BIGINT, nullable=False)
    guild_id: Mapped[int] = Column(BIGINT, nullable=False)
    at: Mapped[float] = Column(Float, nullable=False) # f64

    before_channel_id: Mapped[int] = Column(BIGINT, nullable=True)
    after_channel_id: Mapped[int] = Column(BIGINT, nullable=True)

    deaf: Mapped[bool] = Column(BOOLEAN, nullable=False)
    mute: Mapped[bool] = Column(BOOLEAN, nullable=False)
    self_deaf: Mapped[bool] = Column(BOOLEAN, nullable=False)
    self_mute: Mapped[bool] = Column(BOOLEAN, nullable=False)

    stage_mute: Mapped[bool] = Column(BOOLEAN, nullable=False)

    stream: Mapped[bool] = Column(BOOLEAN, nullable=False)
    video: Mapped[bool] = Column(BOOLEAN, nullable=False)
    afk: Mapped[bool] = Column(BOOLEAN, nullable=False)