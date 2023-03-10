"""
This type stub file was generated by pyright.
"""

import typing as t

from abc import ABC, abstractmethod
from enum import Enum
from .filters import Filter
from .client import Client
from .node import Node

"""
MIT License

Copyright (c) 2017-present Devoxin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

_SelfT = t.TypeVar('_SelfT')
_ClsT = t.TypeVar('_ClsT')

BareAudioTrackDataType = t.Mapping[
    t.Literal['track', 'info'], t.Union[str, AudioTrackInfoDataType]
]
AudioTrackInfoDataType = t.Mapping[
    t.Literal[
        'identifier',
        'isSeekable',
        'author',
        'length',
        'isStream',
        'title',
        'uri',
        'position',
        'sourceName',
    ],
    t.Union[str, int, bool],
]
AudioTrackDataType = BareAudioTrackDataType | AudioTrackInfoDataType
ExtraAudioTrackDataType = t.Mapping[t.Any, t.Any]
PlaylistInfoMappingType = t.Mapping[
    t.Literal['name', 'selectedTrack'], t.Union[str, int]
]
LoadResultMappingType = t.Mapping[
    t.Literal['loadType', 'playlistInfo', 'tracks'],
    t.Union[str, PlaylistInfoMappingType, t.Sequence[AudioTrackDataType]],
]
BandsType = t.List[t.Tuple[int, float]]
PluginMappingType = t.Mapping[t.Any, t.Any]

class AudioTrack:
    """Represents an AudioTrack.

    Parameters
    ----------
    data: Union[:class:`dict`, :class:`AudioTrack`]
        The data to initialise an AudioTrack from.
    requester: :class:`any`
        The requester of the track.
    extra: :class:`dict`
        Any extra information to store in this AudioTrack."""

    track: t.Optional[str]
    """The base64-encoded string representing a Lavalink-readable AudioTrack.
    
    This is marked optional as it could be None when it's not set by a custom :class:`Source`, which is expected behaviour when the subclass is a :class:`DeferredAudioTrack`."""
    identifier: str
    """The track's id. For example, a youtube track's identifier will look like dQw4w9WgXcQ."""
    is_seekable: bool
    """Whether the track supports seeking."""
    author: str
    """The track's uploader."""
    duration: int
    """The duration of the track, in milliseconds."""
    stream: bool
    """Whether the track is a live-stream."""
    title: str
    """The title of the track."""
    uri: str
    """The full URL of track."""
    position: int
    """The playback position of the track, in milliseconds. This is a read-only property; setting it won't have any effect."""
    source_name: str
    """The name of the source that this track was created by."""
    extra: ExtraAudioTrackDataType
    """ Any extra properties given to this AudioTrack will be stored here."""

    def __init__(
        self,
        data: t.Union[AudioTrackDataType, AudioTrack],
        requester: int,
        **extra: ExtraAudioTrackDataType,
    ) -> None: ...
    # def __getitem__(self, name): ...
    @property
    def requester(self) -> int: ...
    @requester.setter
    def requester(self, requester: int) -> None: ...

class DeferredAudioTrack(ABC, AudioTrack):
    """
    Similar to an :class:`AudioTrack`, however this track only stores metadata up until it's
    played, at which time :func:`load` is called to retrieve a base64 string which is then used for playing.

    Note
    ----
    For implementation: The ``track`` field need not be populated as this is done later via
    the :func:`load` method. You can optionally set ``self.track`` to the result of :func:`load`
    during implementation, as a means of caching the base64 string to avoid fetching it again later.
    This should serve the purpose of speeding up subsequent play calls in the event of repeat being enabled,
    for example.
    """

    @abstractmethod
    async def load(self, client: Client) -> str:
        """|coro|

        Retrieves a base64 string that's playable by Lavalink.
        For example, you can use this method to search Lavalink for an identical track from other sources,
        which you can then use the base64 string of to play the track on Lavalink.

        Parameters
        ----------
        client: :class:`Client`
            This will be an instance of the Lavalink client 'linked' to this track.

        Returns
        -------
        :class:`str`
            A Lavalink-compatible base64 string containing encoded track metadata.
        """
        ...

class LoadType(Enum):
    TRACK = ...
    PLAYLIST = ...
    SEARCH = ...
    NO_MATCHES = ...
    LOAD_FAILED = ...
    def __eq__(self: _SelfT, other: _SelfT) -> bool: ...
    @classmethod
    def from_str(cls: _ClsT, other: str) -> _ClsT: ...

