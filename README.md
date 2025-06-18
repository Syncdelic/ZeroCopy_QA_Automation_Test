---

# Zero Copy Labs · QA Automation Test

---

End-to-end demonstration of three core QA skills:

1. **UI automation** with Selenium & pytest  
2. **Visual regression** detection with OpenCV & SSIM  
3. **API testing** with requests & JSON Schema  

---

## Table of Contents
1. [Prerequisites](#prerequisites)  
2. [Quick Start](#quick-start)  
3. [Project Structure](#project-structure)  
4. [Part 1 – UI Login Suite](#part-1--ui-login-suite)  
5. [Part 2 – Visual Tests](#part-2--visual-tests)  
6. [Part 3 – API Tests](#part-3--api-tests)  
7. [Troubleshooting](#troubleshooting)  

---

## Prerequisites
| Requirement             | Notes                                                                  |
|-------------------------|------------------------------------------------------------------------|
| Python ≥ 3.9            | Any OS – use a virtual-environment                                     |
| Google Chrome / Chromium| Make sure the version matches **chromedriver**                         |
| chromedriver            | Must be discoverable on your `PATH` or via `CHROMEDRIVER` environment var |

### One-line install (inside your venv)
```bash
pip install -r requirements.txt
````

---

## Quick Start

```bash
# 1 Clone & enter
git clone https://github.com/Syncdelic/ZeroCopy_QA_Automation_Test.git
cd ZeroCopy_QA_Automation_Test

# 2 Create & activate virtual-env
python -m venv .venv && source .venv/bin/activate      # PowerShell: .venv\Scripts\Activate.ps1

# 3 Install dependencies
pip install -r requirements.txt

# 4 Run the whole test-suite headless
pytest -q                                              # expect: 4 + 1 + 3 = 8 passed
```

> **Tip:** set `HEADLESS=0` to watch the browser during Part 1.

---

## Project Structure

```
.
├── api_tests/           # Part 3
├── pages/               # Page-Object classes (Part 1)
├── tests/               # Login tests (Part 1)
├── visual_tests/        # Part 2
├── requirements.txt
└── README.md            # ← you are here
```

---

## Part 1 – UI Login Suite

|                   | Value / Description                                                |
| ----------------- | ------------------------------------------------------------------ |
| Target site       | `https://the-internet.herokuapp.com/login`                         |
| Valid credentials | **tomsmith / SuperSecretPassword!**                                |
| Scenarios         | ✓ Valid login • ✓ Invalid username • ✓ Invalid password • ✓ Blanks |
| Assertions        | Success / error banner text & colour • URL redirection             |
| Pattern           | **Page Object Model** (see `pages/`)                               |
| Runner            | `pytest` – parametrised across four cases                          |

### Run only Part 1

```bash
pytest tests -q        # 4 passed
```

---

## Part 2 – Visual Tests

Detects pixel-level changes between two UI screenshots using **SSIM ≥ 0.99**.

### Deliverables

1. **Checklist** of ten meaningful differences (see `visual_tests/Differences.md`).
2. **Auto test** (`visual_tests/test_visual.py`) – generates red-overlay artefacts in `visual_tests/artifacts/`.

### Run only Part 2

```bash
pytest visual_tests -q  # 1 passed when images match
```

---

## Part 3 – API Tests

| Endpoint            | Verb   | Expected HTTP code | Assertions (high-level)                       |
| ------------------- | ------ | ------------------ | --------------------------------------------- |
| `/api/users?page=2` | GET    | 200 OK             | Status • JSON schema • content sanity         |
| `/api/users`        | POST   | 201 Created        | Status • echoes input • id + timestamp format |
| `/api/users/2`      | DELETE | 204 No Content     | Status • empty body                           |

### Run only Part 3

```bash
pytest api_tests -q     # 3 passed
```

---

## Troubleshooting

| Symptom / Error                                | Likely Cause & Fix                                                         |
| ---------------------------------------------- | -------------------------------------------------------------------------- |
| `SessionNotCreatedException`                   | Chrome / chromedriver major versions differ → upgrade one side             |
| Browser flashes then closes (or nothing shown) | Remove `HEADLESS=0` on servers without GUI                                 |
| `requests.exceptions.ConnectionError` (Part 3) | Offline / proxy – set `REQRES_URL` to a local stub or use a VPN            |
| SSIM below threshold (Part 2)                  | Genuine visual regression – inspect artefacts in `visual_tests/artifacts/` |

---

### OS-specific chromedriver tips

| OS      | Install example                                                  |
| ------- | ---------------------------------------------------------------- |
| macOS   | `brew install --cask google-chrome && brew install chromedriver` |
| Windows | `choco install googlechrome chromedriver`                        |
| Linux   | `sudo dnf install chromium chromedriver`  *(Fedora example)*     |

> If `chromedriver` lives elsewhere:
> `export CHROMEDRIVER="/custom/path/chromedriver"`

---

*© 2025 Zero Copy Labs · All rights reserved*
