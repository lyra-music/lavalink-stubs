"""
This type stub file was generated by pyright.
"""

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

class Penalty:
    """Represents the penalty of the stats of a Node."""

    player_penalty: int
    """The number of playing players. 1 player = 1 penalty point."""
    cpu_penalty: int
    """The penalty incurred from system CPU usage."""
    null_frame_penalty: int
    """The penalty incurred from the average number of null frames per minute."""
    deficit_frame_penalty: int
    """The penalty incurred from the average number of deficit frames per minute."""
    total: int
    """The overall penalty, as a sum of all other penalties."""

class Stats:
    """Encapsulates the 'Statistics' emitted by Lavalink, usually every minute."""

    is_fake: bool
    """Whether or not the stats are accurate. This should only be True when the node has not yet received any statistics from the Lavalink server."""
    uptime: int
    """How long the node has been running for, in milliseconds."""
    players: int
    """The number of players connected to the node."""
    playing_players: int
    """The number of players that are playing in the node."""
    memory_free: int
    """The amount of memory free to the node, in bytes."""
    memory_used: int
    """The amount of memory that is used by the node, in bytes."""
    memory_allocated: int
    """The amount of memory allocated to the node, in bytes."""
    memory_reservable: int
    """The amount of memory reservable to the node, in bytes."""
    cpu_cores: int
    """The amount of cpu cores the system of the node has."""
    system_load: int
    """The overall CPU load of the system. This is a number between 0-1, but can be multiplied by 100 for the percentage (0-100)."""
    lavalink_load: int
    """The CPU load generated by Lavalink This is a number between 0-1, but can be multiplied by 100 for the percentage (0-100)."""
    frames_sent: int
    """The number of frames sent to Discord.

    Warning
    -------
    Given that audio packets are sent via UDP, this number may not be 100% accurate due to packets dropped in transit."""
    frames_nulled: int
    """The number of frames that yielded null, rather than actual data."""
    frames_deficit: int
    """The number of missing frames. Lavalink generates this figure by calculating how many packets to expect per minute, and deducting ``frames_sent``. Deficit frames could mean the CPU is overloaded, and isn't generating frames as quickly as it should be."""
    penalty: Penalty

    # __slots__ = ...
    # def __init__(self, node, data) -> None: ...
    # @classmethod
    # def empty(cls, node): ...
