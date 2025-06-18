"""Common fixtures for the API test suite."""
import os
import pytest
import requests

# --- ReqRes configuration ----------------------------------------------------
API_KEY = "reqres-free-v1"                     # <–– FREE key from docs
BASE_URL_DEFAULT = "https://reqres.in"

# --- Fixtures ----------------------------------------------------------------
@pytest.fixture(scope="session")
def base_url() -> str:
    """Base endpoint; override with  REQRES_URL=...  pytest."""
    return os.getenv("REQRES_URL", BASE_URL_DEFAULT)

@pytest.fixture(scope="session")
def session():
    """
    Shared requests.Session with a browser-ish UA.
    We *don’t* attach the API key here to avoid confusion —
    each test call sets it explicitly so it’s always visible.
    """
    with requests.Session() as s:
        s.headers.update(
            {
                # Cloudflare blocks default Python UA ⇒ spoof Chrome.
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36 pytest-suite"
                ),
                "Accept": "application/json",
            }
        )
        yield s