class PlaylistInfo:
    name: str
    """The name of the playlist."""
    selected_track: int
    """The index of the selected/highlighted track.

    This will be -1 if there is no selected track."""

    def __init__(self, name: str, selected_track: int = ...) -> None: ...
    # def __getitem__(self, k): ...
    @classmethod
    def from_dict(cls: _ClsT, mapping: PlaylistInfoMappingType) -> _ClsT: ...
    @classmethod
    def none(cls: _ClsT) -> _ClsT: ...
    # def __repr__(self): ...

class LoadResult:
    load_type: LoadType
    """The load type of this result."""
    tracks: t.List[t.Union[AudioTrack, DeferredAudioTrack]]
    """The tracks in this result."""
    playlist_info: PlaylistInfo
    """The playlist metadata for this result.
    
    The :class:`PlaylistInfo` could contain empty/false data if the :class:`LoadType`is not :enum:`LoadType.PLAYLIST`."""

    def __init__(
        self,
        load_type: LoadType,
        tracks: t.List[t.Union[AudioTrack, DeferredAudioTrack]],
        playlist_info: t.Optional[PlaylistInfo] = ...,
    ) -> None: ...
    # def __getitem__(self, k): ...
    @classmethod
    def from_dict(cls: _ClsT, mapping: LoadResultMappingType) -> _ClsT: ...
    # def __repr__(self): ...

class Source(ABC):
    name: str

    def __init__(self, name: str) -> None: ...
    def __eq__(self: _SelfT, other: _SelfT) -> bool: ...
    def __hash__(self) -> int: ...
    @abstractmethod
    async def load_item(self, client: Client, query: str) -> t.Optional[LoadResult]:
        """|coro|

        Loads a track with the given query.

        Parameters
        ----------
        client: :class:`Client`
            The Lavalink client. This could be useful for performing a Lavalink search
            for an identical track from other sources, if needed.
        query: :class:`str`
            The search query that was provided.

        Returns
        -------
        Optional[:class:`LoadResult`]
            A LoadResult, or None if there were no matches for the provided query.
        """
        ...
    # def __repr__(self): ...

class BasePlayer(ABC):
    """Represents the BasePlayer all players must be inherited from."""

    guild_id: int
    """The guild id of the player."""
    node: Node
    """The node that the player is connected to."""
    channel_id: t.Optional[int]
    """The ID of the voice channel the player is connected to. This could be None if the player isn't connected."""

    def __init__(self, guild_id: int, node: Node) -> None: ...
    async def play_track(
        self,
        track: str,
        start_time: t.Optional[int] = ...,
        end_time: t.Optional[int] = ...,
        no_replace: t.Optional[bool] = ...,
        volume: t.Optional[int] = ...,
        pause: t.Optional[bool] = ...,
    ) -> None:
        """|coro|

        Plays the given track.

        Parameters
        ----------
        track: :class:`str`
            The track to play. This must be the base64 string from a track.
        start_time: Optional[:class:`int`]
            The number of milliseconds to offset the track by.
            If left unspecified or ``None`` is provided, the track will start from the beginning.
        end_time: Optional[:class:`int`]
            The position at which the track should stop playing.
            This is an absolute position, so if you want the track to stop at 1 minute, you would pass 60000.
            The default behaviour is to play until no more data is received from the remote server.
            If left unspecified or ``None`` is provided, the default behaviour is exhibited.
        no_replace: Optional[:class:`bool`]
            If set to true, operation will be ignored if a track is already playing or paused.
            The default behaviour is to always replace.
            If left unspecified or None is provided, the default behaviour is exhibited.
        volume: Optional[:class:`int`]
            The initial volume to set. This is useful for changing the volume between tracks etc.
            If left unspecified or ``None`` is provided, the volume will remain at its current setting.
        pause: Optional[:class:`bool`]
            Whether to immediately pause the track after loading it.
            The default behaviour is to never pause.
            If left unspecified or ``None`` is provided, the default behaviour is exhibited.
        """
        ...
    def cleanup(self) -> None: ...
    async def destroy(self) -> None:
        """|coro|

        Destroys the current player instance.

        Shortcut for :func:`PlayerManager.destroy`.
        """
        ...
    @abstractmethod
    async def node_unavailable(self) -> None:
        """|coro|

        Called when a player's node becomes unavailable.
        Useful for changing player state before it's moved to another node.
        """
        ...
    @abstractmethod
    async def change_node(self, node: Node) -> None:
        """|coro|

        Called when a node change is requested for the current player instance.

        Parameters
        ----------
        node: :class:`Node`
            The new node to switch to.
        """
        ...

