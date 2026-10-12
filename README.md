# Bonzi Buddy

A BonziBUDDY-inspired animated ChatGPT Pet. The artwork recreates the original
purple gorilla's appearance; it does not contain the original software, voice,
or animation frames.

![Animation preview](previews/motion-overview.gif)

## Download and install

Get [v1.0.1](https://github.com/Pragith/bonzibuddy/releases/tag/v1.0.1) or the
[latest release](https://github.com/Pragith/bonzibuddy/releases/latest).

- **ChatGPT desktop:** download `install.html`, open it in a browser and click
  **Install Bonzi Buddy**. It opens the app's v2 pet installation flow. After
  installation, choose Bonzi Buddy in **Settings > Pets** and use `/pet` to show it.
- **ChatGPT web:** download `bonzi-buddy-web-v1.png`, then use **Settings >
  Personalization > Pet > Select pet > Upload pet**. The v1 sheet includes the nine
  standard animations; the full v2 sheet adds sixteen directional looks.
- **Everything together:** download `bonzi-buddy-v1.0.1.zip`. Checksums are in
  `SHA256SUMS.txt`; verify with `shasum -a 256 -c SHA256SUMS.txt` beside the files.

Pets must be available for your account and workspace. Desktop pets are local
and do not automatically sync to the web. The install launcher uses the
[documented desktop deep link](https://learn.chatgpt.com/docs/app/commands);
web upload and selection follow [OpenAI's Pets guide](https://learn.chatgpt.com/docs/pets).

## Files

- `assets/bonzi-buddy.png`: final transparent ChatGPT Pets v2 sprite sheet.
- `previews/`: animation overview, directional loop, MP4, contact sheet and stills.
- `pet.json`: format, provenance, checksum and validation summary.
- `validation/`: final structural, quality and direction reports.
- `scripts/verify.py`: checks the exact artifact and all required cells.
- `skills/bonzi-buddy/SKILL.md`: reusable conversational personality, separate from the pet.
- `work/`: ignored generation sources, prompts, revisions and account-specific record.

The sheet is 1536 × 2288 pixels, with 192 × 208 cells in eight columns and eleven
rows. Its 73 frames cover nine animation states and sixteen clockwise look
directions. Unused cells remain transparent.

## Bonzi's personality

[The personality skill](skills/bonzi-buddy/SKILL.md) gives the assistant a cheerful,
curious, slightly goofy retro-companion voice. It keeps technical answers accurate
and adapts to serious topics. It is an original interpretation of Bonzi's character.

Download `bonzi-buddy-skill-v1.0.1.zip` from the release. To use it as a local
Codex skill, extract the `bonzi-buddy` folder into `~/.codex/skills/`, reload
skills, and invoke:

```text
Use $bonzi-buddy to help me plan my day.
```

For a chat without skill installation, attach the standalone `bonzi-buddy-SKILL.md`
and ask: "Follow this personality guide for this conversation."

The animated pet and conversational personality are separate. Choosing the pet
does not automatically load the skill, change the assistant's spoken voice, or
recreate Bonzi's original speech synthesizer. Personality instructions use the
repository's MIT license.

## Verify

Use Python 3 with Pillow installed:

```sh
python3 -m pip install -r requirements.txt
python3 scripts/verify.py
```

To regenerate motion previews, run `python3 scripts/preview.py`. With FFmpeg
installed, refresh the MP4 using:

```sh
ffmpeg -y -i previews/all-states.gif -movflags +faststart -pix_fmt yuv420p previews/all-states.mp4
```

Structural checks, the bundled pet quality gate and ChatGPT Pets preflight passed
on the final bytes. Independent reviewers confirmed the four cardinal looks.
The reports retain warnings for subtle intermediate directions and larger
changes where the two look strips meet. Toe and leg gaps are intentional.

## Creation and use

The canonical design and individual animation strips were generated with OpenAI
image generation, grounded in the same character reference. The ChatGPT Pet
creation tools extracted the poses, assembled the sheet, removed background
spill and rendered previews. Generation is not a deterministic rebuild.

The release sheet was uploaded to an existing custom ChatGPT pet on October 12,
2026. Its downloaded pixels matched the repository artwork exactly. The v1 and
v2 sheets both passed Pets preflight. Selection as active is separate from
installation. Account-specific records remain in ignored `work/`.

The desktop launcher has been checked against the documented URL contract.
Its interactive installation flow still needs testing in the desktop app.

For future changes, preserve the approved character proportions, regenerate only
the affected source strips, rerun the complete final validation, and show motion
previews before uploading. Do not rotate or warp a sprite to invent look poses.

## Make a release

Update `pet.json` and the versioned download links, verify the artwork, commit
the files, and tag that commit. `python3 scripts/release.py` builds downloads
from that exact tagged Git snapshot into ignored `work/releases/`. It refuses
an uncommitted checkout or a version tag that points elsewhere. Publish those
files with GitHub Releases; generation sources and account records stay local.

## License and provenance

Project code and documentation use the [MIT license](LICENSE).
Character artwork is excluded; see [NOTICE](NOTICE) for its separate rights status.

Visual reference: [Bonzi Buddy image on PNGAAA](https://www.pngaaa.com/detail/2991702).
That page labels its reference image for non-commercial use. The downloaded
reference and rejected revisions are retained locally in ignored `work/`.
This is an unofficial fan recreation with no affiliation claim.
