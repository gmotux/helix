#!/usr/bin/env python3
"""
Extract room-boundary lines from a floorplan image.

Outputs:
1) Transparent PNG mask containing only detected boundary lines.
2) Preview PNG overlay to visually inspect extraction quality.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage as ndi


def dark_low_saturation_mask(rgb: np.ndarray) -> np.ndarray:
    """Return likely wall pixels (dark + low saturation)."""
    rgb_f = rgb.astype(np.float32) / 255.0
    cmax = np.max(rgb_f, axis=2)
    cmin = np.min(rgb_f, axis=2)
    delta = cmax - cmin
    sat = np.zeros_like(cmax)
    np.divide(delta, cmax, out=sat, where=cmax > 1e-6)
    val = cmax

    # Walls are mostly gray/black lines. Colored labels/logos are filtered out.
    return (val < 0.78) & (sat < 0.23)


def extract_boundaries(mask: np.ndarray) -> np.ndarray:
    """Keep line-like structures (horizontal/vertical wall segments)."""
    # Long horizontal and vertical runs remove most text/noise.
    horiz = ndi.binary_opening(mask, structure=np.ones((1, 17), dtype=bool))
    vert = ndi.binary_opening(mask, structure=np.ones((17, 1), dtype=bool))
    lines = horiz | vert

    # Reconnect broken segments around doors and antialiasing gaps.
    lines = ndi.binary_closing(lines, structure=np.ones((3, 3), dtype=bool))
    lines = ndi.binary_dilation(lines, structure=np.ones((3, 3), dtype=bool))

    # Drop tiny specks.
    labels, n = ndi.label(lines)
    if n == 0:
        return lines
    counts = np.bincount(labels.ravel())
    keep = counts >= 35
    keep[0] = False
    return keep[labels]


def save_mask_and_overlay(
    rgb: np.ndarray,
    line_mask: np.ndarray,
    mask_path: Path,
    lines_path: Path,
    overlay_path: Path,
) -> None:
    h, w, _ = rgb.shape

    # Transparent mask: only boundary lines are opaque.
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    rgba[..., 3] = line_mask.astype(np.uint8) * 255
    Image.fromarray(rgba, mode="RGBA").save(mask_path)

    # White canvas line preview for quick visual review.
    line_preview = np.full((h, w, 3), 255, dtype=np.uint8)
    line_preview[line_mask] = np.array([0, 0, 0], dtype=np.uint8)
    Image.fromarray(line_preview, mode="RGB").save(lines_path)

    # Preview overlay: cyan lines over original floorplan.
    overlay = rgb.copy()
    overlay[line_mask] = np.array([0, 255, 255], dtype=np.uint8)
    Image.fromarray(overlay, mode="RGB").save(overlay_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("gm/assets/building-b-2f.jpg"),
        help="Input floorplan image.",
    )
    parser.add_argument(
        "--mask-output",
        type=Path,
        default=Path("gm/assets/building-b-2f-boundary-mask.png"),
        help="Transparent boundary-only PNG output path.",
    )
    parser.add_argument(
        "--overlay-output",
        type=Path,
        default=Path("gm/assets/building-b-2f-boundary-overlay.png"),
        help="Preview overlay PNG output path.",
    )
    parser.add_argument(
        "--lines-output",
        type=Path,
        default=Path("gm/assets/building-b-2f-boundary-lines.png"),
        help="Line-only preview PNG output path (black lines on white).",
    )
    args = parser.parse_args()

    src = np.array(Image.open(args.input).convert("RGB"))
    base_mask = dark_low_saturation_mask(src)
    line_mask = extract_boundaries(base_mask)
    save_mask_and_overlay(
        src,
        line_mask,
        args.mask_output,
        args.lines_output,
        args.overlay_output,
    )

    print(f"input:   {args.input}")
    print(f"mask:    {args.mask_output}")
    print(f"lines:   {args.lines_output}")
    print(f"overlay: {args.overlay_output}")
    print(f"pixels kept: {int(line_mask.sum())}")


if __name__ == "__main__":
    main()
