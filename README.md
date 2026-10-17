# BucketComps public landing ⚡

This repository is the public, static front door for the BucketComps
preservation program.

- Default Pages URL: <https://bucketcomps.github.io/>
- Platform: <https://decomp.deucebucket.com/>
- Project dossiers: one public repository per game
- Live dashboards: locally hosted behind a separate, explicit live hostname

The site contains no game assets, ROM data, keys, private evidence, runtime
telemetry, or credentials. See [the security boundary](docs/SECURITY-BOUNDARY.md)
before contributing.

## Work locally

```sh
python3 scripts/check_site.py
python3 -m http.server 8080 --directory site
```

Then open <http://127.0.0.1:8080/>.

## Publishing

Pushes to `main` validate and deploy `site/` through GitHub Pages. Every action
dependency is pinned to a full commit SHA. Pull requests validate but do not
deploy.

The custom domain and Cloudflare records are intentionally **not configured**.
The reviewed future procedure lives in [docs/CUTOVER.md](docs/CUTOVER.md).
