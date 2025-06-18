# ZeroCopy QA Automation Test

A three‑part showcase of core QA skills. This README covers **Part 1: UI Login Tests**, **Part 2: Visual Tests**, and **Part 3: API Tests**.

> **Install once (inside your virtual‑env)**
>
> ```bash
> pip install -r requirements.txt
> ```

---

\## Part 1 — Selenium + pytest login suite

|                   | Requirement                                                |
| ----------------- | ---------------------------------------------------------- |
| Target URL        | `https://the-internet.herokuapp.com/login`                 |
| Happy‑path creds  | `tomsmith` / `SuperSecretPassword!`                        |
| Scenarios covered | ✓ valid login · ✓ bad username · ✓ bad password · ✓ blanks |
| Assertions        | banner text & colour · URL redirect                        |
| Architecture      | Page Object Model (`pages/` dir)                           |

\### Prerequisites

* Python ≥ 3.9
* **Google Chrome / Chromium** installed
* **Chromedriver** matching the browser major version (must be on your `PATH`)

> **macOS (Homebrew)**
>
> ```bash
> brew install --cask google-chrome      # or chromium
> brew install chromedriver
> ```
>
> **Windows (Chocolatey)**
>
> ```powershell
> choco install googlechrome chromedriver
> ```
>
> **Linux (Fedora example)**
>
> ```bash
> sudo dnf install chromium chromedriver   # or google-chrome-stable
> ```
>
> ⚠️ If `chromedriver` isn’t on your `PATH`, set an env‑var before running tests:
>
> ```bash
> export CHROMEDRIVER="/custom/path/to/chromedriver"
> ```

\### Quick start

```bash
# clone the repo
$ git clone https://github.com/Syncdelic/ZeroCopy_QA_Automation_Test.git && cd ZeroCopy_QA_Automation_Test

# create & activate virtual‑env
$ python -m venv .venv && source .venv/bin/activate

# install deps (selenium, pytest, OpenCV, scikit‑image, imutils)
(.venv)$ pip install -r requirements.txt

# run only login tests headless
(.venv)$ pytest tests -q        # expect: 4 passed
```

To **watch the browser**, set `HEADLESS=0`:

```bash
(.venv)$ HEADLESS=0 pytest tests -q
```

\### Project layout (Part 1)

```
.
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   └── login_page.py   # locators + login(), banner helpers
├── tests/
│   ├── __init__.py
│   ├── conftest.py     # cross‑platform driver fixture
│   └── test_login.py   # parametrised 4‑case suite
└── requirements.txt
```

\### Troubleshooting

* **Version mismatch** → `selenium.common.exceptions.SessionNotCreatedException`  ➜  install matching major versions of Chrome/Chromium and chromedriver.
* **Port already in use** → stray chromedriver process; kill it or reboot.
* **Banner assertion fails** → The Internet site sometimes rate‑limits; rerun after 30 s.

---

\## Part 2 — Visual Tests (Spot‑the‑Difference)
Detect and prevent visual regressions between UI versions.

\### Deliverables

1. **Manual checklist** (below) – enumerates every meaningful difference.
2. **Automated pytest suite** in `visual_tests/` – compares screenshots with **SSIM ≥ 0.99** and stores diff artefacts.

*(Extra libraries `opencv-python`, `scikit-image`, and `imutils` are already in `requirements.txt`.)*

\### Quick start

```bash
# run only visual tests
(.venv)$ pytest visual_tests -q
```

\### Differences checklist

| #  | Element / Region                  | Image 1 (Baseline)                             | Image 2 (Candidate)                                 | Why it matters for QA                                                                     |
| -- | --------------------------------- | ---------------------------------------------- | --------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| 1  | **Header text**                   | “My Accounts” (spelled correctly, single line) | “My Acounts” (typo) + red sub‑label “(My Accounts)” | Spelling & duplication affect brand trust, accessibility, and automated text assertions.  |
| 2  | **Dark‑blue header bar height**   | Shorter                                        | Taller                                              | Extra height can push content down, breaking fixed‑height layouts on small screens.       |
| 3  | **Balance amount style**          | **Bold** “\$1,200.50”                          | Regular weight                                      | Loss of emphasis on critical info; affects visual hierarchy and low‑vision accessibility. |
| 4  | **Account‑number placement**      | Centered below balance                         | Right‑aligned beside balance                        | Changes reading order; may confuse screen readers.                                        |
| 5  | **Action buttons present**        | *Transfer*, *Deposit*, *Pay Bills*             | Only *Transfer*                                     | Missing functionality indicates regression of user flows.                                 |
| 6  | **Button row layout**             | Three full‑width buttons                       | Single centred button                               | Alters touch‑target reachability and visual balance.                                      |
| 7  | **Button colour**                 | Vivid blue (`#2979FF`)                         | Paler blue (`#5C8CFF`)                              | Brand‑colour consistency; lower contrast may fail WCAG.                                   |
| 8  | **Colour contrast in header**     | White text on dark blue (high contrast)        | Red text on dark blue (low contrast)                | Risk of WCAG 1.4.3 failure; flagged by automated contrast tests.                          |
| 9  | **Vertical padding / whitespace** | Tighter card                                   | Increased whitespace                                | May push content below the fold on mobile.                                                |
| 10 | **Component height**              | 197 px                                         | 207 px                                              | Off‑by‑10 px can break pixel‑perfect layouts and scroll positioning.                      |

\### Directory layout (Part 2)

```
visual_tests/
├── assets/
│   ├── baseline/      
│   │   └── account_v1.png
│   └── candidate/    
│       └── account_v2.png
├── __init__.py
├── compare_images.py  # OpenCV + SSIM helper
├── test_visual.py     # pytest wrapper calling compare_images()
└── artifacts/         # diff outputs written here at runtime
```

`compare_images.py` highlights changed regions in red and writes three artefacts: baseline‑marked, candidate‑marked, and `diff_mask.png`.

---

\## Part 3 — API Tests
Placeholder for REST‑assurance tests against `https://reqres.in/`.

---

*© 2025 Zero Copy Labs*

