#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse

import core_utils
import xspf_utils
from spotify_utils import authenticate_spotify, get_playlist_tracks, get_playlists

logger = core_utils.setup_logger()
parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", default="output/playlist.xspf")


def main():
    args = parser.parse_args()
    _output_path = core_utils.handle_output_file(args.output)
    creds = core_utils.prompt_credentials()
    sp = authenticate_spotify(creds)
    playlist = [playlist for playlist in get_playlists(sp)]
    logger.info(f"There were {len(playlist)} for user")
    tracks = [track for track in get_playlist_tracks(sp, playlist[0]["id"])]
    playlist = xspf_utils.playlist_from_spotify_items(playlist[0].get("name"), tracks)
    logger.info(xspf_utils.playlist_to_xml(playlist))


if __name__ == "__main__":
    main()
