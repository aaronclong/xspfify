from spotipy.oauth2 import SpotifyOAuth

from core_utils import SpotifyClientAuth


def authenticate_spotify(
    auth: SpotifyClientAuth, scope="playlist-read-private,user-library-read"
):
    return SpotifyOAuth(
        client_id=auth.client_id,
        client_secret=auth.client_secret,
        redirect_uri=auth.redirect_url,
        scope="playlist-read-private,user-library-read",
    )
