"""
pytest wrapper that fails if the Structural-Similarity index (SSIM)
falls below 0.99.  Threshold is adjustable per project style-guide.
"""

from pathlib import Path
from visual_tests.compare_images import diff_images

# Paths are always relative to this file, so the test is platform-agnostic
BASE_DIR = Path(__file__).parent
BASELINE_IMG = BASE_DIR / "assets" / "baseline" / "account_v1.png"
CANDIDATE_IMG = BASE_DIR / "assets" / "candidate" / "account_v2.png"
THRESHOLD = 0.99


def test_visual_regression():
    score = diff_images(BASELINE_IMG, CANDIDATE_IMG, min_area_small=3, min_area_big=60, close_iter=2)
    assert score >= THRESHOLD, (
        f"Visual regression detected — SSIM={score:.4f} < {THRESHOLD}"
    )

