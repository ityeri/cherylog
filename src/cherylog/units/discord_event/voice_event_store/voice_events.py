from abc import ABC, abstractmethod

import discord


class VoiceEvent(ABC):
    @property
    @abstractmethod
    def member(self) -> discord.Member: ...

    @property
    @abstractmethod
    def affected_channels(self) -> list[discord.VoiceChannel]: ...

    @property
    @abstractmethod
    def at(self) -> float: ... # f64


class ChannelChangeEvent(VoiceEvent):
    def __init__(
            self, member: discord.Member, affected_channels: list[discord.VoiceChannel], at: float,
            before: discord.VoiceChannel | None, after: discord.VoiceChannel | None
    ):
        self._member: discord.Member = member
        self._affected_channels: list[discord.VoiceChannel] = affected_channels
        self._at: float = at

        self.before: discord.VoiceChannel | None = before
        self.after: discord.VoiceChannel | None = after

    @property
    def member(self) -> discord.Member: return self._member

    @property
    def affected_channels(self) -> list[discord.VoiceChannel]: return self._affected_channels

    @property
    def at(self) -> float: return self._at


class DeafEvent(VoiceEvent):
    def __init__(
            self, member: discord.Member, affected_channels: list[discord.VoiceChannel], at: float,
            deaf: bool
    ):
        self._member: discord.Member = member
        self._affected_channels: list[discord.VoiceChannel] = affected_channels
        self._at: float = at

        self.deaf: bool = deaf

    @property
    def member(self) -> discord.Member: return self._member

    @property
    def affected_channels(self) -> list[discord.VoiceChannel]: return self._affected_channels

    @property
    def at(self) -> float: return self._at

class MuteEvent(VoiceEvent):
    def __init__(
            self, member: discord.Member, affected_channels: list[discord.VoiceChannel], at: float,
            mute: bool
    ):
        self._member: discord.Member = member
        self._affected_channels: list[discord.VoiceChannel] = affected_channels
        self._at: float = at

        self.mute: bool = mute

    @property
    def member(self) -> discord.Member: return self._member

    @property
    def affected_channels(self) -> list[discord.VoiceChannel]: return self._affected_channels

    @property
    def at(self) -> float: return self._at


class SelfDeafEvent(VoiceEvent):
    def __init__(
            self, member: discord.Member, affected_channels: list[discord.VoiceChannel], at: float,
            deaf: bool
    ):
        self._member: discord.Member = member
        self._affected_channels: list[discord.VoiceChannel] = affected_channels
        self._at: float = at

        self.deaf: bool = deaf

    @property
    def member(self) -> discord.Member: return self._member

    @property
    def affected_channels(self) -> list[discord.VoiceChannel]: return self._affected_channels

    @property
    def at(self) -> float: return self._at

class SelfMuteEvent(VoiceEvent):
    def __init__(
            self, member: discord.Member, affected_channels: list[discord.VoiceChannel], at: float,
            mute: bool
    ):
        self._member: discord.Member = member
        self._affected_channels: list[discord.VoiceChannel] = affected_channels
        self._at: float = at

        self.mute: bool = mute

    @property
    def member(self) -> discord.Member: return self._member

    @property
    def affected_channels(self) -> list[discord.VoiceChannel]: return self._affected_channels

    @property
    def at(self) -> float: return self._at


class StageMuteEvent(VoiceEvent):
    def __init__(
            self, member: discord.Member, affected_channels: list[discord.VoiceChannel], at: float,
            mute: bool
    ):
        self._member: discord.Member = member
        self._affected_channels: list[discord.VoiceChannel] = affected_channels
        self._at: float = at

        self.mute: bool = mute

    @property
    def member(self) -> discord.Member: return self._member

    @property
    def affected_channels(self) -> list[discord.VoiceChannel]: return self._affected_channels

    @property
    def at(self) -> float: return self._at


class StreamEvent(VoiceEvent):
    def __init__(
            self, member: discord.Member, affected_channels: list[discord.VoiceChannel], at: float,
            is_stream_on: bool
    ):
        self._member: discord.Member = member
        self._affected_channels: list[discord.VoiceChannel] = affected_channels
        self._at: float = at

        self.is_stream_on: bool = is_stream_on

    @property
    def member(self) -> discord.Member: return self._member

    @property
    def affected_channels(self) -> list[discord.VoiceChannel]: return self._affected_channels

    @property
    def at(self) -> float: return self._at

class VideoEvent(VoiceEvent):
    def __init__(
            self, member: discord.Member, affected_channels: list[discord.VoiceChannel], at: float,
            is_video_on: bool
    ):
        self._member: discord.Member = member
        self._affected_channels: list[discord.VoiceChannel] = affected_channels
        self._at: float = at

        self.is_video_on: bool = is_video_on

    @property
    def member(self) -> discord.Member: return self._member

    @property
    def affected_channels(self) -> list[discord.VoiceChannel]: return self._affected_channels

    @property
    def at(self) -> float: return self._at


class AfkSwitchEvent(VoiceEvent):
    def __init__(
            self, member: discord.Member, affected_channels: list[discord.VoiceChannel], at: float,
            afk: bool
    ):
        self._member: discord.Member = member
        self._affected_channels: list[discord.VoiceChannel] = affected_channels
        self._at: float = at

        self.afk: bool = afk

    @property
    def member(self) -> discord.Member: return self._member

    @property
    def affected_channels(self) -> list[discord.VoiceChannel]: return self._affected_channels

    @property
    def at(self) -> float: return self._at