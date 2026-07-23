# Custom-domain cutover — held

**State:** staged only. No custom domain, DNS record, tunnel route, or service
change is authorized by this document.

## Preconditions

- Both default GitHub Pages URLs pass HTTPS, link, accessibility, and
  negative-exposure checks.
- The `bucketcomps/infamous` dossier PR is merged and its project Pages
  deployment is healthy.
- The current public program has a recorded rollback target.
- The owner explicitly approves the maintenance window and exact hostnames.
- `decomp.deucebucket.com` is verified for the BucketComps organization before
  it is attached, reducing domain-takeover risk.

## Static site cutover

1. Record the current `decomp` DNS answer, Cloudflare record ID/settings, and
   HTTP status matrix. Do not alter the plural compatibility hostname.
2. In `bucketcomps/bucketcomps.github.io` → Settings → Pages, set the custom
   domain to `decomp.deucebucket.com`. Do not add a repository `CNAME` file.
3. In Cloudflare DNS, replace only the reviewed `decomp` record with a CNAME to
   `bucketcomps.github.io`. Use DNS-only during GitHub domain verification and
   certificate issuance; do not use a wildcard.
4. Wait until GitHub reports the DNS check successful and provisions the
   certificate. Then enable **Enforce HTTPS**.
5. Verify:
   - `https://decomp.deucebucket.com/`
   - `https://decomp.deucebucket.com/infamous/`
   - static assets below both paths
   - a deliberate 404 for private filenames and unknown routes
6. Preserve `https://bucketcomps.github.io/` and
   `https://bucketcomps.github.io/infamous/` as the default rollback evidence,
   noting that GitHub may redirect them while the custom domain is attached.

## Live-hostname cutover

This is a separate change after the static site is healthy.

1. In Cloudflare's existing remotely managed tunnel, add a published
   application for `live.decomp.deucebucket.com` pointing to the existing
   fail-closed sanitized local HTTP service. Do not point it at a repository
   checkout or general-purpose file server.
2. Cloudflare creates the tunnel CNAME. Confirm the tunnel and DNS record belong
   to the expected account and that no wildcard was introduced.
3. Verify the positive live route matrix and negative exposure matrix before
   updating any static label from **proposed** to **live**.
4. Confirm the original live hostname still works until the owner approves its
   retirement or compatibility role.

## Rollback

If static checks fail, restore the recorded `decomp` DNS record and remove the
custom domain from the organization Pages settings. If only the live hostname
fails, remove that exact tunnel application/DNS route; do not touch the static
site or the existing live route. Re-run the original status matrix after either
rollback.

Official references:

- [Managing a GitHub Pages custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
- [Verifying a GitHub Pages custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages)
- [Cloudflare Tunnel routing](https://developers.cloudflare.com/tunnel/routing/)
- [Cloudflare DNS record management](https://developers.cloudflare.com/dns/manage-dns-records/how-to/create-dns-records/)
