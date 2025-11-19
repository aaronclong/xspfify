"""Utilities for building XSPF playlists from Spotify data."""

from __future__ import annotations

from typing import Iterable
from xml.etree import ElementTree as ET

from xspf_lib import Playlist, Track

from dtos import TrackInfo


def spotify_item_to_track(item: TrackInfo) -> Track:
    """Convert a Spotify playlist item into an xspf-lib Track."""
    return Track(title=item.title, creator=item.artist, album=item.album)


def playlist_from_spotify_items(name: str, items: Iterable[TrackInfo]) -> Playlist:
    """Build an xspf-lib Playlist from Spotify playlist items."""
    tracks = [spotify_item_to_track(item) for item in items]
    playlist = Playlist(title=name, trackList=tracks)
    return playlist


def playlist_to_xml(playlist: Playlist) -> str:
    """Render the playlist to XML using xspf-lib."""
    return ET.tostring(playlist.to_xml_element(), encoding="unicode")
