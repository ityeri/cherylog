import discord
from discord.ext import commands
from sqlalchemy.ext.asyncio import AsyncSession

from cherylog.common.database_utils import DatabaseManager
from .orm import VoiceChannelRow, VoiceEventRow, VoiceEventType
from .. import voice_events
from ..voice_event_store import VoiceEventStore
from ..voice_events import VoiceEvent
from . import orm


class DatabaseVoiceEventStore(VoiceEventStore):
    def __init__(self, bot: commands.Bot, db_manager: DatabaseManager):
        self.bot: commands.Bot = bot
        self.db_manager: DatabaseManager = db_manager

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

    async def to_event_obj(self, event_row: VoiceEventRow) -> VoiceEvent:
        # if code works, affected_channels list must not be empty
        # discord py voice event system only works guild separateasdf
        guild = self.bot.get_guild(event_row.affected_channels[0].guild_id)

        if event_row.type == VoiceEventType.CHANNEL_CHANGE:
            return voice_events.ChannelChangeEvent(
                member=guild.get_member(event_row.member_id),
                affected_channels=[self.bot.get_channel(channel.channel_id) for channel in event_row.affected_channels],
                at=event_row.at,
                before=event_row. # TODO a shebal I forgot to add before and after property to orm.VoiceEventRow
            )


    async def push_event(self, event: VoiceEvent, state: discord.VoiceState):
        async with self.db_manager.get_async_session() as session:
            event_row = orm.VoiceEventRow(
                member_id=event.member.id,
                type=orm.get_event_type(event),
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

    async def get_all(self) -> list[VoiceEvent]:
        async with self.db_manager.get_async_session() as session:
