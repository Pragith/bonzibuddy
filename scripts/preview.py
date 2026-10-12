#!/usr/bin/env python3
"""Render compact motion previews from the canonical sprite sheet."""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def save_gif(frames, output, durations):
    palette = frames[0].quantize(colors=128)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    indexed[0].save(output, save_all=True, append_images=indexed[1:],
                    duration=durations, loop=0, disposal=2, optimize=True)


def main():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "pet.json").read_text())
    atlas = Image.open(root / manifest["spritesheet"]).convert("RGBA")
    output = root / "previews"
    output.mkdir(exist_ok=True)
    font = ImageFont.load_default(size=16)
    titles = ["Idle", "Move right", "Move left", "Wave", "Jump",
              "Disappointed", "Waiting", "Thinking", "Reviewing"]
    width, height = manifest["cell_dimensions"]
    rows = []
    for row, count in enumerate(manifest["frames_per_row"]):
        rows.append([atlas.crop((i * width, row * height,
                                 (i + 1) * width, (row + 1) * height))
                     for i in range(count)])

    def tile(image, title):
        canvas = Image.new("RGBA", (width, height + 28), "#f4f2f8")
        canvas.alpha_composite(image, (0, 25))
        ImageDraw.Draw(canvas).text((width // 2, 4), title, fill="#382345",
                                    anchor="mt", font=font)
        return canvas.convert("RGB")

    grid = []
    for tick in range(24):
        canvas = Image.new("RGB", (width * 3, (height + 28) * 3), "#f4f2f8")
        for i, title in enumerate(titles):
            image = rows[i][tick % len(rows[i])]
            canvas.paste(tile(image, title), ((i % 3) * width, (i // 3) * (height + 28)))
        grid.append(canvas.resize((384, 472), Image.Resampling.LANCZOS))
    save_gif(grid, output / "motion-overview.gif", 160)
    save_gif([tile(image, "Looking around") for image in rows[9] + rows[10]],
             output / "look-loop.gif", 220)

    sequence, durations = [], []
    for i, title in enumerate(titles):
        sequence.extend(tile(image, title) for image in rows[i])
        durations.extend([180] * (len(rows[i]) - 1) + [650])
    save_gif(sequence, output / "all-states.gif", durations)

    stills = Image.new("RGB", (width * 4, height + 28), "#f4f2f8")
    for i, (row, frame, title) in enumerate([(0, 2, "Blink"), (3, 2, "Wave"),
                                            (4, 2, "Airborne"), (7, 1, "Thinking")]):
        stills.paste(tile(rows[row][frame], title), (i * width, 0))
    stills.save(output / "motion-stills.png")
    print("Rendered previews from", manifest["spritesheet"])


if __name__ == "__main__":
    main()