class DefaultPlayer(BasePlayer):
    """
    The player that Lavalink.py uses by default.

    This should be sufficient for most use-cases.

    Attributes
    ----------
    LOOP_NONE: :class:`int`
        Class attribute. Disables looping entirely.
    LOOP_SINGLE: :class:`int`
        Class attribute. Enables looping for a single (usually currently playing) track only.
    LOOP_QUEUE: :class:`int`
        Class attribute. Enables looping for the entire queue. When a track finishes playing, it'll be added to the end of the queue.
    guild_id: :class:`int`
        The guild id of the player.
    node: :class:`Node`
        The node that the player is connected to.
    paused: :class:`bool`
        Whether or not a player is paused.
    position_timestamp: :class:`int`
        Returns the track's elapsed playback time as an epoch timestamp.
    volume: :class:`int`
        The volume at which the player is playing at.
    shuffle: :class:`bool`
        Whether or not to mix the queue up in a random playing order.
    loop: :class:`int`
        Whether loop is enabled, and the type of looping.
        This is an integer as loop supports multiple states.

        0 = Loop off.

        1 = Loop track.

        2 = Loop queue.

        Example
        -------
        .. code:: python

            if player.loop == player.LOOP_NONE:
                await ctx.send('Not looping.')
            elif player.loop == player.LOOP_SINGLE:
                await ctx.send(f'{player.current.title} is looping.')
            elif player.loop == player.LOOP_QUEUE:
                await ctx.send('This queue never ends!')
    filters: Dict[:class:`str`, :class:`Filter`]
        A mapping of str to :class:`Filter`, representing currently active filters.
    queue: List[:class:`AudioTrack`]
        A list of AudioTracks to play.
    current: Optional[:class:`AudioTrack`]
        The track that is playing currently, if any.
    """

    LOOP_NONE: int = ...
    LOOP_SINGLE: int = ...
    LOOP_QUEUE: int = ...
    def __init__(self, guild_id: int, node: Node) -> None: ...
    @property
    def repeat(self) -> bool:
        """
        Returns the player's loop status. This exists for backwards compatibility, and also as an alias.

        .. deprecated:: 4.0.0
            Use :attr:`loop` instead.

        If ``self.loop`` is 0, the player is NOT looping.

        If ``self.loop`` is 1, the player is looping the single (current) track.

        If ``self.loop`` is 2, the player is looping the entire queue.
        """
        ...
    @property
    def is_playing(self) -> bool:
        """Returns the player's track state."""
        ...
    @property
    def is_connected(self) -> bool:
        """Returns whether the player is connected to a voicechannel or not."""
        ...
    @property
    def position(self) -> float:
        """Returns the track's elapsed playback time in milliseconds, adjusted for Lavalink stat interval."""
        ...
    def store(self, key: t.Any, value: t.Any) -> None:
        """
        Stores custom user data.

        Parameters
        ----------
        key: :class:`object`
            The key of the object to store.
        value: :class:`object`
            The object to associate with the key.
        """
        ...
    def fetch(self, key: t.Any, default: t.Optional[t.Any] = ...) -> None:
        """
        Retrieves the related value from the stored user data.

        Parameters
        ----------
        key: :class:`object`
            The key to fetch.
        default: Optional[:class:`any`]
            The object that should be returned if the key doesn't exist. Defaults to ``None``.

        Returns
        -------
        Optional[:class:`any`]
        """
        ...
    def delete(self, key: t.Any) -> None:
        """
        Removes an item from the the stored user data.

        Parameters
        ----------
        key: :class:`object`
            The key to delete.

        Raises
        ------
        :class:`KeyError`
            If the key doesn't exist.
        """
        ...
    def add(
        self,
        track: t.Union[AudioTrack, DeferredAudioTrack, BareAudioTrackDataType],
        requester: int = ...,
        index: int = ...,
    ) -> None:
        """
        Adds a track to the queue.

        Parameters
        ----------
        track: Union[:class:`AudioTrack`, :class:`DeferredAudioTrack`, :class:`dict`]
            The track to add. Accepts either an AudioTrack or
            a dict representing a track returned from Lavalink.
        requester: :class:`int`
            The ID of the user who requested the track.
        index: Optional[:class:`int`]
            The index at which to add the track.
            If index is left unspecified, the default behaviour is to append the track. Defaults to ``None``.
        """
        ...
    async def play(
        self,
        track: t.Optional[
            t.Union[AudioTrack, DeferredAudioTrack, BareAudioTrackDataType]
        ] = ...,
        start_time: t.Optional[int] = ...,
        end_time: t.Optional[int] = ...,
        no_replace: t.Optional[bool] = ...,
        volume: t.Optional[int] = ...,
        pause: t.Optional[bool] = ...,
    ) -> None:
        """|coro|

        Plays the given track.

        Parameters
        ----------
        track: Optional[Union[:class:`DeferredAudioTrack`, :class:`AudioTrack`, :class:`dict`]]
            The track to play. If left unspecified, this will default
            to the first track in the queue. Defaults to ``None`` so plays the next
            song in queue. Accepts either an AudioTrack or a dict representing a track
            returned from Lavalink.
        start_time: Optional[:class:`int`]
            The number of milliseconds to offset the track by.
            If left unspecified or ``None`` is provided, the track will start from the beginning.
        end_time: Optional[:class:`int`]
            The position at which the track should stop playing.
            This is an absolute position, so if you want the track to stop at 1 minute, you would pass 60000.
            The default behaviour is to play until no more data is received from the remote server.
            If left unspecified or ``None`` is provided, the default behaviour is exhibited.
        no_replace: Optional[:class:`bool`]
            If set to true, operation will be ignored if a track is already playing or paused.
            The default behaviour is to always replace.
            If left unspecified or None is provided, the default behaviour is exhibited.
        volume: Optional[:class:`int`]
            The initial volume to set. This is useful for changing the volume between tracks etc.
            If left unspecified or ``None`` is provided, the volume will remain at its current setting.
        pause: Optional[:class:`bool`]
            Whether to immediately pause the track after loading it.
            The default behaviour is to never pause.
            If left unspecified or ``None`` is provided, the default behaviour is exhibited.

        Raises
        ------
        :class:`ValueError`
            If invalid values were provided for ``start_time`` or ``end_time``.
        :class:`TypeError`
            If wrong types were provided for ``no_replace``, ``volume`` or ``pause``.
        """
        ...
    async def stop(self) -> None:
        """|coro|

        Stops the player.
        """
        ...
    async def skip(self) -> None:
        """|coro|

        Plays the next track in the queue, if any.
        """
        ...
    def set_repeat(self, repeat: bool) -> None:
        """
        Sets whether tracks should be repeated.

        .. deprecated:: 4.0.0
            Use :func:`set_loop` to repeat instead.

        This only works as a "queue loop". For single-track looping, you should
        utilise the :class:`TrackEndEvent` event to feed the track back into
        :func:`play`.

        Also known as ``loop``.

        Parameters
        ----------
        repeat: :class:`bool`
            Whether to repeat the player or not.
        """
        ...
    def set_loop(self, loop: int) -> None:
        """
        Sets whether the player loops between a single track, queue or none.

        0 = off, 1 = single track, 2 = queue.

        Parameters
        ----------
        loop: :class:`int`
            The loop setting. 0 = off, 1 = single track, 2 = queue.
        """
        ...
    def set_shuffle(self, shuffle: bool) -> None:
        """
        Sets the player's shuffle state.

        Parameters
        ----------
        shuffle: :class:`bool`
            Whether to shuffle the player or not.
        """
        ...
    async def set_pause(self, pause: bool) -> None:
        """|coro|

        Sets the player's paused state.

        Parameters
        ----------
        pause: :class:`bool`
            Whether to pause the player or not.
        """
        ...
    async def set_volume(self, vol: int) -> None:
        """|coro|

        Sets the player's volume

        Note
        ----
        A limit of 1000 is imposed by Lavalink.

        Parameters
        ----------
        vol: :class:`int`
            The new volume level.
        """
        ...
    async def seek(self, position: int) -> None:
        """|coro|

        Seeks to a given position in the track.

        Parameters
        ----------
        position: :class:`int`
            The new position to seek to in milliseconds.
        """
        ...
    async def set_filter(self, _filter: Filter) -> None:
        """|coro|

        Applies the corresponding filter within Lavalink.
        This will overwrite the filter if it's already applied.

        Example
        -------
        .. code:: python

            equalizer = Equalizer()
            equalizer.update(bands=[(0, 0.2), (1, 0.3), (2, 0.17)])
            player.set_filter(equalizer)

        Parameters
        ----------
        _filter: :class:`Filter`
            The filter instance to set.

        Raises
        ------
        :class:`TypeError`
            If the provided ``_filter`` is not of type :class:`Filter`.
        """
        ...
    async def update_filter(self, _filter: Filter, **kwargs: t.Any) -> None:
        """|coro|

        Updates a filter using the upsert method;
        if the filter exists within the player, its values will be updated;
        if the filter does not exist, it will be created with the provided values.

        This will not overwrite any values that have not been provided.

        Example
        -------
        .. code :: python

            player.update_filter(Timescale, speed=1.5)
            # This means that, if the Timescale filter is already applied
            # and it already has set values of "speed=1, pitch=1.2", pitch will remain
            # the same, however speed will be changed to 1.5 so the result is
            # "speed=1.5, pitch=1.2"

        Parameters
        ----------
        _filter: :class:`Filter`
            The filter class (**not** an instance of, see above example) to upsert.
        **kwargs: :class:`any`
            The kwargs to pass to the filter.

        Raises
        ------
        :class:`TypeError`
            If the provided ``_filter`` is not of type :class:`Filter`.
        """
        ...
    def get_filter(self, _filter: t.Union[Filter, str]) -> t.Optional[Filter]:
        """
        Returns the corresponding filter, if it's enabled.

        Example
        -------
        .. code:: python

            from lavalink.filters import Timescale
            timescale = player.get_filter(Timescale)
            # or
            timescale = player.get_filter('timescale')

        Parameters
        ----------
        _filter: Union[:class:`Filter`, :class:`str`]
            The filter name, or filter class (**not** an instance of, see above example), to get.

        Returns
        -------
        Optional[:class:`Filter`]
        """
        ...
    async def remove_filter(self, _filter: t.Union[Filter, str]) -> None:
        """|coro|

        Removes a filter from the player, undoing any effects applied to the audio.

        Example
        -------
        .. code:: python

            player.remove_filter(Timescale)
            # or
            player.remove_filter('timescale')

        Parameters
        ----------
        _filter: Union[:class:`Filter`, :class:`str`]
            The filter name, or filter class (**not** an instance of, see above example), to remove.
        """
        ...
    async def clear_filters(self) -> None:
        """|coro|

        Clears all currently-enabled filters.
        """
        ...
    async def set_gain(self, band: int, gain: float = ...) -> None:
        """|coro|

        Sets the equalizer band gain to the given amount.

        .. deprecated:: 4.0.0
            Use :func:`set_filter` to apply the :class:`Equalizer` filter instead.

        Parameters
        ----------
        band: :class:`int`
            Band number (0-14).
        gain: Optional[:class:`float`]
            A float representing gain of a band (-0.25 to 1.00). Defaults to 0.0.
        """
        ...
    async def set_gains(self, *gain_list: BandsType) -> None:
        """|coro|

        Modifies the player's equalizer settings.

        .. deprecated:: 4.0.0
            Use :func:`set_filter` to apply the :class:`Equalizer` filter instead.

        Parameters
        ----------
        gain_list: :class:`any`
            A list of tuples denoting (``band``, ``gain``).
        """
        ...
    async def reset_equalizer(self) -> None:
        """|coro|

        Resets equalizer to default values.

        .. deprecated:: 4.0.0
            Use :func:`remove_filter` to remove the :class:`Equalizer` filter instead.
        """
        ...
    async def node_unavailable(self) -> None:
        """|coro|

        Called when a player's node becomes unavailable.
        Useful for changing player state before it's moved to another node.
        """
        ...
    async def change_node(self, node: Node) -> None:
        """|coro|

        Changes the player's node

        Parameters
        ----------
        node: :class:`Node`
            The node the player is changed to.
        """
        ...
    # def __repr__(self): ...

class Plugin:
    """
    Represents a Lavalink server plugin.

    Parameters
    ----------
    data: :class:`dict`
        The data to initialise a Plugin from.

    Attributes
    ----------
    name: :class:`str`
        The name of the plugin.
    version: :class:`str`
        The version of the plugin.
    """

    # __slots__ = ...
    def __init__(self, data: PluginMappingType) -> None: ...
    # def __str__(self) -> str: ...
    # def __repr__(self): ...
