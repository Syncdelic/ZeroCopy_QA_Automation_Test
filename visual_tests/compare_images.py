"""
compare_images.py  —  Visual-regression helper (SSIM + CIELAB ΔE).

► Pass A  (fine_mask)   – colour-only ΔE → finds glyph-level changes
► Pass B  (layout_mask) – grayscale SSIM  → finds block-level changes

Artefacts written to  visual_tests/artefacts/ :
    baseline_marked.png   candidate_marked.png   diff_mask.png
Run standalone or import diff_images() from pytest.
"""

from pathlib import Path
import argparse
import cv2
import imutils
import numpy as np
from skimage.metrics import structural_similarity as ssim


# ──────────────────────────────────────────────────────────────────────────────
#  Helpers
# ──────────────────────────────────────────────────────────────────────────────
def _lab_deltae_mask(img_a: np.ndarray,
                     img_b: np.ndarray,
                     delta_thr: float = 15.0) -> np.ndarray:
    """0/255 mask where CIELAB ΔE-76 > delta_thr (perceptual colour shift)."""
    lab_a = cv2.cvtColor(img_a, cv2.COLOR_BGR2LAB).astype("float32")
    lab_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2LAB).astype("float32")
    delta = np.linalg.norm(lab_a - lab_b, axis=2)     # ΔE for each pixel
    return np.where(delta > delta_thr, 255, 0).astype("uint8")


def _boxes(mask: np.ndarray, min_area: int):
    """Return bounding-boxes (x, y, w, h) for contours ≥ min_area."""
    cnts = imutils.grab_contours(
        cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    )
    return [cv2.boundingRect(c) for c in cnts if cv2.contourArea(c) >= min_area]


# ──────────────────────────────────────────────────────────────────────────────
#  Core
# ──────────────────────────────────────────────────────────────────────────────
def diff_images(
    baseline: Path,
    candidate: Path,
    out_dir: Path | None = None,
    *,
    min_area_small: int = 8,     # subtitle / glyphs
    min_area_big:   int = 40,    # header, buttons
    close_iter:     int = 2,     # block-level closing passes
) -> float:
    """Draw red boxes on differences, save artefacts, return SSIM score."""
    if not baseline.exists() or not candidate.exists():
        raise FileNotFoundError("Baseline or candidate image missing")

    img_a = cv2.imread(str(baseline))
    img_b = cv2.imread(str(candidate))
    H, W = max(img_a.shape[0], img_b.shape[0]), max(img_a.shape[1], img_b.shape[1])
    img_a = cv2.resize(img_a, (W, H))
    img_b = cv2.resize(img_b, (W, H))

    # ── SSIM mask (luminance differences) ───────────────────────────────────
    gray_a = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)
    gray_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)
    ssim_score, ssim_map = ssim(gray_a, gray_b, full=True)
    ssim_mask = cv2.threshold((ssim_map * 255).astype("uint8"),
                              0, 255,
                              cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # ── Colour mask (perceptual ΔE) ─────────────────────────────────────────
    colour_mask = _lab_deltae_mask(img_a, img_b, delta_thr=15)

    # ── Pass A – glyph-level  (colour only, slight opening) ────────────────
    kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 1))  # horizontal
    fine_mask = cv2.morphologyEx(colour_mask, cv2.MORPH_OPEN, kernel_h, iterations=1)
    fine_boxes = _boxes(fine_mask, min_area_small)

    # ── Pass B – layout-level (luminance only, closing) ────────────────────
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    layout_mask = cv2.morphologyEx(ssim_mask, cv2.MORPH_CLOSE, kernel, iterations=close_iter)
    coarse_boxes = _boxes(layout_mask, min_area_big)

    # ── Draw rectangles & filter razor-thin strips ─────────────────────────
    img_h, img_w = H, W
    for x, y, w, h in coarse_boxes + fine_boxes:
        if (h < 6 and w > 0.6 * img_w) or (w < 6 and h > 0.6 * img_h):
            continue  # skip full-width 1-px borders
        cv2.rectangle(img_a, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(img_b, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # ── Save artefacts ─────────────────────────────────────────────────────
    out_dir = out_dir or Path(__file__).parent / "artefacts"
    out_dir.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_dir / "baseline_marked.png"), img_a)
    cv2.imwrite(str(out_dir / "candidate_marked.png"), img_b)
    cv2.imwrite(str(out_dir / "diff_mask.png"), layout_mask)

    print(f"[INFO] SSIM: {ssim_score:.4f} — artefacts saved → {out_dir}")
    return ssim_score


# ──────────────────────────────────────────────────────────────────────────────
#  CLI
# ──────────────────────────────────────────────────────────────────────────────
def _cli():
    ap = argparse.ArgumentParser(description="Hybrid SSIM + CIELAB ΔE visual diff.")
    ap.add_argument("--baseline", required=True, type=Path)
    ap.add_argument("--candidate", required=True, type=Path)
    return ap.parse_args()


if __name__ == "__main__":
    args = _cli()
    diff_images(args.baseline, args.candidate)

