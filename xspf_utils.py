"""Utilities for building XSPF playlists from Spotify data."""

from __future__ import annotations

from typing import Iterable, Mapping, Optional
from xml.etree import ElementTree as ET

from xspf_lib import Playlist, Track


def _first_artist(track: Mapping) -> Optional[str]:
    artists = track.get("artists") or []
    if not artists:
        return None
    return (artists[0] or {}).get("name")


def spotify_item_to_track(item: Mapping, *, include_album: bool = True) -> Track:
    """Convert a Spotify playlist item into an xspf-lib Track."""
    track = item.get("track") or {}
    title = track.get("name")
    creator = _first_artist(track)
    album = (track.get("album") or {}).get("name") if include_album else None

    return Track(title=title, creator=creator, album=album)


def playlist_from_spotify_items(
    name: str, items: Iterable[Mapping], *, include_album: bool = True
) -> Playlist:
    """Build an xspf-lib Playlist from Spotify playlist items."""
    tracks = [
        spotify_item_to_track(item, include_album=include_album) for item in items
    ]
    playlist = Playlist(title=name, trackList=tracks)
    return playlist


def playlist_to_xml(playlist: Playlist, *, pretty: bool = True) -> str:
    """Render the playlist to XML using xspf-lib."""
    return ET.tostring(playlist.to_xml_element(), encoding="unicode")
