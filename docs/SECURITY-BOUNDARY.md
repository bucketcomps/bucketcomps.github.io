# Publication boundary 🔒

This repository is a deliberately small public projection. Public Git history is
permanent enough that "we can remove it later" is not an acceptable control.

## Allowed

- Hand-authored HTML and CSS
- Public-safe, dated progress summaries
- Links to public repositories and deliberately published services
- Generic diagrams and original interface graphics
- Public licensing and contribution instructions

## Forbidden

- Game-derived images, video, audio, executables, memory, or extracted assets
- ROMs, keys, firmware, SDK material, or decrypted content
- Copies of private wikis, internal evidence packets, or raw development notes
- Local paths, private infrastructure coordinates, process metadata, or logs
- Live runtime payloads, credentials, account identifiers, or personal data
- Symlinks or generated output that can escape `site/`

## Data flow

Nothing in this repository pulls from the private source repository at build
time. Public summaries must be manually selected from an already sanitized
release, reviewed in a pull request, and committed as static prose. GitHub Pages
receives only the `site/` artifact.

The live hostname is a link, not a data dependency. The static site remains
usable when the live service is offline.
