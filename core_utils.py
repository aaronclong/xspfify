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


def _prompt_redirect_url() -> str:
    """Allow entering a full URL or gather components interactively."""
    template_hint = "${http|https}://127.0.0.1:s{port}/${route}"
    prompt = (
        "Spotify Redirect URL "
        f"(enter full URL or leave empty to build as {template_hint}): "
    )
    redirect_url = input(prompt).strip()
    if redirect_url:
        return redirect_url

    scheme = input("  Scheme [http]: ").strip().lower() or "http"
    if scheme not in ("http", "https"):
        logger.warning('Unknown scheme "%s", defaulting to http', scheme)
        scheme = "http"

    port = input("  Port [8000]: ").strip() or "8000"
    route = input("  Route (no leading slash) [callback]: ").strip() or "callback"
    route = route.lstrip("/")

    return f"{scheme}://127.0.0.1:{port}/{route}"


def prompt_credentials() -> SpotifyClientAuth:
    client_id = getpass("Spotify Client ID: ")
    client_secret = getpass("Spotify Client Secret: ")

    redirect_url = _prompt_redirect_url()

    return SpotifyClientAuth(client_id, client_secret, redirect_url)


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
