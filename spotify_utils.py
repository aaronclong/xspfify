from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from core_utils import SpotifyClientAuth


def authenticate_spotify(
    auth: SpotifyClientAuth, scope="playlist-read-private,user-library-read"
) -> Spotify:
    oauth = SpotifyOAuth(
        client_id=auth.client_id,
        client_secret=auth.client_secret,
        redirect_uri=auth.redirect_url,
        scope=scope,
    )
    return Spotify(auth_manager=oauth)


def steam_playlist(sp: Spotify, *, limit=50, offset=0):
    playlist = sp.current_user_playlists(limit, offset)
    total = playlist["total"]
    items = playlist["items"]
    cur = len(items)

    yield from items

    if cur >= total:
        return

    while cur < total:
        offset += 1
        playlist = sp.current_user_playlists(limit, offset)
        items = playlist["items"]
        cur += len(items)
        yield from items
