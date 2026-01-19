import logging
from abc import ABC, abstractmethod
import discord
from discord import VoiceChannel


class VoiceEvent(ABC):
    @property
    @abstractmethod
    def member(self) -> discord.Member: ...

    @property
    @abstractmethod
    def affected_channels(self) -> list[VoiceChannel]: ...

    @property
    @abstractmethod
    def at(self) -> float: ...


class VoiceEventStore(ABC):
    @abstractmethod
    def push_event(self, event: VoiceEvent): ...


class ChannelChangeEvent(VoiceEvent):
    def __init__(
            self, member: discord.Member, affected_channels: list[VoiceChannel], at: float,
            before: VoiceChannel | None, after: VoiceChannel | None
    ):
        self._member: discord.Member = member
        self._affected_channels: list[VoiceChannel] = affected_channels
        self._at: float = at

        self.before: VoiceChannel | None = before
        self.after: VoiceChannel | None = after

    @property
    def member(self) -> discord.Member: return self._member

    @property
    def affected_channels(self) -> list[VoiceChannel]: return self._affected_channels

    @property
    def at(self) -> float: return self._at

class DeafEvent(VoiceEvent):
    def __init__(
            self, member: discord.Member, affected_channels: list[VoiceChannel], at: float,
            deaf: bool
    ):
        self._member: discord.Member = member
        self._affected_channels: list[VoiceChannel] = affected_channels
        self._at: float = at

        self.deaf: bool = deaf

    @property
    def member(self) -> discord.Member: return self._member

    @property
    def affected_channels(self) -> list[VoiceChannel]: return self._affected_channels

    @property
    def at(self) -> float: return self._at

class MuteEvent(VoiceEvent):
    def __init__(
            self, member: discord.Member, affected_channels: list[VoiceChannel], at: float,
            mute: bool
    ):
        self._member: discord.Member = member
        self._affected_channels: list[VoiceChannel] = affected_channels
        self._at: float = at

        self.mute: bool = mute

    @property
    def member(self) -> discord.Member: return self._member

    @property
    def affected_channels(self) -> list[VoiceChannel]: return self._affected_channels

    @property
    def at(self) -> float: return self._at

class SelfDeafEvent(VoiceEvent):
    def __init__(
            self, member: discord.Member, affected_channels: list[VoiceChannel], at: float,
            deaf: bool
    ):
        self._member: discord.Member = member
        self._affected_channels: list[VoiceChannel] = affected_channels
        self._at: float = at

        self.deaf: bool = deaf

    @property
    def member(self) -> discord.Member: return self._member

    @property
    def affected_channels(self) -> list[VoiceChannel]: return self._affected_channels

    @property
    def at(self) -> float: return self._at

class SelfMuteEvent(VoiceEvent):
    def __init__(
            self, member: discord.Member, affected_channels: list[VoiceChannel], at: float,
            mute: bool
    ):
        self._member: discord.Member = member
        self._affected_channels: list[VoiceChannel] = affected_channels
        self._at: float = at

        self.mute: bool = mute

    @property
    def member(self) -> discord.Member: return self._member

    @property
    def affected_channels(self) -> list[VoiceChannel]: return self._affected_channels

    @property
    def at(self) -> float: return self._at

class StageMuteEvent(VoiceEvent):
    def __init__(
            self, member: discord.Member, affected_channels: list[VoiceChannel], at: float,
            mute: bool
    ):
        self._member: discord.Member = member
        self._affected_channels: list[VoiceChannel] = affected_channels
        self._at: float = at

        self.mute: bool = mute

    @property
    def member(self) -> discord.Member: return self._member

    @property
    def affected_channels(self) -> list[VoiceChannel]: return self._affected_channels

    @property
    def at(self) -> float: return self._at

class StreamEvent(VoiceEvent):
    def __init__(
            self, member: discord.Member, affected_channels: list[VoiceChannel], at: float,
            is_stream_on: bool
    ):
        self._member: discord.Member = member
        self._affected_channels: list[VoiceChannel] = affected_channels
        self._at: float = at

        self.is_stream_on: bool = is_stream_on

    @property
    def member(self) -> discord.Member: return self._member

    @property
    def affected_channels(self) -> list[VoiceChannel]: return self._affected_channels

    @property
    def at(self) -> float: return self._at

class VideoEvent(VoiceEvent):
    def __init__(
            self, member: discord.Member, affected_channels: list[VoiceChannel], at: float,
            is_video_on: bool
    ):
        self._member: discord.Member = member
        self._affected_channels: list[VoiceChannel] = affected_channels
        self._at: float = at

        self.is_video_on: bool = is_video_on

    @property
    def member(self) -> discord.Member: return self._member

    @property
    def affected_channels(self) -> list[VoiceChannel]: return self._affected_channels

    @property
    def at(self) -> float: return self._at

class AfkSwitchEvent(VoiceEvent):
    def __init__(
            self, member: discord.Member, affected_channels: list[VoiceChannel], at: float,
            afk: bool
    ):
        self._member: discord.Member = member
        self._affected_channels: list[VoiceChannel] = affected_channels
        self._at: float = at

        self.afk: bool = afk

    @property
    def member(self) -> discord.Member: return self._member

    @property
    def affected_channels(self) -> list[VoiceChannel]: return self._affected_channels

    @property
    def at(self) -> float: return self._at


class VoiceEventStoreImpl(VoiceEventStore):
    def __init__(self):
        self.events: dict[float, VoiceEvent] = dict()

    def push_event(self, event: VoiceEvent):
        self.events[event.at] = event

        logging.info(f'Event triggered: {event.__class__.__name__}')
        logging.info(f'Member: {event.member}')
        logging.info(f'Affected channels: ')

        for channel in event.affected_channels:
            logging.info(f' |  {channel.name}')

        logging.info(f'Detailed: {event}')