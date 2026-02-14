from discord.ext import commands
from sqlalchemy import select

from cherylog.common.database_utils import DatabaseManager
from .orm import VoiceEventRow
from ..voice_event_store import VoiceEventStore, VoiceEvent


class DatabaseVoiceEventStore(VoiceEventStore):
    def __init__(self, bot: commands.Bot, db_manager: DatabaseManager):
        self.bot: commands.Bot = bot
        self.db_manager: DatabaseManager = db_manager


    def obj_to_row(self, event: VoiceEvent) -> VoiceEventRow:
        return VoiceEventRow(
            event_type=event.event_type,
            user_id=event.member.id,
            guild_id=event.member.guild.id,
            at=event.at,

            before_channel_id=event.before_channel.id,
            after_channel_id=event.after_channel.id,

            deaf=event.deaf,
            mute=event.mute,
            self_deaf=event.self_deaf,
            self_mute=event.self_mute,

            stage_mute=event.stage_mute,

            stream=event.stream,
            video=event.video,
            afk=event.afk
        )

    def row_to_obj(self, event_row: VoiceEventRow) -> VoiceEvent:
        guild = self.bot.get_guild(event_row.guild_id)

        return VoiceEvent(
            event_type=event_row.event_type,
            member=guild.get_member(event_row.user_id),
            guild=guild,
            at=event_row.at,

            before_channel=self.bot.get_channel(event_row.before_channel_id),
            after_channel=self.bot.get_channel(event_row.after_channel_id),

            deaf=event_row.deaf,
            mute=event_row.mute,
            self_deaf=event_row.self_deaf,
            self_mute=event_row.self_mute,

            stage_mute=event_row.stage_mute,

            stream=event_row.stream,
            video=event_row.video,
            afk=event_row.afk
        )


    async def push_event(self, event: VoiceEvent):
        async with self.db_manager.get_async_session() as session:
            session.add(self.obj_to_row(event))
            await session.commit()

    async def get_all(self) -> list[VoiceEvent]:
        async with self.db_manager.get_async_session() as session:
            scalars = await session.scalars(select(VoiceEventRow))
            voice_event_rows = scalars.all()
            return list(map(self.row_to_obj, voice_event_rows))