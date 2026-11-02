# Contributing to the Grana website

Contributions to the Grana website are accepted under the [Apache License 2.0](LICENSE).
Preserve existing upstream copyright and license notices. When adding or
adapting third-party code or assets, document their source, revision, license,
and any modifications in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Add
their license details and links to full license texts in
[THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

## Signing Your Work

Every contributor must sign off each commit under the
[Developer Certificate of Origin 1.1](https://developercertificate.org/).
A sign-off certifies that you created the contribution or have the right to
submit it under the applicable open-source license. This project uses DCO
sign-off and does not require a separate contributor license agreement.

Use your real name and email address:

```bash
git commit -s -m "Describe the change"
```

This adds a trailer such as:

```text
Signed-off-by: Your Name <your.email@example.com>
```

Commits without the required sign-off will not be accepted.

## Development workflow

This repository is a static website: [index.html](index.html) and [assets/](assets/)
contain its pages, styles, scripts, fonts, images, and videos. The
[GitHub Pages workflow](https://github.com/reward-grana/reward-grana.github.io/blob/main/.github/workflows/pages.yml)
copies root-level HTML files, `.nojekyll`, `assets/`, and the five policy documents
(`LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, `THIRD_PARTY_LICENSES.md`, and
`THIRD_PARTY_NOTICES.md`) into the published site. It runs on pushes to `main`
and can also be dispatched manually for `main`.

1. Fork the repository and create a feature branch from `main`.
2. From the repository root, preview the site with Python 3:

   ```bash
   python3 -m http.server 8000 --bind 127.0.0.1
   ```

   Open `http://127.0.0.1:8000/` in a browser. Stop the preview with `Ctrl+C`
   when finished. The website has no local build or package-install step.
3. Keep changes focused on website content, presentation, or behavior. Place
   new static assets under `assets/` and use paths that work on GitHub Pages.
   If you change a file referenced with a `?v=` cache version, update the
   corresponding references. Ensure any new published paths are included by
   the Pages workflow.
4. Check the affected pages at desktop and mobile widths. Verify navigation,
   links, images, and any changed charts or video controls. Check keyboard
   access and reduced-motion behavior when changing interactive content, and
   inspect the browser console and network panel for errors or missing files.
5. Before submitting, run these basic repository checks:

   ```bash
   git diff --check
   test -s index.html
   test -f .nojekyll
   ```

   Confirm that new or changed local links resolve and that each added asset
   is approved for public distribution with the required attribution and
   license notices. Do not commit credentials or unpublished material.
6. Open a pull request against `main` describing the problem, the resulting
   behavior, and the checks you ran. Include screenshots for visual changes
   and note any browser-specific limitations or external dependencies.

Follow [SECURITY.md](SECURITY.md) for private vulnerability reports. Contributors
are expected to communicate respectfully and professionally.

## Full text of the DCO

```text
Developer Certificate of Origin
Version 1.1

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.


Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```
