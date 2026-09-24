import os
import base64

CLIENT_ID = "6bed26ef442c4ef78b48d8ccb97857a6"
CLIENT_SECRET = "faab627eddc64af68e396133d5ba4f4c"
TOKEN_CACHE_PATH = os.path.expanduser("~/mcp/Spotify/.spotify_mcp_token.json")

def auth_header():
    raw = f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
    return {"Authorization": f"Basic {base64.b64encode(raw).decode()}"}