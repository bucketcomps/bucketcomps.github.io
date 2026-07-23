# Public web architecture

## Surfaces

| Surface | Repository / origin | Purpose |
| --- | --- | --- |
| Program landing | `bucketcomps/bucketcomps.github.io` | Cross-project index and public boundary |
| Game dossier | One public repository per game | Static devlog, milestones, methodology, and links |
| Live program | Local sanitized publisher | Dynamic telemetry and approved stream views |
| Internal work | Private repositories and local evidence stores | Source recovery, verification, raw evidence, operations |

GitHub calls the first surface an **organization site** and each game surface a
**project site**. With no custom domain, their URLs are:

- `https://bucketcomps.github.io/`
- `https://bucketcomps.github.io/infamous/`

When a custom domain is later assigned to the organization site, GitHub also
serves project sites below that domain by default. That makes the intended static
layout:

- `https://decomp.deucebucket.com/`
- `https://decomp.deucebucket.com/infamous/`

Dynamic content remains a different trust boundary:

- `https://live.decomp.deucebucket.com/infamous`

## Why the split matters

Static public repositories are reviewable, cacheable, and intentionally boring
to operate. Live telemetry changes independently and must remain behind the
existing fail-closed sanitizer. A game dossier can have its own theme without
coupling its release cadence to the stream.

Official references:

- [What is GitHub Pages?](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [About custom domains and project-site inheritance](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages)
- [Cloudflare Tunnel routing](https://developers.cloudflare.com/tunnel/routing/)
