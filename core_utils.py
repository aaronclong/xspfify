import logging
from getpass import getpass
from pathlib import Path
from typing import NamedTuple


def setup_logger():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__package__)
    return logger


logger = setup_logger()


class SpotifyClientAuth(NamedTuple):
    client_id: str
    client_secret: str
    redirect_url: str


def prompt_credentials() -> SpotifyClientAuth:
    client_id = getpass("Spotify Client ID: ")
    client_secret = getpass("Spotify Client Secret: ")

    return SpotifyClientAuth(client_id, client_secret, "")


def handle_output_file(output: str) -> Path:
    is_file = output.endswith(".xspf")
    output_path = Path(output)

    if is_file:
        logger.info(f'Creating parent folder if doesn\'t exist: "{output_path.parent}"')
        output_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        logger.info(f'Creating output directory if doesn\'t exist: "{output_path}"')
        output_path.mkdir(parents=True, exist_ok=True)
        output_path = output_path.joinpath("playlist.xspf")

    return output_path
