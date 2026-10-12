#!/usr/bin/env python3
"""Verify the final pet's checksum, geometry and populated cells."""

import hashlib
import json
from pathlib import Path

from PIL import Image


def main():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "pet.json").read_text())
    path = root / manifest["spritesheet"]
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    errors = []
    if digest != manifest["sha256"]:
        errors.append("Sprite checksum differs from pet.json")
    if not 0 < len(data) <= 20 * 1024 * 1024:
        errors.append("Sprite exceeds the supported file size")
    with Image.open(path) as image:
        if image.format != "PNG" or image.mode != "RGBA":
            errors.append("Sprite must be an RGBA PNG")
        if image.size != tuple(manifest["dimensions"]):
            errors.append("Sprite dimensions differ from pet.json")
        image = image.convert("RGBA")
        width, height = manifest["cell_dimensions"]
        populated = 0
        for row, count in enumerate(manifest["frames_per_row"]):
            for column in range(8):
                alpha = image.crop((column * width, row * height,
                                    (column + 1) * width, (row + 1) * height)).getchannel("A")
                bounds = alpha.point(lambda value: 255 if value > 16 else 0).getbbox()
                if column < count:
                    if bounds is None:
                        errors.append(f"Missing artwork in row {row}, frame {column}")
                    else:
                        populated += 1
                        if bounds[0] == 0 or bounds[1] == 0 or bounds[2] == width or bounds[3] == height:
                            errors.append(f"Artwork touches cell boundary: row {row}, frame {column}")
                elif alpha.getbbox() is not None:
                    errors.append(f"Unused cell contains artwork: row {row}, frame {column}")
    for name in ("atlas.json", "quality.json"):
        report = json.loads((root / "validation" / name).read_text())
        if not report.get("ok") or report.get("sha256") != digest:
            errors.append(f"{name} is failed or describes different bytes")
    blind = json.loads((root / "validation/directions-blind.json").read_text())
    if not blind.get("ok"):
        errors.append("Independent direction check did not pass")
    preflight = json.loads((root / "validation/preflight.json").read_text())
    if not preflight.get("valid") or preflight.get("sha256") != digest:
        errors.append("Pets preflight is failed or describes different bytes")
    print(json.dumps({"ok": not errors, "populated_cells": populated,
                      "sha256": digest, "errors": errors}, indent=2))
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
