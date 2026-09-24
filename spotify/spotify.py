from mcp.server.mcpserver import MCPServer
import os
import json
import time
import requests
from spotify.env import TOKEN_CACHE_PATH, auth_header

_token_cache = {"access_token": None, "expires_at": 0}

def _load_refresh_token():
    if os.path.exists(TOKEN_CACHE_PATH):
        with open(TOKEN_CACHE_PATH) as f:
            return json.load(f).get("refresh_token")
    return None


def _request_token_via_refresh(refresh_token):
    """Uses a saved refresh_token to get a new access_token, no browser needed."""
    resp = requests.post("https://accounts.spotify.com/api/token", data={
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }, headers=auth_header())
    resp.raise_for_status()
    return resp.json()


def get_access_token():
    """
    Returns a valid access token, refreshing or re-authorizing only when needed.
    Caches in memory for the process lifetime; caches refresh_token on disk.
    """
    if _token_cache["access_token"] and time.time() < _token_cache["expires_at"]:
        return _token_cache["access_token"]

    refresh_token = _load_refresh_token()
    if refresh_token:
        data = _request_token_via_refresh(refresh_token)
        access_token, expires_in = data["access_token"], data.get("expires_in", 3600)
    else:
        return None

    _token_cache["access_token"] = access_token
    _token_cache["expires_at"] = time.time() + expires_in - 60
    return access_token


def make_call(method, endpoint, return_response = True, **kwargs):
    url = f"https://api.spotify.com/v1{endpoint}"
    headers = {"Authorization": f"Bearer {get_access_token()}"}

    resp = requests.request(method, url, headers=headers, **kwargs)
    resp.raise_for_status()

    if return_response and resp.content:
        return resp.json()
    return None

# ------- PARSING -------

def get_artist(artist):
    return {
        "id": artist["id"],
        "name": artist["name"]
    }

def get_album(album):
    return {
        "name": album["name"],
        "artists": [get_artist(artist) for artist in album["artists"]],
        "id": album["id"],
        "images": [image["url"] for image in album["images"]]
    }

def get_track(track):
    return {
        "name": track["name"],
        "id": track["id"],
        "album": get_album(track["album"]),
        "artists": [get_artist(artist) for artist in track["artists"]],
        "duration_ms": track["duration_ms"]
    }

def getCurrentSong():
    """
    Fetch the track currently playing on the user's Spotify account.

    Returns song info if something is playing,
    or None if nothing is playing.
    """
    resp = make_call("GET", "/me/player/currently-playing")

    if resp is not None:
        track = get_track(resp["item"])
        track["current_ms"] = resp["progress_ms"]
        track["is_playing"] = resp["is_playing"]
        return track
    return None