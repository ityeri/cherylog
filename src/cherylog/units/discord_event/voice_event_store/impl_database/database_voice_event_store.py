import discord
from sqlalchemy.ext.asyncio import AsyncSession

from cherylog.common.database_utils import DatabaseManager
from .orm import VoiceChannelRow
from ..voice_event_store import VoiceEventStore
from ..voice_events import VoiceEvent
from . import orm


class DatabaseVoiceEventStore(VoiceEventStore):
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager: DatabaseManager = db_manager

    async def push_event(self, event: VoiceEvent, state: discord.VoiceState):
        async with self.db_manager.get_async_session() as session:
            event_row = orm.VoiceEventRow(
                member=event.member.id,
                type=orm.VoiceEventType.get_event_type(event),
                at=event.at,
                affected_channels=await self.get_channel_rows(session, event.affected_channels),

                deaf=state.deaf,
                mute=state.mute,

                self_deaf=state.self_deaf,
                self_mute=state.self_mute,

                stage_mute=state.suppress,

                stream=state.self_stream,
                video=state.self_video,

                afk=state.afk
            )

            session.add(event_row)
            await session.commit()

    async def get_channel_rows(
            self, session: AsyncSession, channels: list[discord.VoiceChannel]
    ) -> list[VoiceChannelRow]:
        rows = list()

        for voice_channel in channels:
            row = await session.get(VoiceChannelRow, voice_channel.id)

            if row is None:
                row = orm.VoiceChannelRow(
                    channel_id=voice_channel.id,
                    guild_id=voice_channel.guild.id,
                    events=[]
                )
                session.add(row)

            rows.append(row)

        await session.commit()

        return rows