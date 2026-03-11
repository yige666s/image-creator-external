import json
import os
import secrets
import time
import threading
import webbrowser
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional

import keyring

REDIRECT_URI     = "http://localhost:9877/callback"
CALLBACK_PORT    = 9877
KEYRING_SERVICE  = "shortart"
KEYRING_KEY      = "image-creator:session"

SHORTART_API_URL = os.environ.get("SHORTART_API_URL", "https://shortart-api.wenuts.top")

SESSION_TTL_SECONDS = 58 * 24 * 3600


class _CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if "token" in params:
            self.server.auth_token = params["token"][0]
            self.server.auth_state = params.get("state", [None])[0]
            self._respond("✓ Authorization successful! ShortArt login complete, you may return to the desktop...")
        elif "error" in params:
            self.server.auth_error = params["error"][0]
            self._respond(f"✗ Authorization failed: {params['error'][0]}")
        else:
            self._respond("Unknown callback parameters")

    def _respond(self, message: str):
        html = f"""
        <html><body style="font-family:sans-serif;text-align:center;padding:60px;background:#0f0f0f;color:#e8e8e8">
            <h2>{message}</h2>
            <p style="color:#666">You can close this tab now.</p>
        </body></html>
        """.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html)

    def log_message(self, *args):
        pass


class ShortArtAuth:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_token(self) -> str:
        cached = self._load_cached_token()
        if cached:
            return cached

        print("[ShortArtAuth] No valid ShortArt session found, initiating Google OAuth...")
        return self._do_full_auth()

    def is_authorized(self) -> bool:
        return self._load_cached_token() is not None

    def revoke(self):
        try:
            keyring.delete_password(KEYRING_SERVICE, KEYRING_KEY)
            print("[ShortArtAuth] Local session token cleared")
        except Exception:
            pass

    def _do_full_auth(self) -> str:
        state = secrets.token_urlsafe(16)
        start_url = (
            f"{SHORTART_API_URL}/api/oauth/start"
            f"?redirect_back={urllib.parse.quote(REDIRECT_URI, safe='')}"
            f"&state={state}"
        )

        token = self._start_callback_server_and_wait(start_url, state)
        self._save_token(token)
        return token

    def _start_callback_server_and_wait(self, start_url: str, expected_state: str) -> str:
        server = HTTPServer(("localhost", CALLBACK_PORT), _CallbackHandler)
        server.auth_token = None
        server.auth_state = None
        server.auth_error = None

        thread = threading.Thread(target=server.handle_request, daemon=True)
        thread.start()

        print("[ShortArtAuth] Opening browser for Google OAuth...")
        webbrowser.open(start_url)

        thread.join(timeout=180)

        if server.auth_error:
            raise RuntimeError(f"OAuth authorization failed: {server.auth_error}")
        if not server.auth_token:
            raise RuntimeError("OAuth timed out (3 minutes), please retry")

        if server.auth_state != expected_state:
            raise RuntimeError("OAuth state mismatch, possible security issue, please retry")

        return server.auth_token

    def _save_token(self, token: str):
        payload = json.dumps({
            "token":      token,
            "expires_at": time.time() + SESSION_TTL_SECONDS,
        })
        keyring.set_password(KEYRING_SERVICE, KEYRING_KEY, payload)

    def _load_cached_token(self) -> Optional[str]:
        raw = keyring.get_password(KEYRING_SERVICE, KEYRING_KEY)
        if not raw:
            return None
        try:
            payload = json.loads(raw)
            if time.time() > payload["expires_at"] - 86400:
                return None
            return payload["token"]
        except (json.JSONDecodeError, KeyError):
            return None


shortart_auth = ShortArtAuth()


if __name__ == "__main__":
    import sys

    cmd = sys.argv[1] if len(sys.argv) > 1 else "login"

    if cmd == "login":
        try:
            token = shortart_auth.get_token()
            print(f"\n✓ Authentication successful! ShortArt token saved.")
            print(f"  Token prefix: {token[:8]}...")
        except Exception as e:
            print(f"\n✗ Authentication failed: {e}")
            sys.exit(1)

    elif cmd == "status":
        if shortart_auth.is_authorized():
            raw = keyring.get_password(KEYRING_SERVICE, KEYRING_KEY)
            payload = json.loads(raw)
            remaining = payload["expires_at"] - time.time()
            days = int(remaining / 86400)
            print(f"✓ Authorized. ShortArt token expires in ~{days} days")
        else:
            print("✗ Not authorized. Run: python3 auth.py login")

    elif cmd == "revoke":
        shortart_auth.revoke()

    else:
        print("Usage: python3 auth.py [login|status|revoke]")
