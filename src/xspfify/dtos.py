from typing import NamedTuple, Optional


class SpotifyClientAuth(NamedTuple):
    client_id: str
    client_secret: str
    redirect_url: str


class TrackInfo(NamedTuple):
    title: Optional[str]
    artist: Optional[str]
    album: Optional[str]
