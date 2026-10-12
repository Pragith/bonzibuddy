# Repository guidance

Keep this repository focused on the Bonzi Buddy ChatGPT Pet.

- Use `assets/bonzi-buddy.png` as the canonical final sheet and `pet.json` as its manifest.
- Keep source strips, reference downloads and rejected revisions under ignored `work/`.
- Preserve the original character identity. Use grounded image generation for visual changes.
- Keep final reports honest; retain reviewed warnings and rerun checks after changing artwork.
- Run `python3 scripts/verify.py` before committing. Do not claim it replaces visual QA or Pets preflight.
- Show motion previews before uploading an updated pet. Do not persist upload sessions or signed URLs.
- MIT covers code and documentation; do not extend it to character artwork or third-party rights.
- Keep the README current instead of adding duplicate status documents.
- Keep conversational personality in `skills/bonzi-buddy/SKILL.md`; pet selection does not load it automatically.
