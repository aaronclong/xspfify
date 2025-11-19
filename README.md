# XSPF generator

CLI to export your Spotify playlists to [XSPF](https://xspf.org/) files for portable backups.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for dependency management and virtualenvs
- A Spotify application (create one in https://developer.spotify.com/dashboard) to obtain a Client ID, Client Secret, and Redirect URL

## Getting started

1) Install uv if you do not already have it:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2) Install dependencies into a uv-managed virtual environment:
   ```bash
   uv sync
   ```
3) Run the exporter (uv will activate the env automatically):
   ```bash
   uv run python -m main -o output
   ```
   - You will be prompted for your Spotify Client ID, Client Secret, and Redirect URL. The redirect URL must match one configured for your Spotify app (e.g. `http://127.0.0.1:8000/callback`).
   - Playlists will be written as `.xspf` files into the folder provided by `-o` (defaults to `./output`).

## Development workflows

- Format / lint:
  ```bash
  uv run ruff format .
  uv run ruff check .
  ```
- Add new dependencies:
  ```bash
  uv add package-name
  uv add --group dev dev-package-name
  ```
- Update all locked dependencies:
  ```bash
  uv lock --upgrade
  ```

## Notes

The generated playlists include artist, album, and track title for broad compatibility. Extend the payload by updating the `get_playlist_tracks` pipeline in `spotify_utils.py` and `playlist_from_spotify_items` in `xspf_utils.py`.
