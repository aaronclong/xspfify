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


# https://spotipy.readthedocs.io/en/2.25.1/index.html#spotipy.client.Spotify.playlist_items
def get_playlist_tracks(sp: Spotify, playlist_id: str, *, limit=100, offset=0):
    # Only request the fields we need to keep payloads small while paging
    fields = "items(track(name,artists(name),album(name))),next,total,limit,offset"
    page = sp.playlist_items(playlist_id, fields=fields, limit=limit, offset=offset)
    total = page["total"]
    cur = 0

    while cur < total:
        items = page["items"]
        cur += len(items)
        yield from items
        page = sp.next(page)

        # for item in items:
        #     track = item.get("track") or {}
        #     artists = track.get("artists") or []
        #     yield {
        #         "title": track.get("name"),
        #         "artist": artists[0]["name"] if artists else None,
        #         "album": (track.get("album") or {}).get("name"),
        #     }

        # Stop when we've exhausted the collection
        # offset = page.get("offset", offset) + page.get("limit", limit)
        # if offset >= total or not page.get("next"):
        #     break
