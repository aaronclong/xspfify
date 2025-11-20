#!/usr/bin/python
# -*- coding: utf-8 -*-
from pathlib import Path

from pathvalidate import sanitize_filename
from spotipy import Spotify

from . import core_utils, xspf_utils
from .spotify_utils import (
    authenticate_spotify,
    get_playlist_tracks,
    get_playlists,
)

logger = core_utils.setup_logger()
parser = core_utils.create_arg_parser()


def _convert_spotify_playlist_to_xspf(playlist: dict, sp: Spotify, output_path: Path):
    playlist_name = playlist.get("name")
    playlist_id = playlist.get("id")

    logger.info(f"Writing {playlist_name} to xspf")

    tracks = [track for track in get_playlist_tracks(sp, playlist_id)]
    playlist = xspf_utils.playlist_from_spotify_items(playlist_name, tracks)

    output_file = sanitize_filename(f"{playlist_name}.xspf")
    with open(output_path.joinpath(output_file), "w+") as fd:
        fd.write(xspf_utils.playlist_to_xml(playlist))


def main():
    args = parser.parse_args()
    output_path = core_utils.handle_output_folder(args.output)
    creds = core_utils.prompt_credentials()
    sp = authenticate_spotify(creds)

    playlists = []
    for playlist in get_playlists(sp):
        _convert_spotify_playlist_to_xspf(playlist, sp, output_path)
        playlists.append(playlist)

    logger.info(f"There were {len(playlists)} for user")


if __name__ == "__main__":
    main()
