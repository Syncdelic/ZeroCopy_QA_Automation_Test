# tests/conftest.py
import os, shutil, platform, pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def _locate_driver() -> str:
    """Return an executable chromedriver path or raise."""
    # 1) explicit env var beats everything
    if env := os.getenv("CHROMEDRIVER"):
        return env
    # 2) driver bundled in PATH (brew / choco / apt)
    if which := shutil.which("chromedriver"):
        return which
    raise RuntimeError(
        "chromedriver not found. Install it or set CHROMEDRIVER env var."
    )

@pytest.fixture
def driver():
    service = Service(_locate_driver())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")   # comment to see UI
    options.add_argument("--window-size=1280,800")

    drv = webdriver.Chrome(service=service, options=options)
    yield drv
    drv.quit()

