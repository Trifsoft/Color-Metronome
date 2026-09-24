from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
from urllib.parse import urlencode, urlparse, parse_qs
import json
import os
import requests
from env import TOKEN_CACHE_PATH, CLIENT_ID, CLIENT_SECRET, auth_header

REDIRECT_URI = "http://127.0.0.1:8888/callback"
CLAUDE_CONFIG_PATH = os.path.expanduser("~/Library/Application Support/Claude/claude_desktop_config.json")
SPOTIFY_MCP_PATH = os.path.expanduser("~/mcp/Spotify/spotify.py")
SCOPE = os.environ.get(
    "SPOTIFY_SCOPE",
    "user-read-playback-state user-read-currently-playing streaming playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-follow-modify user-follow-read user-read-playback-position user-top-read user-read-recently-played user-library-modify user-library-read"
)

def _save_refresh_token(refresh_token):
    with open(TOKEN_CACHE_PATH, "w") as f:
        json.dump({"refresh_token": refresh_token}, f)


def _write_claude_config():
    config_path = CLAUDE_CONFIG_PATH
    config_dir = os.path.dirname(config_path)
    if config_dir:
        os.makedirs(config_dir, exist_ok=True)

    existing = {}
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            try:
                existing = json.load(f) or {}
            except json.JSONDecodeError:
                existing = {}

    if not isinstance(existing.get("mcpServers"), dict):
        existing["mcpServers"] = {}

    existing["mcpServers"]["spotify"] = {
        "command": "/opt/miniconda3/bin/python",
        "args": [SPOTIFY_MCP_PATH, "--mcp"],
        "env": {
            "SPOTIFY_CLIENT_ID": CLIENT_ID,
            "SPOTIFY_CLIENT_SECRET": CLIENT_SECRET,
        },
    }

    with open(config_path, "w") as f:
        json.dump(existing, f, indent=2)
        f.write("\n")


class _CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        code = query.get("code", [None])[0]

        if code:
            resp = requests.post("https://accounts.spotify.com/api/token", data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI
            }, headers=auth_header())
            resp.raise_for_status()
            data = resp.json()

            _save_refresh_token(data["refresh_token"])
            _write_claude_config()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body>Authorized! You can close this tab.</body></html>")
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body>No code received.</body></html>")

    def log_message(self, format, *args):
        pass  # silence default request logging

def authorize_via_browser():
    """
    Opens the browser for the user to authorize the app. The local server
    captures the redirect, exchanges the code for tokens, and writes the
    refresh_token to disk itself. Returns the fresh access_token.
    """
    server = HTTPServer(("127.0.0.1", 8888), _CallbackHandler)

    auth_url = "https://accounts.spotify.com/authorize?" + urlencode({
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE
    })
    webbrowser.open(auth_url)

    server.handle_request()  # blocks until the callback hits, then stops
    server.server_close()

if __name__ == "__main__":
    authorize_via_browser()