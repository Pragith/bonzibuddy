#!/usr/bin/env python3
"""Package release downloads from the clean, version-tagged Git snapshot."""

import hashlib
import json
import subprocess
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED


def main():
    root = Path(__file__).resolve().parents[1]

    def git(*args):
        return subprocess.check_output(["git", "-C", str(root), *args])

    if git("status", "--porcelain").strip():
        raise SystemExit("Commit repository changes before packaging a release")
    manifest = json.loads(git("show", "HEAD:pet.json"))
    version = manifest["version"]
    tag = "v" + version
    if git("rev-parse", tag + "^{commit}") != git("rev-parse", "HEAD"):
        raise SystemExit("The version tag must point to HEAD")
    output = root / "work/releases" / tag
    output.mkdir(parents=True, exist_ok=True)
    exports = {
        "bonzi-buddy-v2.png": manifest["spritesheet"],
        "bonzi-buddy-web-v1.png": manifest["compatibility"]["web"]["spritesheet"],
        "bonzi-buddy-preview.mp4": "previews/all-states.mp4",
        "install.html": "install.html",
        "bonzi-buddy-SKILL.md": "skills/bonzi-buddy/SKILL.md",
    }
    for target, source in exports.items():
        (output / target).write_bytes(git("show", "HEAD:" + source))
    for name, expected in [("bonzi-buddy-v2.png", manifest["sha256"]),
                           ("bonzi-buddy-web-v1.png", manifest["compatibility"]["web"]["sha256"])]:
        if hashlib.sha256((output / name).read_bytes()).hexdigest() != expected:
            raise SystemExit("Committed asset does not match manifest: " + name)
    archive = output / ("bonzi-buddy-" + tag + ".zip")
    git("archive", "--format=zip", "--prefix=bonzi-buddy-" + tag + "/",
        "--output=" + str(archive), tag)
    skill_archive = output / ("bonzi-buddy-skill-" + tag + ".zip")
    skill_root = "skills/bonzi-buddy/"
    skill_files = git("ls-tree", "-r", "--name-only", tag, "--", skill_root).decode().splitlines()
    with ZipFile(skill_archive, "w", compression=ZIP_DEFLATED) as package:
        for source in skill_files:
            name = "bonzi-buddy/" + source.removeprefix(skill_root)
            package.writestr(ZipInfo(name), git("show", tag + ":" + source), compress_type=ZIP_DEFLATED)
        package.writestr(ZipInfo("bonzi-buddy/LICENSE"), git("show", tag + ":LICENSE"), compress_type=ZIP_DEFLATED)
    assets = [output / name for name in exports] + [archive, skill_archive]
    sums = "".join(hashlib.sha256(path.read_bytes()).hexdigest() + "  " + path.name + "\n"
                   for path in assets)
    (output / "SHA256SUMS.txt").write_text(sums)
    print(output)


if __name__ == "__main__":
    main()
