# Publishing

The workflow follows GitHub's documented custom-workflow model:

1. Validate on every relevant pull request and push.
2. Upload only `site/` as the Pages artifact.
3. Deploy only from `main` or a manual run.
4. Grant `pages: write` and `id-token: write` only to the deploy job.

All GitHub Actions are pinned to immutable commit SHAs. Dependabot may propose
updates, but a human must review the upstream release and resulting diff.

There is no `CNAME` file. GitHub documents that custom-workflow sites configure
their domain in repository settings/API; a `CNAME` file is neither required nor
authoritative for that flow.

Official references:

- [Configuring a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [Using custom workflows with GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
