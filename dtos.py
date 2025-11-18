from typing import NamedTuple, Optional


class TrackInfo(NamedTuple):
    title: Optional[str]
    artist: Optional[str]
    album: Optional[str]
