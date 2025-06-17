# ZeroCopy QA Automation Test

A three‑part showcase of core QA skills. This README covers **Part 1: UI Login Tests**; Parts 2‑3 (image diff + API) live in their own folders.

---

\## Part 1 — Selenium + pytest login suite

|                   | Requirement                                             |
| ----------------- | ------------------------------------------------------- |
| Target URL        | `https://the-internet.herokuapp.com/login`              |
| Happy path creds  | `tomsmith` / `SuperSecretPassword!`                     |
| Scenarios covered | ✓ valid login  ✓ bad username  ✓ bad password  ✓ blanks |
| Assertions        | banner text & colour · URL redirect                     |
| Architecture      | Page Object Model (`pages/` dir)                        |

---

\### Prerequisites

* Python ≥ 3.9
* **Google Chrome *or* Chromium** installed
* **Chromedriver** **same major version** as the browser *(put it in your `PATH`)*

  * **macOS (Homebrew)**

    ```bash
    brew install --cask google-chrome   # or chromium
    brew install chromedriver
    ```
  * **Windows (Chocolatey)**

    ```powershell
    choco install googlechrome chromedriver
    ```
  * **Linux (Fedora example)**

    ```bash
    sudo dnf install chromium chromedriver   # or google-chrome-stable
    ```

> ⚠️ If `chromedriver` isn’t on your `PATH`, set an env‑var before running tests:
>
> ```bash
> export CHROMEDRIVER="/custom/path/to/chromedriver"
> ```

---

\### Quick start

```bash
# clone the repo
$ git clone <your‑fork‑url> && cd ZeroCopy_QA_Automation_Test

# create & activate virtual‑env
$ python -m venv .venv && source .venv/bin/activate

# install deps
(.venv)$ pip install -r requirements.txt   # only selenium + pytest

# run all tests headless
(.venv)$ pytest -q        # expect: 4 passed
```

To **watch the browser**, set `HEADLESS=0`:

```bash
(.venv)$ HEADLESS=0 pytest -q
```

---

\### Project layout (part 1)

```
.
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   └── login_page.py   # contains locators + login(), banner helpers
├── tests/
│   ├── __init__.py
│   ├── conftest.py     # cross‑platform driver fixture
│   └── test_login.py   # parametrised 4‑case suite
└── requirements.txt
```

---

\### Troubleshooting

* **Version mismatch** → `selenium.common.exceptions.SessionNotCreatedException`  ➜  install matching major versions of Chrome/Chromium and chromedriver.
* **Port already in use** → stray chromedriver process; kill it or reboot.
* **Banner assertion fails** → The Internet site sometimes rate‑limits; rerun after 30 s.

---

*© 2025 Zero Copy Labs*

